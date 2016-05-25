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

DEFAULT_TRAIN_RATE_SET = [.1, .2, .3, .4, .5]

def calc_accuracy(lp_evaluation_dir_, num_of_tests=DEFAULT_NUM_OF_TESTS, test_rate=DEFAULT_TEST_RATE, n_neighbors=DEFAULT_N_NEIGHBORS, max_iter=DEFAULT_MAX_ITER, tol=DEFAULT_TOL):
    output = labelprop.do_evaluation(lp_evaluation_dir_, num_of_tests=num_of_tests, test_rate=test_rate, n_neighbors=n_neighbors, max_iter=max_iter, tol=tol)
    return np.mean([_[1] for _ in output])

def generate_accuracy_list(lp_evaluation_dir_, num_of_tests=DEFAULT_NUM_OF_TESTS, n_neighbors=DEFAULT_N_NEIGHBORS, max_iter=DEFAULT_MAX_ITER, tol=DEFAULT_TOL):
    test_rate_set = [1.-_ for _ in DEFAULT_TRAIN_RATE_SET]
    accuracy_list = []
    for test_rate in test_rate_set:
        accuracy_mean = calc_accuracy(lp_evaluation_dir_, num_of_tests=num_of_tests, test_rate=test_rate, n_neighbors=n_neighbors, max_iter=max_iter, tol=tol)
        accuracy_list.append(accuracy_mean)
    return accuracy_list

def generate_accuracy_lists(lp_evaluation_dir_, n_neighbors_set=None, max_iter_set=None, tol_set=None):

    if n_neighbors_set:
        return [generate_accuracy_list(lp_evaluation_dir_, n_neighbors=n_neighbors) for n_neighbors in n_neighbors_set]

    if max_iter_set:
        return [generate_accuracy_list(lp_evaluation_dir_, max_iter=max_iter) for max_iter in max_iter_set]

    if tol_set:
        return [generate_accuracy_list(lp_evaluation_dir_, tol=tol) for tol in tol_set]




def generate_accuracy_plot(accuracy_lists, title, legend_data):
    test_rate_set = [1.-_ for _ in DEFAULT_TRAIN_RATE_SET]

    plt_list = []
    for al in accuracy_lists:
        plt_list.append(plt.plot(DEFAULT_TRAIN_RATE_SET, al, '-o'))   
    plt_list = [tuple(_) for _ in plt_list]     

    plt.legend((plt_list), tuple([str(_) for _ in legend_data]), loc='lower right', shadow=True)
    plt.xlabel('Percentage of data are used for training')
    plt.ylabel('Accuracy')
    plt.title(title)
    plt.show()

    plt.show()


def plot_accuracy(lp_evaluation_dir_):

    def plot_accuracy_for_various_n_neighbors():
        target_name = 'n_neighbors'
        n_neighbors_set = [5, 10, 20, 30]
        accuracy_lists = generate_accuracy_lists(lp_evaluation_dir_, n_neighbors_set=n_neighbors_set)
        generate_accuracy_plot(accuracy_lists, 'Accuracy for varous ' + target_name, [str(_)+' neighbors' for _ in n_neighbors_set])

    def plot_accuracy_for_various_max_iter(): 
        target_name = 'max iterations'
        max_iter_set = [100, 200, 500, 1000]
        accuracy_lists = generate_accuracy_lists(lp_evaluation_dir_, max_iter_set=max_iter_set)
        generate_accuracy_plot(accuracy_lists, 'Accuracy for varous ' + target_name, [str(_)+' iter' for _ in max_iter_set])
        print accuracy_lists

    def plot_accuracy_for_various_tol(): 
        target_name = 'tol values'
        tol_set = [0.000001, 0.00001, 0.0001, 0.0001]
        accuracy_lists = generate_accuracy_lists(lp_evaluation_dir_, tol_set=tol_set)
        generate_accuracy_plot(accuracy_lists, 'Accuracy for varous ' + target_name, [str(_)+' tol' for _ in tol_set])

    def acc_test():
        accuracy_lists = [[0.65384615384615385, 0.95833333333333337, 0.95652173913043481, 1.0, 0.94999999999999996], [0.62068965517241381, 0.95833333333333337, 0.95833333333333337, 1.0, 0.9375], [0.91666666666666663, 0.88888888888888884, 0.95454545454545459, 0.75, 0.95652173913043481], [0.70967741935483875, 0.95833333333333337, 0.85185185185185186, 0.95454545454545459, 0.94117647058823528]]
        tol_set = [0.000001, 0.00001, 0.0001, 0.001]
        generate_accuracy_plot(accuracy_lists, 'test', [str(_)+' tol' for _ in tol_set])

    # plot_accuracy_for_various_n_neighbors()
    # plot_accuracy_for_various_max_iter()
    # plot_accuracy_for_various_tol()
    acc_test()

    
    

