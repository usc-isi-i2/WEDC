import sys
import os
import time
import unittest

from test_data_loader import TestDataLoaderMethods
from test_seed_word import TestSeedWordMethods
from test_word2vec import TestWord2VecMethods
from test_post_vector import TestPostVectorMethods
from test_label_propagation import TestLabelPropagationMethods

if __name__ == '__main__':
    # unittest.main()
    def run_main_test():
        suite = unittest.TestSuite() 

        # required
        # suite.addTest(TestDataLoaderMethods("test_data_loader"))
        # suite.addTest(TestWord2VecMethods("test_setup_model"))
        # suite.addTest(TestSeedWordMethods("test_cache_seed_similar_words_original"))
        # suite.addTest(TestSeedWordMethods("test_generate_weighted_seed_dict"))
        # suite.addTest(TestPostVectorMethods("test_post2sv"))
        # suite.addTest(TestPostVectorMethods("test_post2seeds")) # for test

        # lp
        suite.addTest(TestLabelPropagationMethods("test_do_label_propagation"))


        runner = unittest.TextTestRunner()
        runner.run(suite)
    run_main_test() 