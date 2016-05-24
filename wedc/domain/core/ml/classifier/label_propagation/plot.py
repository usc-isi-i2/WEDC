import matplotlib.pyplot as plt
import numpy as np

from wedc.domain.core.ml.classifier.label_propagation import labelprop

DEFAULT_NUM_OF_TESTS = 1
DEFAULT_TEST_RATE = .9
DEFAULT_N_NEIGHBORS = 5
DEFAULT_MAX_ITER = 200
DEFAULT_TOL = 0.000001

#######################################################
#   Accuracy
#######################################################
DEFAULT_TEST_RATE_SET = [.9, .8, .7, .6, .5, .4, .3, .2, .1]

def calc_accuracy(lp_evaluation_dir_, num_of_tests=DEFAULT_NUM_OF_TESTS, test_rate=DEFAULT_TEST_RATE, n_neighbors=DEFAULT_N_NEIGHBORS, max_iter=DEFAULT_MAX_ITER, tol=DEFAULT_TOL):
    output = labelprop.do_evaluation(lp_evaluation_dir_, num_of_tests=num_of_tests, test_rate=test_rate, n_neighbors=n_neighbors, max_iter=max_iter, tol=tol)
    return np.mean([_[1] for _ in output])

def generate_accuracy_list(lp_evaluation_dir_, num_of_tests=DEFAULT_NUM_OF_TESTS, n_neighbors=DEFAULT_N_NEIGHBORS, max_iter=DEFAULT_MAX_ITER, tol=DEFAULT_TOL):
    test_rate_set = DEFAULT_TEST_RATE_SET
    accuracy_list = []
    for test_rate in test_rate_set:
        accuracy_mean = calc_accuracy(lp_evaluation_dir_, num_of_tests=num_of_tests, test_rate=test_rate, n_neighbors=n_neighbors, max_iter=max_iter, tol=tol)
        accuracy_list.append(accuracy_mean)
    return accuracy_list

def generate_accuracy_lists(lp_evaluation_dir_, n_neighbors_set=None, max_iter_set=None, tol_set=None):

    if n_neighbors_set:
        return [generate_accuracy_list(lp_evaluation_dir_, n_neighbors=n_neighbors) for n_neighbors in n_neighbors_set]


def plot_accuracy(lp_evaluation_dir_):

    test_rate_set = DEFAULT_TEST_RATE_SET
    n_neighbors_set = [5, 10, 20, 30]

    # print generate_accuracy_lists(lp_evaluation_dir_, n_neighbors_set=n_neighbors_set)

    accuracy_lists = [[0.94444444444444442, 1.0, 1.0, 0.94999999999999996, 0.84999999999999998, 1.0, 1.0, 1.0, 1.0], [0.967741935483871, 0.72727272727272729, 1.0, 1.0, 0.96296296296296291, 1.0, 1.0, 1.0, 1.0], [0.91489361702127658, 0.48780487804878048, 0.97297297297297303, 0.9375, 0.96153846153846156, 0.94117647058823528, 1.0, 1.0, 1.0], [0.2857142857142857, 0.93617021276595747, 0.92105263157894735, 0.94444444444444442, 0.90909090909090906, 0.95833333333333337, 0.78947368421052633, 0.91666666666666663, 0.875]]

    t1 = np.arange(0.0, 2.0, 0.1)
    t2 = np.arange(0.0, 2.0, 0.01)
    # accuracy_lists = [' '.join(_) for _ in accuracy_lists]
    # al = accuracy_lists[0]
    
    # l1, = plt.plot(test_rate_set, al)
    # l2, l3 = plt.plot(t2, np.sin(2 * np.pi * t2), '--go', t1, np.log(1 + t1), '.')
    
    plt_list = []
    for al in accuracy_lists:
        plt_list.append(plt.plot(test_rate_set, al))   
    plt_list = [tuple(_) for _ in plt_list]     

    plt.legend((plt_list), tuple([str(_) for _ in n_neighbors_set]), loc='lower left', shadow=True)
    plt.xlabel('percentage of data are used for testing')
    plt.ylabel('accuracy')
    plt.title('Accuracy for varous n_neighbors')
    plt.show()

    plt.show()

