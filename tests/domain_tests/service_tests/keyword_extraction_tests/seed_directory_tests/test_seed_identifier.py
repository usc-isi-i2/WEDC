import sys
import os
import time
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'data')

from wedc.domain.service.data.base import *
from wedc.domain.service.keyword_extraction.word2vec import base
from wedc.domain.service.keyword_extraction.seed_directory import seed_identifier
from wedc.domain.entities.post import Post


output_bin = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'vectors.bin'))
posts_file = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'san-francisco-maria-2.json'))

class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        base.load_word2vec_model(output_bin)
        self.word2vec_model = base.word2vec_model



    def test_identify_post(self):
        import json
        pn_file = open(posts_file, 'rU')
        raw = json.load(pn_file)
        pn_file.close()

        post_id = 12
        post_content = hits = raw['hits']['hits']
        source = hits[post_id]['_source']
        if 'hasBodyPart' not in source:
            return
        text =  source['hasBodyPart']['text']
        print 'original text:\n\n', text, '\n\n'
        post = Post('', '', text)

        seed_identifier.identify_post(post)

    def tearDown(self):
        pass

if __name__ == '__main__':
    def run_main_test():
        suite = unittest.TestSuite()
        suite.addTest(TestDataLoaderMethods("test_identify_post"))
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()