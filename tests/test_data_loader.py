import sys
import os
import time
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


from wedc.domain.core.data import loader
from wedc.domain.core.data.loaders import es_loader
from wedc.domain.core.data import cleaner

data_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'san-francisco-maria-2.json'))
text_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'text'))

class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        filename = 'san-francisco-maria-2.json'
        self.path = os.path.join(TEST_DATA_DIR, filename)        
        
    def test_data_loader(self):
        start_time = time.time()
        posts = loader.load_data(data_, no_dups=False)
        input_file = open(text_, 'w')
        input_file.writelines(posts)

        posts = cleaner.remove_dups(posts)
        origin_back_file = open(text_+'_bk', 'w')
        origin_back_file.writelines(posts)

        print 'Total posts: ', len(posts)
        print 'Time cost:', (time.time() - start_time), 'seconds'
        self.assertIsNotNone(posts)
        # Total posts:  19970
        # Time cost: 634.690217018 seconds

    def test_load_post(self):
        """ test load post by post id

        post id is start from 1
        """
        post_id = 60        
        text, post = loader.load_data_by_post_id(self.path, post_id-1)

        print 'original post content:\n', text.encode('ascii', 'ignore'), '\n\n'
        print 'post content after preprocessing:\n', post.body, '\n\n'

    def test_json_data_extraction(self):
        import json
        pn_file = open(self.path, 'rU')
        raw = json.load(pn_file)
        pn_file.close()

        post_id = 7975
        hits = raw['hits']['hits']
        post = hits[post_id]['_source']['hasBodyPart']['text']
        print post

    def test_json_data_contain(self):
        import json
        pn_file = open(self.path, 'rU')
        raw = json.load(pn_file)
        pn_file.close()

        target = 'massage'
        hits = raw['hits']['hits']
        post_id = 4
        for hit in hits:
            post_id += 1
            source = hit['_source']
            if 'hasBodyPart' not in source:
                continue

            text =  source['hasBodyPart']['text']
            if target in text:
                print 'post line number', post_id

    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()
    def run_main_test():
        suite = unittest.TestSuite()
        # suite.addTest(TestDataLoaderMethods("test_json_data_contain"))
        suite.addTest(TestDataLoaderMethods("test_data_loader"))
        # suite.addTest(TestDataLoaderMethods("test_load_post"))
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()