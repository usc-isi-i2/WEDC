import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

from wedc.domain.entities import post


class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
       pass

    def test_remove_url(self):
        self.assertEquals(post.remove_url('something.ad'), '')
        self.assertEquals(post.remove_url('something.com'), '')
        self.assertEquals(post.remove_url('http://something.ad'), '')
        self.assertEquals(post.remove_url('https://something.ad'), '')

    def test_has_url(self):
        self.assertTrue(post.has_url('locumtenens.com is looking for a gastroenterologist in california , not far from san francisco .'))

        
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()