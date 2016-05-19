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

    
def evaluate_from_file(input_data,
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


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.9, random_state=3)
    label_prop_model = LabelPropagation(kernel=kernel, 
                                        gamma=gamma, 
                                        n_neighbors=n_neighbors, 
                                        alpha=alpha, 
                                        max_iter=max_iter, 
                                        tol=tol)
    label_prop_model.fit(X_train, y_train)

    y_predict = label_prop_model.predict(X_test)

    
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
    from wedc.infrastructure import database
    from wedc.infrastructure.model.labelled_data import LabelledData

    labelled_dataset = LabelledData.load_data()
    # print labelled_data
    ld_data = []
    ld_label = []
    for labelled_data in labelled_dataset:
        ld_data.append(labelled_data.extraction)
        ld_label.append(labelled_data.label)
        
    seed_vector.generate_post_vector(ld_data, seeds, output)




    """
    from sklearn.cross_validation import train_test_split
    from sklearn.metrics import classification_report
    from sklearn.metrics import accuracy_score

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


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.9, random_state=3)
    label_prop_model = LabelPropagation(kernel=kernel, 
                                        gamma=gamma, 
                                        n_neighbors=n_neighbors, 
                                        alpha=alpha, 
                                        max_iter=max_iter, 
                                        tol=tol)
    label_prop_model.fit(X_train, y_train)

    y_predict = label_prop_model.predict(X_test)

    
    print '+--------------------------------------------------------+'
    print '|                         Report                         +'
    print '+--------------------------------------------------------+'
    print classification_report(y_test, y_predict)
    print 'accuracy: ' + str(accuracy_score(y_test, y_predict))
    print '\n\n'
    """


    
