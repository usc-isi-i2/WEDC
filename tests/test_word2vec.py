""" Test word2vec

Example:
http://nbviewer.jupyter.org/github/danielfrg/word2vec/blob/master/examples/word2vec.ipynb#

"""


import sys
import os
import unittest
import tempfile
import word2vec

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

from wedc.domain.service.data.base import *
from wedc.domain.service.keyword_extraction.base import *

class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        # load data
        # filename = 'san-francisco-maria.json'
        # path = os.path.join(TEST_DATA_DIR, filename)
        # self.posts = load_by_path(path)
        self.posts = ['ss', 'ss']

        # load path
        directory_name = tempfile.mkdtemp()
        self.from_file = tempfile.NamedTemporaryFile(suffix='', 
                                   prefix='w2v_', 
                                   dir=directory_name,
                                   )
        self.to_file = tempfile.NamedTemporaryFile(suffix='', 
                                   prefix='w2v_', 
                                   dir=directory_name,
                                   )
        
        posts = [str(_) for _ in self.posts]
        print self.posts[0:1]
        self.from_file.writelines(posts)
        # print self.from_file.read()
        print 'gettempdir():', tempfile.gettempdir()
        print self.from_file.name


        
    def test_word2vec(self):
        # word2vec.word2phrase(self.from_file.name, self.to_file.name, verbose=True)
        # print 'gettempdir():', self.to_file.gettempdir()
        pass
        
        
    def tearDown(self):
        self.from_file.close()
        self.to_file.close()

if __name__ == '__main__':
    unittest.main()