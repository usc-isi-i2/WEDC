import sys
import time
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# text_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'text'))

from wedc.infrastructure import database

class TestDatabaseMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_create_database(self):
        database.create_database()

    def test_drop_database(self):
        database.drop_database()

    def tearDown(self):
        pass

class TestLabelledDataMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_insert_data(self):
        LabelledData.insert(content='test_content', label=1, flag=2)

    def test_insert_from_csv(self):
        csv_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'groundtruth.csv'))
        LabelledData.insert_from_csv(csv_)

    def test_load_data(self):
        for data in LabelledData.load_data():
            print data.label, data.content

    def test_clear_data(self):
        print LabelledData.clear_data()

    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()

    def run_main_test():
        suite = unittest.TestSuite()
        suite.addTest(TestDatabaseMethods("test_create_database"))
        # suite.addTest(TestDatabaseMethods("test_drop_database"))
    
        # suite.addTest(TestLabelledDataMethods("test_insert_data"))
        # suite.addTest(TestLabelledDataMethods("test_insert_from_csv"))
        # suite.addTest(TestLabelledDataMethods("test_load_data"))
        # suite.addTest(TestLabelledDataMethods("test_clear_data"))
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()



