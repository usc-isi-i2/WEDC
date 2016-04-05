"""
https://github.com/phoenix24/google-all-pairs-similarity-search
http://atmarkplant.com/install-swig-for-mac-os-x/
"""

import sys
import os
import unittest
import allpairs

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

word2vec_output = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'vectors.txt'))
ap_input = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'ap_vectors.txt'))


class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_ap_format(self):
        """ AllPairs Input Format
        
        <record id> <number of features> <fid 1> <fid 2> ... <fid n>
        """
        input_file = open(ap_input, 'w')
        with open(word2vec_output) as f:
            lines = f.readlines()

        word_size, vector_size = lines[0].split()

        for line in lines[1:]:
            line = line.split()
            # word = line[0]
            # vectors = ' '.join(line[1:])
            line.insert(1, vector_size)
            input_file.write(' '.join(line))


        
    # def test_word2vec(self):
    #     allpairs.DataSourceIterator_Get()

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()



