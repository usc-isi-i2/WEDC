import sys
import os
import time
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

from wedc.domain.service.data.base import *
from wedc.domain.service.data.loaders import es_loader

class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        filename = 'san-francisco-maria-2.json'
        self.path = os.path.join(TEST_DATA_DIR, filename)
        
    def test_data_loader(self):
        start_time = time.time()
        posts = load_by_path(self.path)
        print 'Total posts: ', len(posts)
        print 'Time cost:', (time.time() - start_time), 'seconds'
        self.assertIsNotNone(posts)
        # print posts
        # Total posts:  49974
        # Time cost: 133.985596895 seconds
        
        # for post in posts:
        #     self.assertFalse(type(post) is list)
            # if type(post) is list:
            #     print post
            #     break

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
        post_id = 0
        for hit in hits:
            post_id += 1
            source = hit['_source']
            if 'hasBodyPart' not in source:
                continue

            text =  source['hasBodyPart']['text']
            if target in text:
                print 'post line number', post_id
                # print text
                # break  

    def test_load_post(self):
        # departed solution
        # text = es_loader.load_post(self.path, 0, post_object=False)
        # print text
        # post = es_loader.load_post(self.path, 0, post_object=True)
        # print post.body
        
        post_id = 4444

        post_id = post_id - 1 # only for test graph annotation
        # {'job_ads': 1, 'massage': 2, 'escort': 3,}
        
        text, post = es_loader.load_post(self.path, post_id)
        print 'original post content:\n', text.encode('ascii', 'ignore'), '\n\n'
        print 'post content after preprocessing:\n', post.body, '\n\n'


    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()
    def run_main_test():
        suite = unittest.TestSuite()
        # suite.addTest(TestDataLoaderMethods("test_json_data_contain"))
        suite.addTest(TestDataLoaderMethods("test_load_post"))
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()