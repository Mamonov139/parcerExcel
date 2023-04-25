from itertools import groupby

import pandas as pd
from datetime import datetime as DT

from sqlalchemy import func

from ETL import withSession
from datetime import timedelta
import random

from ETL.models import ParseOut


def get_random_date():
    start_dt = DT.strptime('01.01.2017', '%d.%m.%Y')
    end_dt = DT.strptime('31.01.2017', '%d.%m.%Y')
    delta = end_dt - start_dt
    return start_dt + timedelta(random.randint(0, delta.days))


class ParserError(Exception):
    default_detail = 'не удалось открытть файл'
    detail = ''

    def __init__(self, detail=None, status_code=None):
        if detail is None:
            detail = self.default_detail

        self.detail = detail
        self.status_code = status_code

    def __str__(self):
        return str(self.detail)


class Parcer:
    def __init__(self, fileName):
        try:
            self.file = pd.read_excel(fileName, header=[0, 1, 2])
        except Exception as e:
            raise ParserError(f'не удалось открыть файл: {e.__class__.__name__} ({str(e)})')

    @withSession(is_class_method=True)
    def doParse(self, ses):
        for i, columns in enumerate(self.file.columns.levels):
            columns_new = columns.tolist()
            for j, row in enumerate(columns_new):
                if "Unnamed: " in row:
                    columns_new[j] = ""
            self.file = self.file.rename(columns=dict(zip(columns.tolist(), columns_new)), level=i)

        for i, v in self.file.iterrows():
            a = v.to_dict()
            id = a.pop(('id', '', ''))
            company = a.pop(('company', '', ''))
            date = get_random_date()
            headers = [k for k, v1 in a.items()]
            for key, item in groupby(headers, key=lambda x: (x[0], x[1])):
                out = {'status_type': key[0], 'typeq': key[1], 'id': id, 'company': company, 'date': date}
                for value in item:
                    out.update({f'{value[2]}': a[value]})
                instanc = ParseOut(**out)
                ses.add(instanc)
        ses.commit()


class Analyze:
    def __init__(self, namesAttr):
        self.attrs = namesAttr

    @withSession(is_class_method=True)
    def doAnalyze(self, ses):
        qu = ses.query(ParseOut.date, ParseOut.typeq,
                       (func.sum(ParseOut.data1) + func.sum(ParseOut.data2)).label('total')). \
            group_by(ParseOut.date, ParseOut.typeq).order_by(ParseOut.date)
        out = {}
        for attr in self.attrs:
            out[attr] = [{'date': DT.strftime(i.date, '%d.%m.%Y'), 'total': i.total} for i in qu.filter_by(typeq=attr)]
        return out
