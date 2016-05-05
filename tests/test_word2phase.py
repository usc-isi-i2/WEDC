

import sys
import time
import os
import unittest


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

input_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'word2phase_input'))
output_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'word2phase_output'))

import word2vec


class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test(self):
        word2vec.word2phrase(input_, output_, verbose=True)



    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()

    def run_main_test():
        suite = unittest.TestSuite()
        suite.addTest(TestDataLoaderMethods("test"))
        
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()



