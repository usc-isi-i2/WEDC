import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

from wedc.domain.service.data.base import *


class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        filename = 'san-francisco-maria.json'
        self.path = os.path.join(TEST_DATA_DIR, filename)
        
    def test_data_loader(self):
        posts = load_by_path(self.path)
        self.assertIsNotNone(posts)
        print posts[2]

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()