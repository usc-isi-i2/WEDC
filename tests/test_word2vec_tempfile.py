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
        filename = 'san-francisco-maria.json'
        path = os.path.join(TEST_DATA_DIR, filename)
        self.posts = load_by_path(path)

        # load path
        directory_name = tempfile.mkdtemp()
        self.from_file = tempfile.NamedTemporaryFile(suffix='', 
                                   prefix='w2v_', 
                                   mode='w',
                                   delete=False,
                                   dir=directory_name
                                   )
        self.to_file = tempfile.NamedTemporaryFile(suffix='', 
                                   prefix ='w2v_', 
                                   mode='w',
                                   delete=False,
                                   dir=directory_name,
                                   )
        print self.posts[0]
        try:
            self.from_file.writelines(self.posts)
        except Exception as e: 
            print "ERROR: " + str(e)

        # self.posts = [' '.join(post) for post in self.posts]
        # self.from_file.writelines("%s\n" % l for l in self.posts)
        # self.from_file.seek(0)
        # print 'read: '+self.from_file.read()
        # print 'gettempdir():', tempfile.gettempdir()
        print 'from_file: '+self.from_file.name


    def test_word2vec(self):
        # word2vec.word2phrase(self.from_file.name, self.to_file.name, verbose=True)
        word2vec.word2vec(self.from_file.name, self.to_file.name, verbose=True)
        model = word2vec.load(self.to_file.name)
        print model.vocab
        # print 'gettempdir():', self.to_file.gettempdir()
        
        
        
    def tearDown(self):
        self.from_file.close()
        self.to_file.close()

if __name__ == '__main__':
    unittest.main()