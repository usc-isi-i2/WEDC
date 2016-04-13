

import sys
import time
import os
import unittest




sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

input_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'text'))
output_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'post_vec.txt'))
output_bin = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'vectors.bin'))

from wedc.domain.service.keyword_extraction.word2vec import base
base.load_word2vec_model(output_bin)

from wedc.domain.service.keyword_extraction.seeds import seed_word
from wedc.domain.service.keyword_extraction.word2vec import similarity

from wedc.domain.vendor.nltk import stem
from wedc.domain.service.keyword_extraction.seeds import post2sv






class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_post2sv(self):
        post2sv.post2sv(input_, output_)




        
    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()

    def run_main_test():
        suite = unittest.TestSuite()
        suite.addTest(TestDataLoaderMethods("test_post2sv"))
        
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()



