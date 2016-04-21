import sys
import os
import time
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'data')

from wedc.domain.service.keyword_extraction.seeds import seed_word
from wedc.domain.service.keyword_extraction.word2vec import similarity
from wedc.domain.service.keyword_extraction.word2vec import base

output_bin = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'vectors.bin'))
google_news_model_bin = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'GoogleNews-vectors-negative300.bin'))



class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        base.load_word2vec_model(output_bin)

    def test_get_seed_files(self):
        print seed_word.get_seed_files()

    def test_load_seed_words(self):
        print seed_word.load_seed_words()

    def test_load_seed_similar_words(self):
        print seed_word.load_seed_similar_words(level=2)

    def test_adjust_weight(self):
        seed_dict = seed_word.load_seed_similar_words(level=2)
        print seed_word.adjust_weight(seed_dict, google_news_model_bin)

    def tearDown(self):
        pass

if __name__ == '__main__':
    def run_main_test():
        suite = unittest.TestSuite()
        # suite.addTest(TestDataLoaderMethods("test_load_seed_words"))
        # suite.addTest(TestDataLoaderMethods("test_load_seed_similar_words"))
        suite.addTest(TestDataLoaderMethods("test_adjust_weight"))
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()