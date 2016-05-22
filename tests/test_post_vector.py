import sys
import time
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

text_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'text'))
word2vec_model_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'word2vec_model.bin'))
weighted_seed_dict_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'weighted_seed_dict'))
post2vec_  = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'post2vec.txt'))
post2vec_seeds_  = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'post2vec_seeds.txt'))

from wedc.domain.vendor.word2vec import w2v
from wedc.domain.core.data.seed import seed_vector
from wedc.domain.core.data.seed import seed_word


class TestPostVectorMethods(unittest.TestCase):
    def setUp(self):
        self.seeds = seed_word.load_weighted_seed_dict(weighted_seed_dict_)

    def test_post2sv(self):
        seed_vector.post2sv(text_, post2vec_, self.seeds)

    def test_post2seeds(self):
        seed_vector.post2seed(text_, output=post2vec_seeds_, seeds=self.seeds)

    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()

    def run_main_test():
        suite = unittest.TestSuite()
        # suite.addTest(TestPostVectorMethods("test_post2sv"))
        suite.addTest(TestPostVectorMethods("test_post2seeds"))
        
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()



