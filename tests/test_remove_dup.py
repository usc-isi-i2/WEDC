

import sys
import time
import os
import unittest




sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

input_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'text'))
output_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'text_no_dup'))


from wedc.domain.service.data import remove_duplication


class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_remove_dup(self):
        remove_duplication.remove_dup(input_, output_)

        
    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()

    def run_main_test():
        suite = unittest.TestSuite()
        suite.addTest(TestDataLoaderMethods("test_remove_dup"))
        
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()



