import sys
import os
import time
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

from wedc.domain.service.data.base import *


class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        filename = 'san-francisco-maria-2.json'
        self.path = os.path.join(TEST_DATA_DIR, filename)
        
    def test_data_loader(self):
        start_time = time.time()
        posts = load_by_path(self.path)
        print 'Total posts: ', len(posts)
        print 'Time cost:', (time.time() - start_time), 'seconds'
        self.assertIsNotNone(posts)
        # Total posts:  49974
        # Time cost: 133.985596895 seconds
        

        # for post in posts:
        #     self.assertFalse(type(post) is list)
            # if type(post) is list:
            #     print post
            #     break


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()