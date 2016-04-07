import sys
import os
import time
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'data')

from wedc.domain.service.keyword_extraction.seed_directory import seed_dict

output_bin = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'vectors.bin'))

class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_build_seed_dict(self):
        start_time = time.time()
        seed_dict.build_seed_dict(output_bin)
        print 'Time cost:', (time.time() - start_time), 'seconds'


    def tearDown(self):
        pass

if __name__ == '__main__':
    def run_main_test():
        suite = unittest.TestSuite()
        suite.addTest(TestDataLoaderMethods("test_build_seed_dict"))
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()