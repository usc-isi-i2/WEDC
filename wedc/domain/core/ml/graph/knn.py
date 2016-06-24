import math
import heapq
import random   

class KNNGraph():

    KNN_GRAPH_DISTANCE_TYPE_EUCLIDEAN = 'euclidean'
    KNN_GRAPH_DISTANCE_TYPE_JACCARD = 'jaccard'
    KNN_GRAPH_DISTANCE_TYPE_COSINE = 'cosine'

    def __init__(self, dist_type='euclidean'):
        self.set_graph_distance_type(dist_type)

    def set_graph_distance_type(self, dist_type):
        if dist_type not in [KNNGraph.KNN_GRAPH_DISTANCE_TYPE_EUCLIDEAN, KNNGraph.KNN_GRAPH_DISTANCE_TYPE_JACCARD, KNNGraph.KNN_GRAPH_DISTANCE_TYPE_COSINE]:
            raise Exception('graph distance type should be "euclidean", "jaccard" or "cosine"')
        self.dist_type = dist_type

    def validate_n_neighbors(self, n_neighbors):
        if n_neighbors < 1:
            raise Exception('the value for n_neighbors should be bigger than zero')

    def calc_distance(self, node, data, n_neighbors=None):
        def euclidean_distance(x,y):
            return math.sqrt(sum([(a-b)**2 for (a,b) in zip(x,y)]))

        def jaccard_distance(x,y,weighted=True):
            x = [round(_,2) for _ in x]
            y = [round(_,2) for _ in y]
            set1, set2 = set(x), set(y)
            if not sum(set1) or not sum(set2):
                return 0
            if weighted:
                intersection = set1 & set2
                union = set1 | set2
                return 1 - sum(intersection) / float(sum(union))
            else:
                return 1 - len(set1 & set2) / float(len(set1 | set2))
                # return 1 - sum([min(a,b) for (a,b) in zip(x,y)]) / sum([max(a,b) for (a,b) in zip(x,y)])

        def cosine_distance(x,y):
            return 1 - float(sum([a*b for (a,b) in zip(x,y)])) / (math.sqrt(sum([_**2 for _ in x])) * math.sqrt(sum([_**2 for _ in y])))

        def knn(data, k, distance):
            def nn(x):
                # get k nearest neighbors (itself included)
                closestPoints = heapq.nsmallest(k, enumerate(data), key=lambda y: distance(x, y[1]))

                # load distance
                closestPoints = [(node_id, distance(x, vector)) for node_id, vector in closestPoints]

                # normalize, and weighed (1-)
                sum_values = sum([_[1] for _ in closestPoints])
                closestPoints = [(node_id, 1-float(dis)/sum_values) for node_id, dis in closestPoints]
                return closestPoints

            return nn

        self.validate_n_neighbors(n_neighbors)
        n_neighbors += 1 # not including itself

        if self.dist_type == KNNGraph.KNN_GRAPH_DISTANCE_TYPE_EUCLIDEAN:
            nn = knn(data, n_neighbors, euclidean_distance)
        elif self.dist_type == KNNGraph.KNN_GRAPH_DISTANCE_TYPE_JACCARD:
            nn = knn(data, n_neighbors, euclidean_distance)
        elif self.dist_type == KNNGraph.KNN_GRAPH_DISTANCE_TYPE_COSINE:
            nn = knn(data, n_neighbors, euclidean_distance)

        return nn(node)[1:]



    def build(self, graph_input, output=None, n_neighbors=10):

        self.validate_n_neighbors(n_neighbors)

        size = len(graph_input)
        if n_neighbors > size:
            raise Exception('cannot find {0} neighbors for a node in the graph with {1} nodes'.format(n_neighbors, size))

        # load data
        pid_set = [_[0] for _ in graph_input]
        X = [_[1] for _ in graph_input]
        y = [_[2] for _ in graph_input]

        graph = []

        post_weight_sum_dict = {}
        for i in range(size):
            post_id = pid_set[i]
            graph_item = [post_id, y[i]]
            knn_pairs = self.calc_distance(X[i], X, n_neighbors=n_neighbors)
            # post_weight_sum_dict[str(post_id)] = sum(post_k_distances) # for sort post by weight only

            post_neighbors = []
            for idx in range(n_neighbors):
                post_neighbors.append([pid_set[knn_pairs[idx][0]], knn_pairs[idx][1]])

            graph_item.append(post_neighbors)
            graph.append(graph_item) # graph.append(str(graph_item)), if reutrn graph is not required

        if output:
            output_fh = open(output, 'wb')
            for item in [str(_) for _ in graph]:
                output_fh.write(item+'\n')
            output_fh.close()

        # sort post by weight
        # if top_k_rate:
        #     top_k_size = int(top_k_rate * size)
        #     post_weight_sum_dict = sorted(post_weight_sum_dict.iteritems(), key=lambda x: x[1], reverse=True)
        #     post_weight_sum_dict = [int(_[0]) for _ in post_weight_sum_dict]
        #     return post_weight_sum_dict[:top_k_size]

        return graph




"""
from sklearn.neighbors import NearestNeighbors
from sklearn import preprocessing
import numpy as np
import random


def do_knn(X, output, post_labels=None, n_neighbors=10, algorithm='ball_tree'):
    n_neighbors += 1
    size = len(X)
    # X = np.array(np.mat(';'.join(post_vectors)))
    
    nbrs = NearestNeighbors(n_neighbors=n_neighbors, algorithm=algorithm).fit(X)
    # Because the query set matches the training set, the nearest neighbor of each point is the point itself, at a distance of zero.
    distances, indices = nbrs.kneighbors(X)
    distances = preprocessing.normalize(distances, norm='l2')

    # sort post by weight
    post_dict = {}
    k_rate = 0.005
    top_k = int(k_rate * size)

    # load post labels
    if not post_labels:
        post_labels = [0]*size

    training_index = list(np.random.choice(size-1, int(size*.1), replace=False))
    training_index = [_+1 for _ in training_index]
    # print 'training size:', len(training_index)
    training_index.sort()

    testing_index = []
    testing_labels = []
    training_labels = []
    for i in range(len(post_labels)):
        post_id = i+1
        if post_id in training_index:
            training_labels.append(post_labels[i])
        else:
            testing_labels.append(post_labels[i])
            testing_index.append(post_id)
            post_labels[i] = 0
            
    # print training_labels
    # print training_index
    # print testing_index

    graph = []
    for i in range(0, size):
        post_id = i + 1
        # line = X[i].strip().split(' ') 
        line = X[i]
        post_indices = indices[i]
        post_k_distances = distances[i]
        post_dict[str(post_id)] = sum(post_k_distances)

        # if max([float(_) for _ in line]) == 0:
        #     post_labels[post_id] = 1
        graph_item = [post_id, post_labels[i]]

        post_neighbors = []
        for idx in range(n_neighbors):
            if post_id == post_indices[idx] + 1:
                continue
            post_neighbors.append([post_indices[idx]+1, 1-post_k_distances[idx]])
        graph_item.append(post_neighbors)
        graph.append(str(graph_item))

    output_fh = open(output, 'wb')
    for node in graph:
        output_fh.write(node+'\n')
    output_fh.close()

    post_dict = sorted(post_dict.iteritems(), key=lambda x: x[1], reverse=True)
    post_dict = [int(_[0]) for _ in post_dict]

    return post_dict[:top_k], top_k, training_index, training_labels, testing_index, testing_labels


def build_graph(input, output, n_neighbors=10, algorithm='ball_tree'):
    with open(input, 'rb') as f:
        lines = f.readlines()
        return do_knn(lines, output)
"""
