""" Test word2vec

Example:
http://nbviewer.jupyter.org/github/danielfrg/word2vec/blob/master/examples/doc2vec.ipynb
http://nbviewer.jupyter.org/github/danielfrg/word2vec/blob/master/examples/word2vec.ipynb

"""


import sys
import time
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

text_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'text'))
word2vec_model_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'word2vec_model.bin'))

from wedc.domain.vendor.word2vec import w2v

class TestWord2VecMethods(unittest.TestCase):
    def setUp(self):
        w2v.word2vec_model = w2v.load_model(word2vec_model_)

    def test_setup_model(self):
        w2v.setup_model(text_, 
                        word2vec_model_, 
                        binary=1, 
                        cbow=0, 
                        size=300, 
                        window=10, 
                        negative=5, 
                        hs=0, 
                        threads=12, 
                        iter_=5, 
                        min_count=5, 
                        verbose=False)
        
    def test_get_similars_by_word(self):
        print w2v.get_similars_by_word('young', n=100)
        
    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()
    def run_main_test():
        suite = unittest.TestSuite()

        # suite.addTest(TestWord2VecMethods("test_setup_model"))
        suite.addTest(TestWord2VecMethods("test_get_similars_by_word"))

        runner = unittest.TextTestRunner()
        runner.run(suite)
    run_main_test()



