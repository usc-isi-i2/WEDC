from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

dbase = declarative_base()
engine = None



def create_database(db_url, db_type='sqlite'):
    dbase.metadata.create_all(engine)


def link_database(db_url, db_type='sqlite'):
    if db_type == 'sqlite':
        db_url = 'sqlite:///' + db_url
    engine = create_engine(db_url)
    dbase.metadata.bind = engine



def initialize_db():
    """ Be careful !!!!!!!
    """
    db.create_all()
    models.PSABase.metadata.create_all(db.engine)

def drop_db():
    db.drop_all()


