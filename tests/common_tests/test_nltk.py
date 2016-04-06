
import sys
import time
import os
import unittest


sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')


from wedc.domain.vendor.nltk import stem


class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_stemming(self):
        in_word = 'was'
        out_word = stem.stemming(in_word)
        print in_word, ' : ', out_word
        
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
    
    # def run_main_test():
    #     pass
    # run_main_test()





