import numpy as np
import os
import shutil


from sklearn import datasets
from sklearn.semi_supervised import LabelPropagation
from wedc.domain.core.ml.helper import label
# from wedc.domain.core.ml.graph import knn
from wedc.domain.core.ml.classifier.label_propagation import knn
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

def do_evaluation(output_path, num_of_tests=1, test_rate=.9, n_neighbors=10, max_iter=100, tol=0.00001):
    
    # load data and label
    dataset = load_dataset()

    # load seeds and generate post vector
    # short posts will be removed when load post vectors
    seeds = SeedDict.load_data()
    dataset = load_post_vectors(dataset, seeds) # short post removed
    
    # load file path
    if os.path.isdir(output_path):
        shutil.rmtree(output_path)
    os.mkdir(output_path)
    
    pid_set = [_[0] for _ in dataset]
    random_seeds = np.random.randint(1, 10000000, size=num_of_tests)

    # count = 0
    ans = []
    for i, random_seed in enumerate(random_seeds):
        # prepare report env
        round_path_ = os.path.join(output_path, 'round_' + str(i+1) + '_random_seed_' + str(random_seed))
        os.mkdir(round_path_)
        graph_path_ = os.path.join(round_path_, 'graph_knn.txt')
        labelprop_path_ = os.path.join(round_path_, 'graph_lp.txt')
        report_path_ = os.path.join(round_path_, 'report.txt')

        # shuffle post id set to load random data
        shuffled_pid_set = list(pid_set)
        np.random.seed(random_seed)
        np.random.shuffle(shuffled_pid_set) 
        
        total_size = len(shuffled_pid_set)
        total_testing_items = int(total_size*test_rate)
        total_training_items = total_size - total_testing_items
        # print total_training_items, '+', total_testing_items, '=', total_size

        training_pid_set = shuffled_pid_set[total_testing_items:]
        testing_pid_set = shuffled_pid_set[:total_testing_items]

        # item[0]: post id
        # item[1]: label
        # item[2]: vector
        # training_set = [[_[0], _[1], _[3]] for _ in dataset if _[0] in training_pid_set] 
        # testing_set = [[_[0], _[1], _[3]] for _ in dataset if _[0] in testing_pid_set] 

        # # for X_train, vector formated in a string
        training_data = [_[3] for _ in dataset if _[0] in training_pid_set] 
        # # for y_train, label in int
        training_label = [_[1] for _ in dataset if _[0] in training_pid_set] 
        # # for X_test, vector formated in a string
        testing_data = [_[3] for _ in dataset if _[0] in testing_pid_set]
        # # for y_test, label in int
        testing_label = [_[1] for _ in dataset if _[0] in testing_pid_set]

        # prepare X, y for graph
        X = np.array(np.mat(';'.join([_[3] for _ in dataset]))) # in order, asc
        y = np.copy([_[1] for _ in dataset])    # in order, asc
        y[[pid_set.index(_) for _ in testing_pid_set]] = 0  # in order, asc

        # item[0]: post id
        # item[1]: vector in numpy
        # item[2]: label in numpy, filling with 0 for testing data
        graph_input = [[pid_set[_], X[_], y[_]] for _ in range(len(pid_set))]

        # build knn graph
        graph = knn.build(graph_input, output=graph_path_, n_neighbors=n_neighbors)
        rtn_lp = run_lp(graph_path_, output=labelprop_path_)
        
        valid_pid_set = [_[0] for _ in rtn_lp if _[0] in testing_pid_set]   # in order, asc

        y_predict = [_[1] for _ in rtn_lp if _[0] in valid_pid_set] # in order, asc
        y_test = [_[1] for _ in dataset if _[0] in valid_pid_set]   # in order, asc

        # from sklearn.metrics import accuracy_score
        # accuracy = accuracy_score(y_test, y_predict)
        # if accuracy < 0.9:
        #     count += 1

        info_data = [[training_pid_set, training_data, training_label], [testing_pid_set, testing_data, testing_label], [len(y), len(valid_pid_set)]]
        label_data = [y_test, y_predict, valid_pid_set]

        accuracy = generate_report(report_path_, i+1, random_seed, info_data, label_data)

        ans.append([i+1, accuracy, info_data, label_data])

    return ans
    # print 1.*count/num_of_tests

def generate_report(report_path_, round_id, random_seed, info_data, label_data):
    from sklearn.metrics import classification_report
    from sklearn.metrics import accuracy_score

    # info data
    training_pid_set = info_data[0][0]
    training_data = info_data[0][1]
    training_label = info_data[0][2]

    testing_pid_set = info_data[1][0]
    testing_data = info_data[1][1]
    testing_label = info_data[1][2]

    size_witout_short_posts = info_data[2][0]
    size_valid_lp_pred = info_data[2][0]

    # label data
    # label_data = sorted(label_data, key=lambda x: x[2])
    y_test = label_data[0]
    y_predict = label_data[1]
    valid_pid_set = label_data[2]
    report = classification_report(y_test, y_predict)
    accuracy = accuracy_score(y_test, y_predict)

    # test only
    """
    if accuracy < 0.8:
        print 'round_id:', round_id, ', accuracy: ', accuracy 
        print valid_pid_set
    print accuracy
    """

    with open(report_path_, 'wb') as rf:
        rf.write('+--------------------------------------------------------+\n')
        rf.write('|                         Report                         |\n')
        rf.write('+--------------------------------------------------------+\n\n')

        rf.write('total size of posts without short posts: ' + str(size_witout_short_posts) + '\n')
        rf.write('valid prediction from label propagation: ' + str(size_valid_lp_pred) + '\n')
        
        rf.write('\n'+ report +'\n')
        rf.write('accuracy: ' + str(accuracy) + '\n')

        rf.write('y_test:\n')
        rf.write(str(y_test) + '\n')
        rf.write('y_predict:\n')
        rf.write(str(y_predict) + '\n')

        rf.write('y_test | y_pred | pid \n')
        
        for i in range(len(y_test)):
            rf.write(str(y_test[i]) + ' | ' + str(y_predict[i]) + ' | ' + str(valid_pid_set[i]) + '\n')

        rf.write('\n\n\n\n')
        
        rf.write('---- Training ----\n')
        rf.write('size: '+str(len(training_pid_set))+'\n')
        rf.write('post id set:\n'+str(training_pid_set)+'\n')
        rf.write('training labels:\n'+str(training_label)+'\n')
        rf.write('label | pid \n')
        for i in range(len(training_pid_set)):
            rf.write(str(training_label[i]) + ' | ' + str(training_pid_set[i]) + '\n')
        
        rf.write('\n\n\n\n')
        
        rf.write('---- Testing ----\n')
        rf.write('size: '+str(len(testing_pid_set))+'\n')
        rf.write('post id set:\n'+str(testing_pid_set)+'\n')
        rf.write('testing labels:\n'+str(testing_label)+'\n')
        rf.write('label | pid \n')
        for i in range(len(testing_pid_set)):
            rf.write(str(testing_label[i]) + ' | ' + str(testing_pid_set[i]) + '\n')
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
        # data[3]: source id
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


