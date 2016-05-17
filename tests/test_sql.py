import sys
import os
import time
import unittest
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

database_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'wedc.db'))

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class TestSeedWordMethods(unittest.TestCase):
    def setUp(self):
        # self.conn = sqlite3.connect(database_)
        self.db = create_engine('sqlite:///' + database_)
        Base.metadata.create_all(self.db)
        Base.metadata.bind = self.db
        DBSession = sessionmaker(bind=self.db)
        self.session = DBSession()

    def test_sql(self):
         
        new_person = Person(name='new person')
        self.session.add(new_person)
        self.session.commit()

        persons = self.session.query(Person)
        for person in persons:
            print person.name


    def tearDown(self):
        pass



if __name__ == '__main__':
    # unittest.main()
    def run_main_test():
        suite = unittest.TestSuite() 

        
        suite.addTest(TestSeedWordMethods("test_sql"))

        runner = unittest.TextTestRunner()
        runner.run(suite)
    run_main_test() 