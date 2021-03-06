import numpy as np

from sklearn import datasets
from sklearn.semi_supervised import LabelPropagation
from wedc.domain.core.ml.helper import label
from wedc.domain.core.ml.graph import knn
from wedc.domain.core.data.seed import seed_vector

from wedc.infrastructure import database
from wedc.infrastructure.model.labelled_data import LabelledData
from wedc.infrastructure.model.seed_dict import SeedDict

def do_label_propagation(input_data,
                        input_label,
                        output=None,
                        kernel='knn', 
                        gamma=None,
                        n_neighbors=10, 
                        alpha=1, 
                        max_iter=30, 
                        tol=0.001):
    n_neighbors += 1

    # input label
    input_label_fh = open(input_label, 'rb')
    label_lines = input_label_fh.readlines()
    label_lines = [int(_.strip()) for _ in label_lines]
    y = np.array(label_lines)
    input_label_fh.close()

    size = len(y)

    # input data
    input_data_fh = open(input_data, 'rb')
    data_lines = input_data_fh.readlines()[:size]
    data_lines = [_.strip() for _ in data_lines]
    X = np.array(np.mat(';'.join(data_lines)))
    input_data_fh.close()

    label_prop_model = LabelPropagation(kernel=kernel, 
                                        gamma=gamma, 
                                        n_neighbors=n_neighbors, 
                                        alpha=alpha, 
                                        max_iter=max_iter, 
                                        tol=tol)
    label_prop_model.fit(X, y)

    prediction = label_prop_model.predict(X)

    if output:
        output_fh = open(output, 'wb')
        for p in prediction:
            output_fh.write(str(p)+'\n')
        output_fh.close()

    return label_prop_model


def run_lp(input, output, lp_jar):
    import subprocess
    import os
    if os.path.isfile(output):
        os.remove(output)
    output_file = open(output, 'a')
    working_dir = os.sep.join(lp_jar.split(os.sep)[:-1])
    jar_file = lp_jar.split(os.sep)[-1]
    
    argsArray = ['java', '-classpath', jar_file, 'org.ooxo.LProp', '-a', 'GFHF', '-m', '100', '-e', '10e-6', input]
    subprocess.call(argsArray, cwd=working_dir, stdout=output_file)
    output_file.close()

    
def evaluate_from_file(input_data,
            output=None,
            kernel='knn', 
            gamma=None,
            n_neighbors=10, 
            alpha=1, 
            max_iter=100, 
            tol=0.00001):
    
    label_dict = label.load_label_dict()
    label_dict = sorted(label_dict.iteritems(), key=lambda x:x[0])
    post_id_list = []
    y = []
    for (k, v) in label_dict:
        post_id_list.append(k)
        y.append(v)

    input_data_fh = open(input_data, 'rb')
    data_lines = input_data_fh.readlines()
    data_lines = [data_lines[i] for i in post_id_list]
    data_lines = [_.strip() for _ in data_lines]

    X = np.array(np.mat(';'.join(data_lines)))
    input_data_fh.close()

    # sklearn_lp(X, y, output=output, kernel=kernel, gamma=gamma, n_neighbors=n_neighbors, alpha=alpha, max_iter=max_iter, tol=tol)

    java_lp(new_X, new_y, output=output, kernel=kernel, gamma=gamma, n_neighbors=n_neighbors, alpha=alpha, max_iter=max_iter, tol=tol)



def sklearn_lp(X, y,
            output=None,
            kernel='knn', 
            gamma=None,
            n_neighbors=10, 
            alpha=1, 
            max_iter=1000, 
            tol=0.00001):

    from sklearn.cross_validation import train_test_split
    from sklearn.metrics import classification_report
    from sklearn.metrics import accuracy_score

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.9, random_state=3)
    label_prop_model = LabelPropagation(kernel=kernel, 
                                        gamma=gamma, 
                                        n_neighbors=n_neighbors, 
                                        alpha=alpha, 
                                        max_iter=max_iter, 
                                        tol=tol)
    label_prop_model.fit(X_train, y_train)

    y_predict = label_prop_model.predict(X_test)
    print 'y_train: ', y_train
    print 'y_predict: ', y_predict
    
    print '+--------------------------------------------------------+'
    print '|                         Report                         +'
    print '+--------------------------------------------------------+'
    print classification_report(y_test, y_predict)
    print 'accuracy: ' + str(accuracy_score(y_test, y_predict))
    print '\n\n'

    
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



    # do_evaluation(X, y, kernel=kernel, gamma=gamma, n_neighbors=n_neighbors, alpha=alpha, max_iter=max_iter, tol=tol)

def do_evaluation(X, y, 
                kernel='knn',
                output=None, 
                gamma=None,
                n_neighbors=10, 
                alpha=1, 
                max_iter=1000, 
                tol=0.00001):
    # from sklearn.cross_validation import train_test_split
    from sklearn.metrics import classification_report
    from sklearn.metrics import accuracy_score
    import random

    size = len(X)

    random_seeds = np.random.randint(1, 1000, size=10)
    for i in range(len(random_seeds)):
        
        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.6, random_state=random_seeds[i])
        labels = np.copy(y)
        tmp = np.arange(size)
        np.random.shuffle(tmp)
        train_test_split_rate = int(size*.9)
        random_unlabeled_points = tmp[:train_test_split_rate]
        labeled_points = tmp[train_test_split_rate:]
        random_unlabeled_points.sort()
        X_test = [X[_] for _ in range(size) if _ in random_unlabeled_points]
        y_test = [y[_] for _ in range(size) if _ in random_unlabeled_points]
        y_train = [y[_] for _ in range(size) if _ in labeled_points]

        labels[random_unlabeled_points] = -1

        label_prop_model = LabelPropagation(kernel=kernel, 
                                            gamma=gamma, 
                                            n_neighbors=n_neighbors, 
                                            alpha=alpha, 
                                            max_iter=max_iter, 
                                            tol=tol)
        label_prop_model.fit(X, labels)

        y_predict = label_prop_model.predict(X_test)
        
        print '+--------------------------------------------------------+'
        print '|                         Report                         |'
        print '+--------------------------------------------------------+'
        print 'test round:', (i+1), ' with random seed: ', random_seeds[i]
        print 'training label: ', y_train
        print 'training post id: ', [_+1 for _ in labeled_points]
        print 'predict label: ', y_predict
        print classification_report(y_test, y_predict)
        print 'accuracy: ' + str(accuracy_score(y_test, y_predict))
        print '\n\n'
    


    
