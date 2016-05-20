import numpy as np

from sklearn import datasets
from sklearn.semi_supervised import LabelPropagation
from wedc.domain.core.ml.helper import label

# label_prop_model = LabelPropagation()
iris = datasets.load_iris()
# random_unlabeled_points = np.where(np.random.random_integers(0, 1,
# size=len(iris.target)))
# labels = np.copy(iris.target)
# labels[random_unlabeled_points] = -1
# label_prop_model.fit(iris.data, labels)

# print iris.data
# print iris.target

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
            max_iter=1000, 
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

    sklearn_lp(X, y, output=output, kernel=kernel, gamma=gamma, n_neighbors=n_neighbors, alpha=alpha, max_iter=max_iter, tol=tol)



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
                        max_iter=1000, 
                        tol=0.00001):

    from wedc.domain.core.data.seed import seed_vector
    from wedc.domain.core.ml.graph import knn

    from wedc.infrastructure import database
    from wedc.infrastructure.model.labelled_data import LabelledData
    from wedc.infrastructure.model.seed_dict import SeedDict

    labelled_dataset = LabelledData.load_data()
    size = len(labelled_dataset)
    ld_data = []
    ld_label = []
    for labelled_data in labelled_dataset:
        ld_data.append(labelled_data.extraction)
        ld_label.append(labelled_data.label)

    seeds = SeedDict.load_data()
    post_vectors = seed_vector.generate_post_vector(ld_data, seeds)
    short_post_indexes = []
    for i, vec in enumerate(post_vectors):
        post_id = i + 1
        if max([float(_) for _ in vec.strip().split(' ')]) == 0:
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

            
    do_evaluation(new_X, new_y, output=output, kernel=kernel, gamma=gamma, n_neighbors=n_neighbors, alpha=alpha, max_iter=max_iter, tol=tol)

    # sklearn_lp(new_X, new_y, output=output, kernel=kernel, gamma=gamma, n_neighbors=n_neighbors, alpha=alpha, max_iter=max_iter, tol=tol)


    # java_lp(X, y, output=output, kernel=kernel, gamma=gamma, n_neighbors=n_neighbors, alpha=alpha, max_iter=max_iter, tol=tol)



def java_lp(X, y,
        output=None,
            kernel='knn', 
            gamma=None,
            n_neighbors=10, 
            alpha=1, 
            max_iter=1000, 
            tol=0.00001):

    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.9, random_state=42)

    # code below is for test

    post_dict, top_k, training_index, training_labels, testing_index, testing_labels = knn.do_knn(post_vectors, output, post_labels=ld_label)

    print 'training_labels:', training_labels #, len(training_labels)
    print 'training_index:', training_index #, len(training_index)
    # print len(training_index), ' + ', len(testing_index)
    # print testing_index

    gk_path = '/Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/graph_knn.txt'
    gl_path = '/Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/graph_lp.txt'
    lp_path = '/Users/ZwEin/job_works/StudentWork_USC-ISI/projects/WEDC/tests/data/labelprop.jar'

    run_lp(gk_path, gl_path, lp_path)

    y_test = testing_labels
    y_predict = []

    with open(gl_path, 'rb') as gl_file:
        lines = gl_file.readlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            line = line[1:-1]
            line = line.split(',')
            post_id = int(line[0])

            if post_id not in training_index:
                y_predict.append(int(line[1])) 

    # print 'y_predict', len(y_predict), y_predict
    # print 'y_test', len(y_test), y_test
    from sklearn.metrics import classification_report
    from sklearn.metrics import accuracy_score
    print '+--------------------------------------------------------+'
    print '|                         Report                         |'
    print '+--------------------------------------------------------+'
    # print 'test round:', (i+1), ' with random seed: ', random_seeds[i]
    # print 'training label: ', training_labels
    print 'predict label: ', y_predict
    print 'y_test: ', y_test
    print classification_report(y_test, y_predict)
    print 'accuracy: ' + str(accuracy_score(y_test, y_predict))
    print '\n\n'





    # do_evaluation(X, y, kernel=kernel, gamma=gamma, n_neighbors=n_neighbors, alpha=alpha, max_iter=max_iter, tol=tol)

def do_evaluation(X, y, 
                kernel='knn',
                output=None, 
                gamma=None,
                n_neighbors=10, 
                alpha=1, 
                max_iter=1000, 
                tol=0.00001):
    from sklearn.cross_validation import train_test_split
    from sklearn.metrics import classification_report
    from sklearn.metrics import accuracy_score
    import random

    size = len(X)

    random_seeds = np.random.randint(1, 1000, size=10)
    for i in range(len(random_seeds)):
        
        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.6, random_state=random_seeds[i])
        
        # random_unlabeled_points = np.where(np.random.random_integers(0, 1, size=size))

        label_prop_model = LabelPropagation(kernel=kernel, 
                                            gamma=gamma, 
                                            n_neighbors=n_neighbors, 
                                            alpha=alpha, 
                                            max_iter=max_iter, 
                                            tol=tol)
        label_prop_model.fit(X_train, y_train)


        y_predict = label_prop_model.predict(X_test)
        
        print '+--------------------------------------------------------+'
        print '|                         Report                         |'
        print '+--------------------------------------------------------+'
        print 'test round:', (i+1), ' with random seed: ', random_seeds[i]
        print 'training label: ', y_train
        print 'predict label: ', y_predict
        print classification_report(y_test, y_predict)
        print 'accuracy: ' + str(accuracy_score(y_test, y_predict))
        print '\n\n'
    


    
