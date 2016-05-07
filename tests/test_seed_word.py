import sys
import os
import time
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

from wedc.domain.vendor.word2vec import w2v
from wedc.domain.core.data.seed import seed_word

word2vec_model_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'word2vec_model.bin'))
google_news_word2vec_model_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'GoogleNews-vectors-negative300.bin'))
original_seed_similar_words_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'original_seed_similar_words'))
google_news_similar_words_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'google_new_seed_similar_words'))

class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        w2v.word2vec_model = w2v.load_model(word2vec_model_)

    def test_get_seed_files(self):
        print seed_word.get_seed_files()

    def test_load_seed_words(self):
        print seed_word.load_seed_words()

    def test_load_seed_similar_words(self):
        seed_word.load_seed_similar_words(level=2)

    def test_cache_seed_similar_words_original(self):
        seed_word.cache_seed_similar_words(path=original_seed_similar_words_, level=1)
    
    def test_cache_seed_similar_words_gn(self):
        google_news_word2vec_model = w2v.load_model(google_news_word2vec_model_)
        # seed_words = seed_word.load_seed_words()
        seed_word.cache_seed_similar_words(path=google_new_seed_similar_words, model=google_news_word2vec_model, level=2)

    def test_generate_weighted_seed_dict(self):
        print seed_word.generate_weighted_seed_dict(original_seed_similar_words_, google_news_similar_words_)

    def tearDown(self):
        pass

if __name__ == '__main__':
    def run_main_test():
        suite = unittest.TestSuite()

        # suite.addTest(TestDataLoaderMethods("test_get_seed_files"))
        # suite.addTest(TestDataLoaderMethods("test_load_seed_words"))
        # suite.addTest(TestDataLoaderMethods("test_load_seed_similar_words"))
        # suite.addTest(TestDataLoaderMethods("test_cache_seed_similar_words_original"))
        # suite.addTest(TestDataLoaderMethods("test_cache_seed_similar_words_gn"))
        # suite.addTest(TestDataLoaderMethods("test_generate_weighted_seed_dict"))

        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()