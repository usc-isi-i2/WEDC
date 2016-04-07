import sys
import os
import time
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'data')
REPORT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'report')

from wedc.domain.service.data.base import *
from wedc.domain.service.keyword_extraction.word2vec import base
from wedc.domain.service.keyword_extraction.seed_directory import seed_identifier
from wedc.domain.entities.post import Post
from wedc.domain.service.data.loaders import es_loader


output_bin = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'vectors.bin'))
posts_file = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'san-francisco-maria-2.json'))


class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        base.load_word2vec_model(output_bin)
        self.word2vec_model = base.word2vec_model



    def test_identify_post(self):
        post_id = 12
        text, post = es_loader.load_post(posts_file, post_id)
        print 'original post content:\n', text, '\n\n'
        print 'post content after preprocessing:\n', post.body, '\n\n'

        ans = seed_identifier.identify_post(post)
        print 'predict result: ', ans

    def test_identify_posts(self):
        import numpy as np
        report_file = os.path.expanduser(os.path.join(REPORT_DIR, 'identification_by_seeds'))
        post_ids = np.random.choice(20000, 10, replace=False)

        with open(report_file, 'w') as f:
            # print 'posts used for this report (post_id shown below):\n', post_ids
            f.write('posts used for this report (post_id shown below):\n')
            f.write(str(post_ids))
            f.write('\n\n')

            for post_id in post_ids:
                f.write('\n#######################################################\n')
                f.write('# POST ID: ' + str(post_id))                
                f.write('\n#######################################################\n')

                text, post = es_loader.load_post(posts_file, post_id)
                # print 'original post content:\n', text, '\n\n'
                f.write('\noriginal post content:')
                f.write('\n---------------------------------------------------------\n')
                f.write(text.encode('ascii', 'ignore'))
                f.write('\n\n')
                
                # print 'post content after preprocessing:\n', post.body, '\n\n'
                f.write('\npost content after preprocessing:')
                f.write('\n---------------------------------------------------------\n')
                f.write(post.body)
                f.write('\n\n')

                ans = seed_identifier.identify_post(post)
                # print 'predict result: ', ans
                f.write('predict result: ')
                f.write(str(ans))
                f.write('\n\n\n\n')



    def tearDown(self):
        pass

if __name__ == '__main__':
    def run_main_test():
        suite = unittest.TestSuite()
        # suite.addTest(TestDataLoaderMethods("test_identify_post"))
        suite.addTest(TestDataLoaderMethods("test_identify_posts"))
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()