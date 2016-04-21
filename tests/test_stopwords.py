

import sys
import time
import os
import unittest




sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

from wedc.domain.core.common import stopword_helper


class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_stopwords(self):
        print stopword_helper.get_male_names()[0]

        
    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()

    def run_main_test():
        suite = unittest.TestSuite()
        suite.addTest(TestDataLoaderMethods("test_get_stopwords"))
        
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()



