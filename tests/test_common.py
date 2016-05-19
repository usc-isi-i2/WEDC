import sys
import time
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


class TestCSVMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_read_csv(self):
        import csv
        csv_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'groundtruth.csv'))
        with open(csv_) as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):
                print i+1
                print row
                # print row[1].decode('ascii', 'ignore')
                # print ', '.join(row)
                print '\n\n\n\n'

    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()

    def run_main_test():
        suite = unittest.TestSuite()
        suite.addTest(TestCSVMethods("test_read_csv"))
       
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()



