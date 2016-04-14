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

input_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'post_vec.txt'))
output_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'graph.txt'))

from wedc.domain.service.category_identification.graph import knn_graph 

class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_build_knn_graph(self):
        knn_graph.build_graph(input_, output_)
        
    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()

    def run_main_test():
        suite = unittest.TestSuite()
      
        suite.addTest(TestDataLoaderMethods("test_build_knn_graph"))
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()



