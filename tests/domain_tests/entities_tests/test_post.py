import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data')

from wedc.domain.entities import post


class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        filename = 'san-francisco-maria-2.json'
        self.path = os.path.join(TEST_DATA_DIR, filename)

    def test_remove_url(self):
        self.assertEquals(post.remove_url('something.ad'), '')
        self.assertEquals(post.remove_url('something.com'), '')
        self.assertEquals(post.remove_url('http://something.ad'), '')
        self.assertEquals(post.remove_url('https://something.ad'), '')

    def test_has_url(self):
        self.assertTrue(post.has_url('locumtenens.com is looking for a gastroenterologist in california , not far from san francisco .'))

    def test_post_parser(self):
        import json
        pn_file = open(self.path, 'rU')
        raw = json.load(pn_file)
        pn_file.close()

        target_post_id = 1207
        hits = raw['hits']['hits']
        post_body = hits[target_post_id]['_source']['hasBodyPart']['text']
        print 'post before process\n', post_body.encode('ascii', 'ignore'), '\n\n'
        p = post.Post('', '', post_body)
        print 'post after process\n', p.body, '\n\n'

        
    def tearDown(self):
        pass

if __name__ == '__main__':
    def run_main_test():
        suite = unittest.TestSuite()
        suite.addTest(TestDataLoaderMethods("test_post_parser"))
        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()