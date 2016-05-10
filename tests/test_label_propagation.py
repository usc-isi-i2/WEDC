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

post2vec_  = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'post2vec.txt'))
post2vec_label_  = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'post2vec_label.txt'))
post2vec_predict_  = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'post2vec_predict.txt'))

from wedc.domain.core.ml.graph import knn
from wedc.domain.core.ml.helper import label
from wedc.domain.core.ml.classifier.label_propagation import lp

class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        label_dict = label.load_label_dict()
        label.generate_label_file(label_dict, post2vec_label_)

    def test_generate_label_file(self):
        label_dict = label.load_label_dict()
        label.generate_label_file(label_dict, post2vec_label_)

    def test_do_label_propagation(self):
        lp.do_label_propagation(input_data=post2vec_,
                                input_label=post2vec_label_,
                                output=post2vec_predict_,
                                kernel='knn',
                                n_neighbors=10, 
                                alpha=1, 
                                max_iter=100, 
                                tol=0.000001)


    def test_build_knn_graph(self):
        knn.build_graph(post2vec_, graph_)
        
    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()

    def run_main_test():
        suite = unittest.TestSuite()
        # suite.addTest(TestDataLoaderMethods("test_generate_label_file"))
        suite.addTest(TestDataLoaderMethods("test_do_label_propagation"))
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()


