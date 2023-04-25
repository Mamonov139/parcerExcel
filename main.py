from ETL import init_db
from Utils import clearDb
from Utils.Parser import Parcer, Analyze


if __name__ == '__main__':
    init_db()
    clearDb()
    files = Parcer('1.xlsx')
    files.doParse()
    analytic = Analyze(('Qliq', 'Qoil'))
    out = analytic.doAnalyze()
    print(out)








