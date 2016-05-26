""" Test word2vec

Example:
http://nbviewer.jupyter.org/github/danielfrg/word2vec/blob/master/examples/doc2vec.ipynb
http://nbviewer.jupyter.org/github/danielfrg/word2vec/blob/master/examples/word2vec.ipynb

"""


import sys
import time
import os
import unittest


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

jsonl_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'jsonlines.jsonl'))
import jsonlines

class TestJSONLINESMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_jsonl(self):
        obj = jsonlines.open(jsonl_, mode='r')
        for i in obj:
            
            # print obj.__next__
        # with open(jsonl_, 'rb') as f:
        #     for line in f.readlines():
        #         line = line.strip()
        #         jq(".").transform(text="42") == 42
        # jq(".[]+1").transform([1, 2, 3], multiple_output=True) == [2, 3, 4]

   
        
    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()
    def run_main_test():
        suite = unittest.TestSuite()

        suite.addTest(TestJSONLINESMethods("test_jsonl"))

        runner = unittest.TextTestRunner()
        runner.run(suite)
    run_main_test()



