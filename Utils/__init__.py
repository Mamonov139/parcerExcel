from ETL import withSession
from ETL.models import ParseOut


@withSession()
def clearDb(ses):
    ses.query(ParseOut).delete()
    ses.commit()