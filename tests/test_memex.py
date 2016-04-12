
import sys
import time
import os
import unittest


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

output_file_path = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'memex_raw'))

from wedc.domain.vendor.memex import manager

class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_load_all_data_to_disk(self):
        manager.load_all_data_to_disk(table_name='dig_isi_cdr2_ht_ads_2016', limit=100, output_file_path= output_file_path)
        
    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()

    def run_main_test():
        suite = unittest.TestSuite()
       
        suite.addTest(TestDataLoaderMethods("test_load_all_data_to_disk"))
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()



