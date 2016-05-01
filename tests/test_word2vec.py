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
input_no_dup = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'text_no_dup'))
# input_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'memex_raw'))
output_phrases = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'text-phrases.txt'))
output_clusters = os.path.expanduser(os.path.join(TEST_DATA_DIR,'text-clusters.txt'))
output_bin = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'vectors.bin'))
output_txt = os.path.expanduser(os.path.join(TEST_DATA_DIR,'vectors.txt'))

from wedc.domain.service.data.base import *
from wedc.domain.service.keyword_extraction.base import *
from wedc.domain.vendor.nltk import stem

class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_setup_input(self):
        # load data
        filename = 'san-francisco-maria-2.json'
        path = os.path.join(TEST_DATA_DIR, filename)
        posts = load_by_path(path)

        input_file = open(input_, 'w')
        input_file.writelines(posts)



    # """ set up model
    def test_setup_model(self):
        # word2vec.word2phrase(input_, output_phrases, verbose=True)
        
        # word2vec.word2vec(input_, output_bin, size=300, binary=1, verbose=False)
        word2vec.word2vec(input_no_dup, output_bin, binary=1, cbow=0, size=300, window=10, negative=5, hs=0, threads=12, iter_=5, min_count=5, verbose=False)

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

    def test_all_similarity(self):
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
    
    def test_word_similiarity(self):
        target_word = stem.stemming('escort')  # "#/h"
        model = word2vec.load(output_bin)

        try:
            indexes, metrics = model.cosine(target_word, n=10)
            similar_words = [str(_) for _ in list(model.vocab[indexes])]    # similar words
            
            # print 'similar words\n', similar_words
            # print 'similarity matrix\n', metrics

            # word:similarity pair
            pairs = [(similar_words[i], metrics[i]) for i in range(len(similar_words))]
            print 'word:similarity pairs\n', pairs

        except Exception:
            print 'NO FOUND'

        
    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()

    def run_main_test():
        suite = unittest.TestSuite()
        # suite.addTest(TestDataLoaderMethods("test_setup_input"))    # 468.220s
        # suite.addTest(TestDataLoaderMethods("test_setup_model"))
        # suite.addTest(TestDataLoaderMethods("test_load_bin"))
        # suite.addTest(TestDataLoaderMethods("test_all_similarity"))
        suite.addTest(TestDataLoaderMethods("test_word_similiarity"))
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()



