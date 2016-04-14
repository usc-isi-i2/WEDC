
import sys
import time
import os
import unittest


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

input_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'text'))
output_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'post_vec.txt'))


class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        pass

    
        
    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()

    def run_main_test():
        suite = unittest.TestSuite()
       
        suite.addTest(TestDataLoaderMethods("test_load_all_data_to_disk"))
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()



