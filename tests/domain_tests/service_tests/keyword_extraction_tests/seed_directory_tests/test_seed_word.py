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
        print seed_word.load_all_seed_words()
        # print seed_word.load_seed_words()

    def test_load_seed_similar_words(self):
        original_seed_similar_words = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'original_seed_similar_words'))
        seed_word.load_seed_similar_words(level=2)

    def test_adjust_weight(self):
        # departed
        
        # import word2vec
        # import time
        # start_time = time.time()
        # load google_news_model_bin costs 169.9s
        # other_word2vec_model = word2vec.load(google_news_model_bin)
        
        # print base.word2vec_model
        # seed_dict = seed_word.load_seed_similar_words(level=2)  # cost 0.87s
        # print 'time cost:', time.time() - start_time

        seed_dict = seed_word.load_seed_similar_words(level=2)
        print seed_word.adjust_weight(seed_dict, google_news_model_bin)


    def test_cache_seed_similar_words_original(self):
        original_seed_similar_words = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'original_seed_similar_words'))
        seed_word.cache_seed_similar_words(base.word2vec_model, level=2, path=original_seed_similar_words)
    
    def test_cache_seed_similar_words_gn(self):

        import word2vec

        google_new_seed_similar_words = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'google_new_seed_similar_words'))
        other_word2vec_model = word2vec.load(google_news_model_bin)
        seed_words = seed_word.load_all_seed_words()
        # print seed_words
        seed_word.cache_seed_similar_words(other_word2vec_model, seed_words, level=2, path=google_new_seed_similar_words)


    def test_generate_weighted_seed_dict(self):
        original_seed_similar_words = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'original_seed_similar_words'))
        google_new_seed_similar_words = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'google_new_seed_similar_words'))
        print seed_word.generate_weighted_seed_dict(original_seed_similar_words, google_new_seed_similar_words)



    def tearDown(self):
        pass

if __name__ == '__main__':
    def run_main_test():
        suite = unittest.TestSuite()
        suite.addTest(TestDataLoaderMethods("test_load_seed_words"))
        # suite.addTest(TestDataLoaderMethods("test_load_seed_similar_words"))
        # suite.addTest(TestDataLoaderMethods("test_cache_seed_similar_words_original"))
        # suite.addTest(TestDataLoaderMethods("test_cache_seed_similar_words_gn"))
        # suite.addTest(TestDataLoaderMethods("test_generate_weighted_seed_dict"))

        
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()