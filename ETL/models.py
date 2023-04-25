from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db

Base = declarative_base()


def getData(dt: datetime = None) -> str:
    if not dt:
        dt = datetime.now()
    return f'{dt.strftime("%Y-%m-%d %H:%M:%S")}.{f"{dt.microsecond * 1e-6:.3f}".split(".")[1]}'


class ParseOut(Base):
    """
    Специальная таблица для описания работ, внесенных в смету
    """
    __tablename__ = 'parser_out'
    __table_args__ = {'schema': 'public'}
    id = db.Column(db.String(32), primary_key=True)
    company = db.Column(db.String(32), primary_key=True)
    typeq = db.Column(db.String(32), primary_key=True)
    data1 = db.Column(db.Integer, primary_key=True)
    data2 = db.Column(db.Integer, primary_key=True)
    status_type = db.Column(db.String(32), primary_key=True)
    date = db.Column(db.DateTime)
