import sys
import time
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# text_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'text'))

from wedc.application.api import WEDC

class TestPostVectorMethods(unittest.TestCase):
    def setUp(self):
        self.api = WEDC()

    def test(self):
        

    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()

    def run_main_test():
        suite = unittest.TestSuite()
        suite.addTest(TestPostVectorMethods("test"))
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()



