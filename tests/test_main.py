


import sys
import time
import os
import unittest
import word2vec


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

from wedc.domain.service.keyword_extraction.seeds import seed_word
from wedc.domain.service.keyword_extraction.word2vec import similarity

from wedc.domain.vendor.nltk import stem
from wedc.domain.service.keyword_extraction.seeds import post2sv

raw_data = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'san-francisco-maria-2.json'))
input_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'text'))
output_phrases = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'text-phrases.txt'))
output_clusters = os.path.expanduser(os.path.join(TEST_DATA_DIR,'text-clusters.txt'))
output_bin = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'vectors.bin'))
output_txt = os.path.expanduser(os.path.join(TEST_DATA_DIR,'vectors.txt'))
google_news_model_bin = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'GoogleNews-vectors-negative300.bin'))
original_seed_similar_words = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'original_seed_similar_words'))
google_new_seed_similar_words = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'google_new_seed_similar_words'))
output_post2vec = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'post_vec.txt'))

output_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'graph.txt'))

class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_setup_input(self):
        posts = load_by_path(raw_data)
        input_file = open(input_, 'w')
        input_file.writelines(posts)

    def test_setup_model(self):
        word2vec.word2vec(input_, output_bin, binary=1, cbow=0, size=300, window=10, negative=5, hs=0, threads=12, iter_=5, min_count=5, verbose=False)

    def test_cache_seed_similar_words_original(self):
        seed_word.cache_seed_similar_words(base.word2vec_model, level=2, path=original_seed_similar_words)
    
    def test_cache_seed_similar_words_gn(self):
        other_word2vec_model = word2vec.load(google_news_model_bin)
        seed_words = seed_word.load_all_seed_words()
        seed_word.cache_seed_similar_words(other_word2vec_model, seed_words, level=2, path=google_new_seed_similar_words)

    def test_post2sv_weighted(self):
        from wedc.domain.service.keyword_extraction.word2vec import base
        base.load_word2vec_model(output_bin)
        seeds = seed_word.generate_weighted_seed_dict(original_seed_similar_words, google_new_seed_similar_words)
        post2sv.post2sv_weighted(input_, output_post2vec, seeds)

    def test_build_knn_graph(self):
        knn_graph.build_graph(output_post2vec, output_)
        
    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()

    def run_main_test():
        suite = unittest.TestSuite()
       
        # suite.addTest(TestDataLoaderMethods("test_setup_input"))
        # suite.addTest(TestDataLoaderMethods("test_setup_model"))
        # suite.addTest(TestDataLoaderMethods("test_cache_seed_similar_words_original"))
        # suite.addTest(TestDataLoaderMethods("test_cache_seed_similar_words_gn"))
        suite.addTest(TestDataLoaderMethods("test_post2sv_weighted"))
        # suite.addTest(TestDataLoaderMethods("test_build_knn_graph"))


        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()



