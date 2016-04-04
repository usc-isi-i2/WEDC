""" Test word2vec

Example:
http://nbviewer.jupyter.org/github/danielfrg/word2vec/blob/master/examples/word2vec.ipynb#

"""


import sys
import os
import unittest
import word2vec


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

input_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'text'))
output_phrases = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'text-phrases.txt'))
output_clusters = os.path.expanduser(os.path.join(TEST_DATA_DIR,'text-clusters.txt'))
output_bin = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'vectors.bin'))
output_txt = os.path.expanduser(os.path.join(TEST_DATA_DIR,'vectors.txt'))

from wedc.domain.service.data.base import *
from wedc.domain.service.keyword_extraction.base import *

class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        # load data
        filename = 'san-francisco-maria.json'
        path = os.path.join(TEST_DATA_DIR, filename)
        posts = load_by_path(path)

        input_file = open(input_, 'w')
        input_file.writelines(posts)

    # """ set up model
    def test_setup_model(self):
        # word2vec.word2phrase(input_, output_phrases, verbose=True)
        word2vec.word2vec(input_, output_bin, size=300, binary=1, verbose=False)
        word2vec.word2vec(input_, output_txt, size=10, binary=0, verbose=False)
        # word2vec.word2clusters(input_, output_clusters, 10, verbose=True)
    # """

    def test_files_create(self):
        # assert os.path.exists(output_phrases)
        # assert os.path.exists(output_clusters)
        assert os.path.exists(output_bin)
        # assert os.path.exists(output_txt)
    
    def test_load_bin(self):
        model = word2vec.load(output_bin)
        vocab = model.vocab
        vectors = model.vectors
        # print vectors

        assert vectors.shape[0] == vocab.shape[0]
        assert vectors.shape[0] > 3000
        assert vectors.shape[1] == 10

    """
    def test_load_txt(self):
        model = word2vec.load(output_txt)
        vocab = model.vocab
        vectors = model.vectors

        assert vectors.shape[0] == vocab.shape[0]
        assert vectors.shape[0] > 3000
        assert vectors.shape[1] == 10
    """

    def test_prediction(self):
        model = word2vec.load(output_bin)
        indexes, metrics = model.cosine('the')
        assert indexes.shape == (10,)
        assert indexes.shape == metrics.shape

        py_response = model.generate_response(indexes, metrics).tolist()
        assert len(py_response) == 10
        assert len(py_response[0]) == 2

    """
    def test_analogy(self):
        model = word2vec.load(output_txt)
        indexes, metrics = model.analogy(pos=['the', 'the'], neg=['the'], n=20)
        assert indexes.shape == (20,)
        assert indexes.shape == metrics.shape

        py_response = model.generate_response(indexes, metrics).tolist()
        assert len(py_response) == 20
        assert len(py_response[0]) == 2
    """

    def test_word2vec(self):
        pass
        
        
        
    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()
    
    def run_model_test():
        suite = unittest.TestSuite()
        suite.addTest(TestDataLoaderMethods("test_setup_model"))
        runner = unittest.TextTestRunner()
        runner.run(suite)

    def run_other_test():
        suite = unittest.TestSuite()
        suite.addTest(TestDataLoaderMethods("test_load_bin"))
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_model_test()



