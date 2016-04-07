import sys
import os
import time
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'data')

from wedc.domain.service.keyword_extraction.seed_directory import seed_word


class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_seed_files(self):
        print seed_word.get_seed_files()

    def test_load_seed_words(self):
        print seed_word.load_seed_words()

    def tearDown(self):
        pass

if __name__ == '__main__':
    def run_main_test():
        suite = unittest.TestSuite()
        suite.addTest(TestDataLoaderMethods("test_load_seed_words"))
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()