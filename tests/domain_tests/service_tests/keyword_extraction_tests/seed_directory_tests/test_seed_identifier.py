import sys
import os
import time
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'data')
REPORT_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'report')

from wedc.domain.service.data.base import *
from wedc.domain.service.keyword_extraction.word2vec import base
from wedc.domain.service.keyword_extraction.seeds import seed_identifier
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
                f.write('\npredict result: ')
                f.write('\n---------------------------------------------------------\n')
                f.write(str(ans))
                f.write('\n\n\n\n')

    def test_generate_label(self):
        from wedc.domain.service.keyword_extraction.seeds import seed_word
        from wedc.domain.service.keyword_extraction.seeds import seed_dict
        from wedc.domain.vendor.nltk import stem

        category = ['others','job_ads', 'massage', 'escort']

        label_from_seeds_filename = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'label_from_seeds'))
        # posts = es_loader.load(posts_file)
        posts = []
        dataset = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'text'))
        with open(dataset, 'r') as pf:
            for line in pf:
                posts.append(line.strip())

        seeds = seed_word.load_seed_similar_words(level=2)
        # print seeds
        sdict = seed_dict.build_sd_with_similar_seeds(level=2)

        with open(label_from_seeds_filename, 'w') as f:
            for post in posts:
                if not post:
                    continue
                judge_dict = {}
                for (word, cates) in sdict.items():
                    if stem.stemming(word) in post.split(' ') and word != ' ':
                        for cate in cates:
                            judge_dict.setdefault(cate, 0)
                            judge_dict[cate] += 1
                            
                if not len(judge_dict.values()):
                    f.write('0\n')
                    continue
                max_value = max(judge_dict.values())
                ans = [cate for (cate, count) in judge_dict.items() if count == max_value]
                
                if len(ans) == 1:
                    for i in range(1, 4):
                        if ans[0] == category[i]:
                            f.write(str(i)+'\n')
                else:
                    f.write('0\n')
                # break
                

    def tearDown(self):
        pass

if __name__ == '__main__':
    def run_main_test():
        suite = unittest.TestSuite()
        # suite.addTest(TestDataLoaderMethods("test_identify_post"))
        # suite.addTest(TestDataLoaderMethods("test_identify_posts"))
        suite.addTest(TestDataLoaderMethods("test_generate_label"))
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()