import sys
import time
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# text_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'text'))
seeds_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'seeds'))
labelled_data_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'labelled_data'))


from wedc.infrastructure import database
from wedc.infrastructure.model.labelled_data import LabelledData
from wedc.infrastructure.model.need_to_label_data import NeedToLabelData
from wedc.infrastructure.model.seed_dict import SeedDict

class TestDatabaseMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_create_database(self):
        database.create_database()

    def test_drop_database(self):
        database.drop_database()

    def tearDown(self):
        pass

class TestLabelledDataMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_insert_data(self):
        LabelledData.insert(content='test_content', label=1, flag=2)

    def test_insert_from_csv(self):
        csv_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'groundtruth.csv'))
        LabelledData.insert_from_csv(csv_)

    def test_load_data(self):
        for idx, data in enumerate(LabelledData.load_data()):
            post_id = idx + 1
            # print data.label, data.content
            print post_id, data.label, data.extraction

    def test_clear_data(self):
        print LabelledData.clear_data()

    def test_load_potential_seeds(self):
        potential_seeds = LabelledData.load_potential_seeds()
        for seed, vec in potential_seeds.items():
            weight = vec[0]
            label = vec[1]
            SeedDict.insert(seed, weight)

    def test_generate_labelled_data_file(self):
        LabelledData.generate_labelled_data_file(labelled_data_)

    def test_load_labelled_data_file(self):
        print LabelledData.load_labelled_data_file(labelled_data_)[0]


    def tearDown(self):
        pass

class TestSeedDictMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_insert_from_txt(self):
        txt_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'weighted_seed_dict'))
        SeedDict.insert_from_txt(txt_)

    def test_load_data(self):
        seeds = SeedDict.load_data()
        for seed, weight in seeds.items():
            print seed, weight
        print len(seeds)
            
    def test_clear_data(self):
        print SeedDict.clear_data()

    def test_generate_seed_file(self):
        SeedDict.generate_seed_file(seeds_)

    def test_load_seed_file(self):
        print SeedDict.load_seed_file(seeds_)
        

    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()

    def run_main_test():
        suite = unittest.TestSuite()
        # suite.addTest(TestDatabaseMethods("test_create_database"))
        # suite.addTest(TestDatabaseMethods("test_drop_database"))
    
        # suite.addTest(TestLabelledDataMethods("test_insert_data"))
        # suite.addTest(TestLabelledDataMethods("test_insert_from_csv"))
        # suite.addTest(TestLabelledDataMethods("test_load_data"))
        # suite.addTest(TestLabelledDataMethods("test_clear_data"))
        # suite.addTest(TestLabelledDataMethods("test_load_potential_seeds"))
        # suite.addTest(TestLabelledDataMethods("test_generate_labelled_data_file"))
        suite.addTest(TestLabelledDataMethods("test_load_labelled_data_file"))
        
        # suite.addTest(TestSeedDictMethods("test_insert_from_txt"))
        # suite.addTest(TestSeedDictMethods("test_load_data"))
        # suite.addTest(TestSeedDictMethods("test_clear_data"))
        # suite.addTest(TestSeedDictMethods("test_generate_seed_file"))
        # suite.addTest(TestSeedDictMethods("test_load_seed_file"))

        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()



