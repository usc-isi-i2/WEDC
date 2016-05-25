import sys
import os
import time
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


from wedc.domain.core.data import loader

data_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'san-francisco-maria-2.json'))
imd_data_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'imd_san-francisco-maria-2.json'))
text_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'text'))
text_nodups2dups_mapping_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'text_mapping'))
raw_posts_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'raw_posts'))
# raw_posts_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'raw_posts_massage'))


class TestDataLoaderMethods(unittest.TestCase):
    def setUp(self):
        filename = 'san-francisco-maria-2.json'
        self.path = os.path.join(TEST_DATA_DIR, filename)  
        self.no_dups = True     

    def test_load(self):
        # loader.load_input(imd_data_)
        loader.generate_compressed_data(imd_data_)
        
    def test_data_loader(self):
        start_time = time.time()
        posts = loader.load_data(data_, text_, no_dups=self.no_dups)

        print 'Total posts: ', len(posts)
        print 'Time cost:', (time.time() - start_time), 'seconds'
        self.assertIsNotNone(posts)
        # Total posts:  19974
        # Time cost: 261.857595921 seconds
    
    def test_mapping(self):
        print loader.load_nodups2dups_mapping(text_nodups2dups_mapping_)

    def test_load_post(self):
        """ test load post by post id
        post id is start from 1
        """
        post_id = 184 # 28 # 16274
        loader.mapping = loader.load_nodups2dups_mapping(text_nodups2dups_mapping_)
        text, post = loader.load_data_by_post_id(self.path, post_id, no_dups=self.no_dups)

        print 'original post content:\n', text.encode('ascii', 'ignore'), '\n\n'
        print 'post content after preprocessing:\n', post.body, '\n\n'

    def test_get_posts_for_token(self):
        token = 'massage'
        post_id_set = []
        target_file = open(text_, 'rb')
        lines = target_file.readlines()
        for idx in range(len(lines)):
            line = lines[idx]
            line = line.strip()
            if token in line and "spa" in line:
                post_id_set.append(idx+1)
        target_file.close()
        print post_id_set

    def test_load_data_by_post_id_set(self):
        # post_id_set = [1114, 18441, 6796, 16703, 9255, 9252, 16833, 1176, 11771, 7183, 875, 871, 8013, 7455, 7450, 10886, 14476, 4728, 2303, 3748, 3747, 3745, 10461, 10397, 16935, 7212, 9751, 8840, 8844, 11842, 695, 8717, 5618, 5610, 11569, 9526, 6776, 6773, 9964, 9962, 12032, 9507, 5057, 10760, 13595, 1158, 1155, 1154, 1152, 8037, 8036, 8523, 8522, 18205, 8536, 13562, 4606, 4607, 4600, 6902, 6900, 8689, 10827, 7948, 7239, 16918, 6231, 6232, 9777, 8864, 811, 7819, 15854, 3029, 15583, 8737, 10573, 5670, 5672, 6751, 230, 4680, 2537, 5385, 11832, 11833, 790, 1138, 1134, 10790, 13777, 7145, 7143, 13779, 8059, 13585, 7496, 11998]
        # post_id_set = [53, 71, 72, 105, 117, 128, 132, 133, 154, 172, 182, 183, 184, 185, 187, 217, 218, 219, 242, 243, 244, 245, 247, 248, 251, 274, 276, 277, 278, 280, 281, 282, 283, 284, 378, 424, 425, 426, 428, 488, 490, 491, 573, 579, 612, 618, 631, 633, 634, 635, 639, 640, 641, 642, 643, 644, 653, 672, 793, 803, 806, 813, 815, 824, 925, 970, 971, 972, 975, 981, 1055, 1272, 1276, 1442, 1471, 1473, 1481, 1489, 1498, 1516, 1528, 1535, 1538, 1605, 1678, 1681, 1691, 1696, 1698, 1699, 1700, 1701, 1702, 1703, 1704, 1708, 1709, 1710, 1712, 1717, 1791, 1809, 1818, 1819, 1841, 1863, 1905, 1912, 1918, 1922, 1924, 1952, 1973, 1990, 1997, 2006, 2043, 2056, 2075, 2087, 2088, 2120, 2121, 2122, 2128, 2159, 2161, 2308, 2334, 2434, 2438, 2459, 2568, 2584, 2595, 2618, 2631, 2633, 2670, 2677, 2712, 2714, 2725, 2733, 2765, 2777, 2814, 2897, 2902, 2907, 3033, 3063, 3173, 3177, 3178, 3179, 3184, 3187, 3192, 3193, 3194, 3195, 3197, 3224, 3250, 3260, 3272, 3277, 3318, 3321, 3346, 3383, 3414, 3442, 3497, 3514, 3516, 3541, 3575, 3628, 3669, 3689, 3708, 3723, 3737, 3797, 3832, 3874, 3875, 3887, 3893, 3956, 4008, 4050, 4053, 4059, 4064, 4071, 4109, 4125, 4142, 4144, 4154, 4167, 4204, 4231, 4241, 4255, 4269, 4283, 4310, 4325, 4339, 4350, 4369, 4403, 4404, 4448, 4454, 4479, 4480, 4488, 4507, 4519, 4537, 4561, 4587, 4593, 4609, 4617, 4634, 4697, 4756, 4769, 4771, 4776, 4778, 4807, 4809, 4828, 4830, 4861, 4880, 4883, 4911, 4915, 4961, 4966, 4971, 4975, 4998, 5002, 5019, 5028, 5047, 5090, 5100, 5106, 5126, 5127, 5143, 5146, 5159, 5188, 5199, 5208, 5212, 5225, 5243, 5252, 5265, 5289, 5294, 5306, 5322, 5362, 5393, 5411, 5418, 5431, 5457, 5458, 5463, 5514, 5519, 5568, 5575, 5596, 5598, 5633, 5678, 5681, 5685, 5699, 5721, 5741, 5833, 5841, 5862, 5925, 6037, 6703, 6751, 6774, 6888, 6891, 6904, 6952, 6957, 6986, 6999, 7004, 7010, 7079, 7088, 7103, 7198, 7224, 7226, 7230, 7231, 7233, 7254, 7259, 7279, 7320, 7356, 7378, 7381, 7384, 7385, 7388, 7402, 7415, 7426, 7438, 7447, 7457, 7462, 7467, 7472, 7490, 7497, 7510, 7511, 7520, 7552, 7562, 7567, 7596, 7601, 7604, 7615, 7631, 7635, 7641, 7652, 7684, 7694, 7696, 7709, 7719, 7721, 7731, 7734, 7738, 7743, 7750, 7769, 7786, 7788, 7792, 7825, 7879, 7882, 7890, 7897, 7918, 7931, 7934, 7938, 7993, 8016, 8029, 8055, 8118, 8119, 8120, 8162, 8171, 8190, 8199, 8204, 8210, 8251, 8253, 8268, 8285, 8289, 8301, 8305, 8318, 8321, 8339, 8340, 8351, 8362, 8399, 8454, 8514, 8520, 8521, 8533, 8548, 8556, 8558, 8560, 8565, 8597, 8617, 8622, 8629, 8634, 8673, 8705, 8725, 8736, 8740, 8769, 8783, 8822, 8829, 8856, 8872, 8917, 8938, 8968, 8997, 9014, 9106, 9113, 9143, 9146, 9163, 9166, 9194, 9206, 9224, 9234, 9244, 9246, 9253, 9257, 9259, 9262, 9275, 9297, 9300, 9312, 9324, 9325, 9332, 9346, 9350, 9360, 9389, 9407, 9429, 9459, 9487, 9499, 9520, 9557, 9564, 9566, 9576, 9581, 9603, 9616, 9622, 9625, 9630, 9658, 9681, 9682, 9683, 9711, 9755, 9770, 9790, 9817, 9818, 9827, 9844, 9871, 9872, 9885, 9887, 9917, 9919, 9939, 9951, 9964, 9966, 9979, 9981, 9983, 9989, 9992, 10003, 10012, 10018, 10044, 10049, 10091, 10108, 10109, 10144, 10155, 10162, 10168, 10195, 10243, 10267, 10268, 10320, 10324, 10343, 10346, 10348, 10349, 10674, 10701, 10734, 10787, 10840, 10883, 10916, 10918, 10968, 11047, 11063, 11079, 11086, 11088, 11089, 11099, 11196, 11236, 11243, 11298, 11302, 11317, 11378, 11388, 11396, 11457, 11488, 11551, 11604, 11641, 11685, 11727, 11750, 11752, 11755, 11788, 11795, 11835, 11870, 12035, 12075, 12076, 12086, 12124, 12214, 12264, 12318, 13040, 13463, 13585, 13660, 13845, 13924, 14814, 15233, 15239, 15249, 15455, 15488, 15621, 15895, 16069, 16123, 16202, 16319, 16700, 16925, 17272, 17957, 18415, 18827, 19611, 19657, 19670, 19693]

        post_id_set.sort()
        loader.mapping = loader.load_nodups2dups_mapping(text_nodups2dups_mapping_)
        loader.load_data_by_post_id_set(self.path, post_id_set, raw_posts_, no_dups=self.no_dups)

    def tearDown(self):
        pass


class TestESLoaderMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_es_data_loader(self):
        es_loader.load(data_)

    def tearDown(self):
        pass   


if __name__ == '__main__':
    # unittest.main()
    def run_main_test():
        suite = unittest.TestSuite()
        suite.addTest(TestDataLoaderMethods("test_load"))
        # suite.addTest(TestDataLoaderMethods("test_data_loader"))
        # suite.addTest(TestDataLoaderMethods("test_mapping"))
        # suite.addTest(TestDataLoaderMethods("test_load_post"))
        # suite.addTest(TestDataLoaderMethods("test_load_data_by_post_id_set"))
        # suite.addTest(TestDataLoaderMethods("test_get_posts_for_token"))
        
        # suite.addTest(TestESLoaderMethods("test_es_data_loader"))




        runner = unittest.TextTestRunner()
        runner.run(suite)



    run_main_test()



"""
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
"""