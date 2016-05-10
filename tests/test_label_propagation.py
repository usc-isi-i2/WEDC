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

from wedc.domain.core.ml.graph import knn
from wedc.domain.core.ml.helper import label

class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_generate_label_file(self):
        # -1: unknown
        #  1: others
        #  2: massage
        #  3: escort
        #  4: job_ads
 
        label_dict = {
                        1:4,
                        2:4,
                        3:4,
                        4:1,
                        5:4,
                        6:4,
                        7:4,
                        8:4,
                        9:3,
                        10:3
                    }
        label.generate_label_file(label_dict, post2vec_label_)

    def test_build_knn_graph(self):
        knn.build_graph(post2vec_, graph_)
        
    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()

    def run_main_test():
        suite = unittest.TestSuite()
        suite.addTest(TestDataLoaderMethods("test_generate_label_file"))
        # suite.addTest(TestDataLoaderMethods("test_build_knn_graph"))
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()



