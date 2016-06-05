
import os
import sys

# from wedc.application.api import api
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

def load_engine():
    db_uri = 'sqlite:///wedc.db' # api.config('DATABASE_URI')
    engine = create_engine(db_uri)
    return engine

def load_session():
    dbase.metadata.create_all(engine)
    dbase.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = load_session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        print 'DATABASE ERROR'
        # raise
    finally:
        session.close()

def create_database():
    from wedc.infrastructure.model.labelled_data import LabelledData
    from wedc.infrastructure.model.need_to_label_data import NeedToLabelData
    from wedc.infrastructure.model.seed_dict import SeedDict
    dbase.metadata.create_all(engine)

def drop_database():
    dbase.metadata.drop_all(engine)

dbase = declarative_base()
engine = load_engine()



