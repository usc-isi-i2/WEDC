import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

from wedc.domain.core.http import domain


class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
       pass

    def test_domain_ext_list(self):
        de_list = domain.get_domain_ext_list()
        print de_list
        
        
   
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()