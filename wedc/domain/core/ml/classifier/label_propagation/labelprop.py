import numpy as np
import os

from sklearn import datasets
from sklearn.semi_supervised import LabelPropagation
from wedc.domain.core.ml.helper import label
from wedc.domain.core.ml.graph import knn
from wedc.domain.core.data.seed import seed_vector

from wedc.infrastructure import database
from wedc.infrastructure.model.labelled_data import LabelledData
from wedc.infrastructure.model.seed_dict import SeedDict

from wedc.domain.conf.storage import __res_dir__


def run(input, output=None):
    return run_by_jar(input, output=output)

def run_by_jar(input, output=None, iter=100, eps='1e-05'):
    import ast
    import subprocess
    from subprocess import check_output

    lp_runnable_jar_ = os.path.expanduser(os.path.join(__res_dir__, 'labelprop.jar'))

    # run label propagation
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

        # line[0]: post id
        # line[1]: predict label
        # line[2:]: categories with weight
        line = ast.literal_eval(line)
        ans.append(line)

    return ans
   

    """
    valid_predict_indexes = []
    with open(gl_path, 'rb') as gl_file:
        lines = gl_file.readlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            line = line[1:-1]
            line = line.split(',')
            post_id = int(line[0])

            check_point = float(line[3][:-1]) + float(line[5][:-1]) + float(line[7][:-1])
            # if check_point > 0:
            #     valid_predict_indexes.append(post_id-1)

            if post_id not in training_index and check_point > 0: 
                valid_predict_indexes.append(post_id)
                y_predict.append(int(line[1]))

                if post_id in testing_index:
                    tmp = testing_index.index(post_id)
                    y_test.append(testing_labels[tmp])
    """





def evaluate_from_database(output=None,
                        kernel='knn', 
                        gamma=None,
                        n_neighbors=10, 
                        alpha=1, 
                        max_iter=100, 
                        tol=0.00001):

    labelled_dataset = LabelledData.load_data()
    size = len(labelled_dataset)
    ld_data = []
    ld_label = []
    for labelled_data in labelled_dataset:
        ld_data.append(labelled_data.extraction)
        ld_label.append(labelled_data.label)

    seeds = SeedDict.load_data()
    post_vectors = seed_vector.generate_post_vector(ld_data, seeds)

    # post_vector_seeds = seed_vector.generate_post_vector_seed(ld_data, seeds=seeds)
    # for i, vector in enumerate(post_vector_seeds):
    #     if ld_label[i] == 4:
    #         print vector.strip()

    # remove short post
    short_post_indexes = []
    short_ext_word_edge = 8
    for i, vec in enumerate(post_vectors):
        post_id = i + 1

        if len(ld_data[i].split(' ')) < short_ext_word_edge or max([float(_) for _ in vec.strip().split(' ')]) == 0:
            short_post_indexes.append(post_id)
        
    # print short_post_indexes
    
    X = np.array(np.mat(';'.join(post_vectors)))
    y = ld_label

    mapping = {}
    new_X = []
    new_y = []
    new_post_id = 1
    for i in range(size):
        post_id = i + 1
        if post_id not in short_post_indexes:
            new_X.append(X[i])
            new_y.append(y[i])
            mapping[new_post_id] = post_id
            new_post_id += 1

            
    # do_evaluation(new_X, new_y, output=output, kernel=kernel, gamma=gamma, n_neighbors=n_neighbors, alpha=alpha, max_iter=max_iter, tol=tol)

    # sklearn_lp(new_X, new_y, output=output, kernel=kernel, gamma=gamma, n_neighbors=n_neighbors, alpha=alpha, max_iter=max_iter, tol=tol)

    # print len(new_X), len(new_y)
    # print len(X), len(y)
    print mapping



    return java_lp(new_X, new_y, mapping=mapping, output=output, kernel=kernel, gamma=gamma, n_neighbors=n_neighbors, alpha=alpha, max_iter=max_iter, tol=tol)

def java_lp(X, y,
            mapping=None,
            output=None,
            kernel='knn', 
            gamma=None,
            n_neighbors=10, 
            alpha=1, 
            max_iter=1000, 
            tol=0.00001):
    
    gk_path = '/Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/graph_knn.txt'
    gl_path = '/Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/graph_lp.txt'
    lp_path = '/Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/labelprop.jar'

    post_dict, top_k, training_index, training_labels, testing_index, testing_labels = knn.do_knn(X, output=gk_path, post_labels=y, n_neighbors=n_neighbors)

    # print top_k, post_dict

    run_lp(gk_path, gl_path, lp_path)

    # y_test = testing_labels
    y_test = []
    y_predict = []

    valid_predict_indexes = []
    with open(gl_path, 'rb') as gl_file:
        lines = gl_file.readlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            line = line[1:-1]
            line = line.split(',')
            post_id = int(line[0])

            check_point = float(line[3][:-1]) + float(line[5][:-1]) + float(line[7][:-1])
            # if check_point > 0:
            #     valid_predict_indexes.append(post_id-1)

            if post_id not in training_index and check_point > 0: 
                valid_predict_indexes.append(post_id)
                y_predict.append(int(line[1]))

                if post_id in testing_index:
                    tmp = testing_index.index(post_id)
                    y_test.append(testing_labels[tmp])

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

