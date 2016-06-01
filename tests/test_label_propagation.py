""" Test word2vec

Example:
http://nbviewer.jupyter.org/github/danielfrg/word2vec/blob/master/examples/doc2vec.ipynb
http://nbviewer.jupyter.org/github/danielfrg/word2vec/blob/master/examples/word2vec.ipynb

"""


import sys
import time
import os
import unittest
import shutil
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
from wedc.domain.core.ml.classifier.label_propagation import plot

post2vec_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'post2vec.txt'))
post2vec_label_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'post2vec_label.txt'))
post2vec_predict_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'post2vec_predict.txt'))
graph_knn_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'graph_knn.txt'))
graph_lp_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'graph_lp.txt'))
lp_jar_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'labelprop.jar'))
lp_evaluation_dir_ = os.path.expanduser(os.path.join(TEST_DATA_DIR, 'evaluation'))


from wedc.domain.core.ml.graph import knn
from wedc.domain.core.ml.helper import label
from wedc.domain.core.ml.classifier.label_propagation import lp
from wedc.domain.core.ml.classifier.label_propagation import labelprop

class TestLabelPropagationMethods(unittest.TestCase):
    def setUp(self):
        label_dict = label.load_label_dict()
        label.generate_label_file(label_dict, post2vec_label_)
        # label.generate_label_file(label_dict, post2vec_label_, post2vec_txt_path=post2vec_)

    def test_generate_label_file(self):
        label_dict = label.load_label_dict()
        label.generate_label_file(label_dict, output=post2vec_label_)
        # label.generate_label_file(label_dict, output=post2vec_label_, post2vec_txt_path=post2vec_)

    def test_do_label_propagation(self):
        label_prop_model = lp.do_label_propagation(input_data=post2vec_,
                                input_label=post2vec_label_,
                                output=post2vec_predict_,
                                kernel='knn',
                                n_neighbors=10, 
                                alpha=1,
                                max_iter=100, 
                                tol=0.000001)



    def test_load_unknown_post_index(self):
        print label.load_unknown_post_index(post2vec_)

    def test_evaluate(self):
        # lp.evaluate_from_file(input_data=post2vec_)
        
        # accuracy = lp.evaluate_from_database(kernel='knn', 
        #                         output=graph_knn_,
        #                         gamma=None,
        #                         n_neighbors=10, 
        #                         alpha=1, 
        #                         max_iter=100, 
        #                         tol=0.000001)

        # for i in range(100):
        #     try:
        #         accuracy = lp.evaluate_from_database(kernel='knn', 
        #                         output=graph_knn_,
        #                         gamma=None,
        #                         n_neighbors=10, 
        #                         alpha=1, 
        #                         max_iter=100, 
        #                         tol=0.000001)
        #         if accuracy < 0.5:
        #             break
        #     except Exception as e:
        #         print "IGNORE \n"

        
        labelprop.run_by_jar(graph_knn_, graph_lp_)

    def test_run(self):
        output = labelprop.run_lp(graph_knn_, output=graph_lp_)
        

    def test_do_evaluation(self):
        # 0.27: 27 out of 100 posts with accuracy below .9%
        output = labelprop.do_evaluation(lp_evaluation_dir_, num_of_tests=1, test_rate=.7, n_neighbors=5, max_iter=200, tol=0.000001)

        for rnd in output:
            round_id = rnd[0]
            accuracy = rnd[1]

            # info data
            info_data = rnd[2]
            training_pid_set = info_data[0][0]
            training_data = info_data[0][1]
            training_label = info_data[0][2]

            testing_pid_set = info_data[1][0]
            testing_data = info_data[1][1]
            testing_label = info_data[1][2]

            size_witout_short_posts = info_data[2][0]
            size_valid_lp_pred = info_data[2][0]

            # label data
            label_data = rnd[3]
            y_test = label_data[0]
            y_predict = label_data[1]
            valid_pid_set = label_data[2]
        
    def tearDown(self):
        pass


class TestGraphMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_build_knn_graph(self):
        print knn.build_graph(input=post2vec_, output=graph_knn_, n_neighbors=10, algorithm='ball_tree')

    def tearDown(self):
        pass

class TestPlotMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_accuracy_plot(self):
        plot.plot_accuracy(lp_evaluation_dir_)

    def test_confusion_matrix(self):
        plot.plot_confusion_matrix(lp_evaluation_dir_)

    def test_plot_prf(self):
        plot.plot_prf(lp_evaluation_dir_)

    def tearDown(self):
        pass

if __name__ == '__main__':
    # unittest.main()

    def run_main_test():
        suite = unittest.TestSuite()

        ### Test Label Propagation ###
        # suite.addTest(TestLabelPropagationMethods("test_generate_label_file"))
        # suite.addTest(TestLabelPropagationMethods("test_do_label_propagation"))
        # suite.addTest(TestLabelPropagationMethods("test_load_unknown_post_index"))
        # suite.addTest(TestLabelPropagationMethods("test_evaluate"))
        # suite.addTest(TestLabelPropagationMethods("test_run"))
        suite.addTest(TestLabelPropagationMethods("test_do_evaluation"))

        ### Test Graph ###
        # suite.addTest(TestGraphMethods("test_build_knn_graph"))
        
        ### Test Plot ###
        # suite.addTest(TestPlotMethods("test_accuracy_plot"))
        # suite.addTest(TestPlotMethods("test_confusion_matrix"))
        # suite.addTest(TestPlotMethods("test_plot_prf"))


        runner = unittest.TextTestRunner()
        runner.run(suite)

    run_main_test()



