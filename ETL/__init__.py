from urllib.parse import quote
from enum import Enum
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import wraps

from Config import configs
from ETL.models import Base


nameDB = configs.get('postgres', 'nameBD')

all = ('init_db')


def makeEngine(engine):
    pw = quote(configs.get('postgres', 'password'), safe='')
    usr = configs.get('postgres', 'username')
    host = configs.get('postgres', 'host')
    port = configs.get('postgres', 'port')
    hostname = f'{host}:{port}' if port else host
    engineString = f'postgresql://{usr}:{pw}@{hostname}/{engine}'
    engine = create_engine(engineString)
    return engine


def init_db():
    engine = makeEngine(nameDB)
    Base.metadata.create_all(engine)


def withSession(engine: str = nameDB, is_class_method: bool = False):
    def withSessionDecorator(func):

        def initSession():
            sessionClass = sessionmaker(bind=makeEngine(engine))
            SQLSession = sessionClass()
            return SQLSession

        @wraps(func)
        def wrapper1(*args, **kwargs):
            SQLSession = initSession()
            res = func(SQLSession, *args, **kwargs)
            SQLSession.close()
            return res

        @wraps(func)
        def wrapper2(self, *args, **kwargs):
            SQLSession = initSession()
            res = func(self, SQLSession, *args, **kwargs)
            SQLSession.close()
            return res

        return wrapper1 if not is_class_method else wrapper2

    return withSessionDecorator