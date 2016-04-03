import sys
import os
import unittest
import word2vec

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

from wedc.domain.service.data.base import *
from wedc.domain.service.keyword_extraction.base import *


class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        filename = 'san-francisco-maria.json'
        self.path = os.path.join(TEST_DATA_DIR, filename)
        self.posts = load_by_path(self.path)
        
    def test_word2vec(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()