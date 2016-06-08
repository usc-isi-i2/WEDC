import numpy as np
import os
import shutil

from sklearn import datasets
from sklearn.semi_supervised import LabelPropagation
from wedc.domain.core.ml.helper import label
from wedc.domain.core.ml.classifier.label_propagation import knn
from wedc.domain.core.data.seed import seed_vector
from wedc.domain.vendor.label_propagation import lp

#######################################################
#   Run Label Propagation
#######################################################

def run(data, labelled_data, n_neighbors=10, iter=100, eps=0.00001):
    pid = 1
    mapping = {}    # from pid to sid
    X = []
    y = []
    pids = []
    
    # load data
    for i, kv in enumerate(data):
        sid, vector = kv
        mapping[pid] = sid
        pids.append(pid)
        X.append(vector)
        y.append(0)
        # dataset.append([pid, vector, 0])
        pid = pid + 1

    # load labelled data
    for item in labelled_data: 
        vector = item[0]
        label = item[1]
        pids.append(pid)
        X.append(vector)
        y.append(label)
        # dataset.append([pid, vector, label])
        pid = pid + 1

    # prepare X, y for graph
    X = np.array(np.mat(';'.join([_ for _ in X]))) # in order, asc
    y = np.copy(y)    # in order, asc

    # graph
    graph_input = [[pids[_], X[_], y[_]] for _ in range(len(pids))]
    graph = knn.build(graph_input, n_neighbors=n_neighbors)

    # lp
    lp_data = '\n'.join([str(_) for _ in graph])
    rtn_lp = lp.run_by_py4j(lp_data, iter=iter, eps=eps)
    
    # return (10, '1')

    ans = {}
    for preds in rtn_lp:
        pid = int(preds[0])
        if pid not in mapping:
            continue
        pred_label = preds[1]
        score = preds[2]
        ans[mapping[pid]] = [pred_label, score]
    return [(1, ans)]


def run_lp(input, output=None):
    return lp.run_by_jar(input, output=output)

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


