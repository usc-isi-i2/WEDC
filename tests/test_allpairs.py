"""
https://pypi.python.org/pypi/pyallpairs/0.1.0
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
# ap_input = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'ap_vectors.bin'))
# ap_input = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'dblp_le.bin'))
ap_input = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'somefile.bin'))


class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_ap_format(self):
        """ AllPairs Input Format
        
        <record id> <number of features> <fid 1> <fid 2> ... <fid n>
        """
        input_file = open(ap_input, 'wb')
        with open(word2vec_output) as f:
            lines = f.readlines()

        word_size, vector_size = lines[0].split()

        for line in lines[1:]:
            line = line.split()
            line.insert(1, vector_size)
            input_file.write(' '.join(line) + '\n')
            
        input_file.close()


    def test_allpairs(self):
        ap = allpairs.AllPairs()
        data = allpairs.DataSourceIterator_Get(ap_input)
        ans = ap.FindAllSimilarPairs(.1, data, 600000, 120000000)
        
        if not ans:
            print data.GetErrorMessage()
            return 
        
        print 'found ' + str(ap.SimilarPairsCount()) + ' similar pairs'
        # print 'Candidates considered: ' + str(ap.CandidatesConsidered())
        # print '\n'
        # print 'Vector intersections performed:'
        # print ap.IntersectionsPerformed()


    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()
    def run_main_test():
        suite = unittest.TestSuite()

        # suite.addTest(TestDataLoaderMethods("test_ap_format"))
        suite.addTest(TestDataLoaderMethods("test_allpairs"))
        
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()


