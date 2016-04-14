"""


{'job_ads': 1, 'massage': 2, 'escort': 3,}
"""

import ast

class LabelAnnotation():

    def __init__(self, label_list):
        self.labels = self.map_label_list(label_list)


    def map_label_list(self, label_list):
        ans = {}
        for idx in range(len(label_list)):
            ans.setdefault(label_list[idx], idx+1)
        return ans

    def annoate_label(self, post_id, posts_path, graph_path):
        pass







graph_txt = '[147, 0, [[147, 0.0], [19721, 0.49319696191607187], [10366, 0.49319696191607187], [32230, 0.49319696191607187], [2188, 0.51987524491003645]]]'

label_list = ['job_ads', 'massage', 'escort']
ll = LabelAnnotation(label_list)
print ll.labels
        




