""" Test word2vec

Example:
http://nbviewer.jupyter.org/github/danielfrg/word2vec/blob/master/examples/doc2vec.ipynb
http://nbviewer.jupyter.org/github/danielfrg/word2vec/blob/master/examples/word2vec.ipynb

"""


import sys
import time
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
        pass
        # filename = 'san-francisco-maria.json'
        # path = os.path.join(TEST_DATA_DIR, filename)
        # posts = load_by_path(path)

        # input_file = open(input_, 'w')
        # input_file.writelines(posts)

    # """ set up model
    def test_setup_model(self):
        # word2vec.word2phrase(input_, output_phrases, verbose=True)
        
        # word2vec.word2vec(input_, output_bin, size=300, binary=1, verbose=False)
        word2vec.word2vec(input_, output_bin, binary=1, cbow=0, size=100, window=10, negative=5, hs=0, threads=12, iter_=5, min_count=5, verbose=False)

        # word2vec.word2vec(input_, output_txt, size=10, binary=0, verbose=False)
        # word2vec.word2vec(input_, output_txt, binary=0, cbow=0, size=300, window=10, negative=5, hs=0, threads=12, iter_=20, min_count=5, verbose=False)
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
        print model.vocab
        print model.vectors.shape

        assert vectors.shape[0] == vocab.shape[0]
        # assert vectors.shape[0] > 3000
        # assert vectors.shape[1] == 10

    """
    def test_load_txt(self):
        model = word2vec.load(output_txt)
        vocab = model.vocab
        vectors = model.vectors

        print model.vocab

        assert vectors.shape[0] == vocab.shape[0]
        # assert vectors.shape[0] > 3000
        # assert vectors.shape[1] == 10
        
    def test_prediction(self):
        model = word2vec.load(output_bin)
        indexes, metrics = model.cosine('the')
        assert indexes.shape == (10,)
        assert indexes.shape == metrics.shape

        py_response = model.generate_response(indexes, metrics).tolist()
        assert len(py_response) == 10
        assert len(py_response[0]) == 2
    
    def test_analogy(self):
        model = word2vec.load(output_txt)
        indexes, metrics = model.analogy(pos=['the', 'the'], neg=['the'], n=20)
        assert indexes.shape == (20,)
        assert indexes.shape == metrics.shape

        py_response = model.generate_response(indexes, metrics).tolist()
        assert len(py_response) == 20
        assert len(py_response[0]) == 2
    """

    def test_similarity(self):
        start_time = time.time()
        model = word2vec.load(output_bin)
        num_of_words, num_of_features = model.vectors.shape
        for i in range(num_of_words):
            word = model.vocab[i]
            indexes, metrics = model.cosine(word)
            # print model.vocab[indexes]    # similar words
        print 'Number of words:', num_of_words
        print 'Time cost:', (time.time() - start_time), 'seconds'
        # Number of words: 6051
        # Time cost: 4.86683392525 seconds
    
    def test_word(self):
        model = word2vec.load(output_bin)
        num_of_words, num_of_features = model.vectors.shape

        indexes, metrics = model.cosine('massag')
        print model.vocab[indexes]    # similar words
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
        # suite.addTest(TestDataLoaderMethods("test_setup_model"))
        # suite.addTest(TestDataLoaderMethods("test_load_bin"))
        # suite.addTest(TestDataLoaderMethods("test_similarity"))
        suite.addTest(TestDataLoaderMethods("test_word"))
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_other_test()



