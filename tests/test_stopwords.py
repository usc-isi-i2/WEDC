

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
        from sets import Set
        from wedc.domain.vendor.nltk import stem

        names = stopword_helper.get_person_names()
        country, country_abbr = stopword_helper.get_country_names()
        stop_set = Set(names) | Set(country) | Set(country_abbr)
        stop_set = [stem.stemming(_).strip() for _ in stop_set]
        if 'singapor' in stop_set:
            print 'ss'

        
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



