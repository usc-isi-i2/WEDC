import numpy as np
import os
import shutil


from sklearn import datasets
from sklearn.semi_supervised import LabelPropagation
from wedc.domain.core.ml.helper import label
from wedc.domain.core.ml.graph import knn
from wedc.domain.core.data.seed import seed_vector

from wedc.infrastructure import database
from wedc.infrastructure.model.labelled_data import LabelledData
from wedc.infrastructure.model.seed_dict import SeedDict

from wedc.domain.conf.storage import __res_dir__

#######################################################
#   Run Label Propagation
#######################################################

def run_lp(input, output=None):
    return run_by_jar(input, output=output)

def run_by_jar(input, output=None, iter=100, eps=0.00001):
    import ast
    import subprocess
    from subprocess import check_output
    from decimal import Decimal

    lp_runnable_jar_ = os.path.expanduser(os.path.join(__res_dir__, 'labelprop.jar'))

    # run label propagation
    eps = '%.e' % Decimal(eps)  # change decimal into e format
    argsArray = ['java', '-classpath', lp_runnable_jar_, 'org.ooxo.LProp', '-a', 'GFHF', '-m', str(iter), '-e', eps, input]
    raw_output = check_output(argsArray)

    # output into file
    if output:
        output_file = open(output, 'wb')
        output_file.writelines(raw_output)
        output_file.close()

    # refine result
    ans = []
    for line in raw_output.split('\n'):
        if not line:    # actually in the end of file
            continue

        # line definition
        # line[0]: post id
        # line[1]: predict label
        # line[2:]: categories with weight
        line = ast.literal_eval(line)

        # filter invalid predictionobject
        if sum([float(_[1]) for _ in line[2:]]):
            ans.append(line)

    return ans


#######################################################
#   Evaluation
#######################################################

def do_evaluation(output_path, n_neighbors=10, max_iter=100, tol=0.00001):
    """
    # load data and label
    dataset = load_dataset()

    # load seeds and generate post vector
    # short posts will be removed when load post vectors
    seeds = SeedDict.load_data()
    dataset = load_post_vectors(dataset, seeds)

    # do knn here
    # X, y (y contain 0 randomly for test)
    """
    
    # load file path
    if os.path.isdir(output_path):
        shutil.rmtree(output_path)
    os.mkdir(output_path)
    graph_path_ = os.path.join(output_path, 'graph_knn.txt')
    labelprop_path_ = os.path.join(output_path, 'graph_lp.txt')
    report_path_ = os.path.join(output_path, 'report_path_.txt')
    




    # X = np.array(np.mat(';'.join(post_vectors)))
    # y = ld_label


    # output = run_lp(graph_knn_, output=graph_lp_)

    # post_dict, top_k, training_index, training_labels, testing_index, testing_labels = knn.do_knn(X, output=gk_path, post_labels=y, n_neighbors=n_neighbors)

    # # print top_k, post_dict

    # run_lp(gk_path, gl_path, lp_path)


    # y_test = testing_labels
    y_test = []
    y_predict = []

    # valid_predict_indexes = [mapping[_] for _ in valid_predict_indexes]


    # print len(valid_predict_indexes), valid_predict_indexes
    # print len(y_predict), y_predict
    # print len(y_test), y_test

    # """
    # print 'y_predict', len(y_predict), y_predict
    # print 'y_test', len(y_test), y_test
    from sklearn.metrics import classification_report
    from sklearn.metrics import accuracy_score
    accuracy = accuracy_score(y_test, y_predict)
    if accuracy > 0.5:
        print accuracy, '\n'
        return accuracy
    print '+--------------------------------------------------------+'
    print '|                         Report                         |'
    print '+--------------------------------------------------------+'
    print 'training size:', len(training_index)
    print 'training_labels:', training_labels #, len(training_labels)
    print 'training_index:', training_index #, len(training_index)
    # print len(training_index), ' + ', len(testing_index)
    # print testing_index
    # print 'test round:', (i+1), ' with random seed: ', random_seeds[i]
    # print 'training label: ', training_labels
    
    print 'predict label: ', y_predict
    print 'y_test: ', y_test
    print 'graph post_id:', valid_predict_indexes
    print 'original post_id:', [mapping[_] for _ in valid_predict_indexes]

    print classification_report(y_test, y_predict)
    print 'accuracy: ' + str(accuracy_score(y_test, y_predict))
    print '\n\n'
    # """
    return accuracy




#######################################################
#   Common
#######################################################




def load_dataset():
    
    # load dataset from database
    labelled_dataset = LabelledData.load_data()

    dataset = []
    for idx, ld in enumerate(labelled_dataset):

        # data[0]: post id
        # data[1]: data label
        # data[2]: data extraction
        data = [idx+1, int(ld.label), str(ld.extraction)]

        dataset.append(data)

    return dataset

def load_post_vectors(dataset, seeds):

    # load extractions and generate post vectors
    post_vectors = seed_vector.generate_post_vector([_[2] for _ in dataset], seeds)

    # add post_id for post vectors
    # data[0]: post id
    # data[1]: post label
    # data[2]: post extration
    # data[3]: post vector
    [dataset[i].extend([_]) for i, _ in enumerate(post_vectors)]

    # refine dataset
    # 1. less than 8 extraction words will be removed
    # 2. extraction without any seed words will be removed
    refined_dataset = []
    ext_len_threshold = 8
    for data in dataset:
        # pid = data[0]
        # label = data[1]
        # extraction = data[2]
        # vector = data[3]
        extractions_count = len(data[2].split(' '))
        vector_list = [float(_) for _ in data[3].strip().split(' ')]
        if extractions_count < ext_len_threshold or max(vector_list) == 0:
            continue
        else:
            refined_dataset.append(data)
    
    return refined_dataset


