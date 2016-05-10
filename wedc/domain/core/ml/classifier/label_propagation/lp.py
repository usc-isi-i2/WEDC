import numpy as np

from sklearn import datasets
from sklearn.semi_supervised import LabelPropagation
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
                        gamma=20, 
                        n_neighbors=7, 
                        alpha=1, 
                        max_iter=30, 
                        tol=0.001):
    n_neighbors += 1

    # input data
    input_data_fh = open(input_data, 'rb')
    data_lines = input_data_fh.readlines()[:10]
    size = len(data_lines)
    data_lines = [_.strip() for _ in data_lines]
    X = np.array(np.mat(';'.join(data_lines)))
    input_data_fh.close()

    # input label
    input_label_fh = open(input_label, 'rb')
    label_lines = input_label_fh.readlines()[:10]
    label_lines = [int(_.strip()) for _ in label_lines]
    y = np.array(label_lines)
    input_label_fh.close()

    # print y
    label_prop_model = LabelPropagation()
    label_prop_model.fit(X, y)

    if output:
        output_fh = open(output, 'wb')
        output_fh.close()

    



    
