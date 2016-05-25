import matplotlib.pyplot as plt
import numpy as np

from wedc.domain.core.ml.classifier.label_propagation import labelprop

DEFAULT_NUM_OF_TESTS = 50
DEFAULT_TEST_RATE = .9
DEFAULT_N_NEIGHBORS = 5
DEFAULT_MAX_ITER = 200
DEFAULT_TOL = 0.000001

DEFAULT_TARGETS = ['Massage', 'Escort', 'Job_ads']

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
        # print accuracy_lists

    def plot_accuracy_for_various_tol(): 
        target_name = 'tol values'
        tol_set = [0.000001, 0.00001, 0.0001, 0.001]
        accuracy_lists = generate_accuracy_lists(lp_evaluation_dir_, tol_set=tol_set)
        generate_accuracy_plot(accuracy_lists, 'Accuracy for varous ' + target_name, [str(_)+' tol' for _ in tol_set])

    def acc_test():
        accuracy_lists = [[0.65384615384615385, 0.95833333333333337, 0.95652173913043481, 1.0, 0.94999999999999996], [0.62068965517241381, 0.95833333333333337, 0.95833333333333337, 1.0, 0.9375], [0.91666666666666663, 0.88888888888888884, 0.95454545454545459, 0.75, 0.95652173913043481], [0.70967741935483875, 0.95833333333333337, 0.85185185185185186, 0.95454545454545459, 0.94117647058823528]]
        tol_set = [0.000001, 0.00001, 0.0001, 0.001]
        generate_accuracy_plot(accuracy_lists, 'test', [str(_)+' tol' for _ in tol_set])

    # plot_accuracy_for_various_n_neighbors()
    # plot_accuracy_for_various_max_iter()
    plot_accuracy_for_various_tol()
    # acc_test()

    
#######################################################
#   Confusion Matrix
#######################################################   

# http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html

def generate_confusion_matrix_plot(cm, target_names, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(target_names))
    plt.xticks(tick_marks, target_names, rotation=45)
    plt.yticks(tick_marks, target_names)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def plot_confusion_matrix(lp_evaluation_dir_):
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.metrics import confusion_matrix

    output = labelprop.do_evaluation(lp_evaluation_dir_, num_of_tests=1, test_rate=.9, n_neighbors=10, max_iter=100, tol=0.000001)

    for rnd in output:
        round_id = rnd[0]
        accuracy = rnd[1]

        # label data
        label_data = rnd[3]
        y_test = label_data[0]
        y_pred = label_data[1]
        valid_pid_set = label_data[2]

        # fig = plt.figure()

        # Compute confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        np.set_printoptions(precision=2)
        print('Confusion matrix, without normalization')
        print(cm)
        # plt.subplot(221)
        plt.figure()
        generate_confusion_matrix_plot(cm, DEFAULT_TARGETS)

        # Normalize the confusion matrix by row (i.e by the number of samples
        # in each class)
        cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print('Normalized confusion matrix by the number of samples in each class')
        print(cm_normalized)
        # plt.subplot(222)
        plt.figure()
        generate_confusion_matrix_plot(cm_normalized, DEFAULT_TARGETS, title='Normalized confusion matrix (samples in each class)')

        # Normalize the confusion matrix by row (i.e by the number of all samples)
        cm_normalized = cm.astype('float') / cm.sum(axis=0)
        print('Normalized confusion matrix by the number of samples')
        print(cm_normalized)
        # plt.subplot(223)
        plt.figure()
        generate_confusion_matrix_plot(cm_normalized, DEFAULT_TARGETS, title='Normalized confusion matrix (all samples)')


        # plt.subplot_tool()

        plt.show()

        break

    

    # plt.show()


#######################################################
#   Histogram for precision, recall and f1-score
####################################################### 

def generate_histogram_plot(target_names, precisions, recalls, fscores):
    N = len(target_names)   

    ind = np.arange(N)  # the x locations for the groups
    width = 0.1       # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, precisions, width, color='skyblue')
    rects2 = ax.bar(ind + width, recalls, width, color='palegreen')
    rects3 = ax.bar(ind + width*2, fscores, width, color='bisque')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('value')
    ax.set_title('Precision & Recall & F1-score values')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(tuple(target_names))

    ax.legend((rects1[0], rects2[0], rects3[0]), ('Precision', 'Recall', 'F1-score'), loc='lower right', shadow=True)


    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%.3f' % float(height),
                    ha='center', va='bottom')

    # autolabel(rects1)
    # autolabel(rects2)
    # autolabel(rects3)

    plt.show()

def plot_prf(lp_evaluation_dir_):
    from sklearn.metrics import precision_recall_fscore_support

    output = labelprop.do_evaluation(lp_evaluation_dir_, num_of_tests=1, test_rate=.9, n_neighbors=10, max_iter=100, tol=0.000001)

    for rnd in output:
        round_id = rnd[0]
        accuracy = rnd[1]

        # label data
        label_data = rnd[3]
        y_test = label_data[0]
        y_pred = label_data[1]
        valid_pid_set = label_data[2]

        precisions, recalls, fscores, _ = precision_recall_fscore_support(y_test, y_pred)
        print precisions
        print recalls
        print fscores
        generate_histogram_plot(DEFAULT_TARGETS, precisions, recalls, fscores)
        break



