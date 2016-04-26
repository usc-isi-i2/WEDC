
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


    #############################################
    #   Test Stemming
    #############################################

    def test_stemming_be(self):
        in_word = 'was'
        out_word = stem.stemming(in_word)
        assert out_word == 'be'
        print in_word, ' : ', out_word

    def test_stemming_dns(self):
        """ Test Stemming for words contain digits and string
        """
        in_word = '401k'
        out_word = stem.stemming(in_word)
        # assert in_word == out_word
        print in_word, ' : ', out_word

    def test_sentence(self):
        in_word = 'source incall physicians phoneno'
        out_word = stem.stemming(in_word)
        print in_word, ' : ', out_word

    def test_custom_word(self):
        in_word = 'san'
        out_word = stem.stemming(in_word)
        # assert in_word == out_word
        print in_word, ' : ', out_word

    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()
    
    def run_main_test():
        suite = unittest.TestSuite()
        suite.addTest(TestDataLoaderMethods("test_custom_word"))

        runner = unittest.TextTestRunner()
        runner.run(suite)
    run_main_test()





