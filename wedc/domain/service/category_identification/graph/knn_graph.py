
from sklearn.neighbors import NearestNeighbors
from sklearn import preprocessing
import numpy as np


# X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])

# X = np.array([])
# X = np.append(X, [[1, 1, 0, 0]], axis=0)
# X = np.append(X, [[0, 0, 0, 0]], axis=0)
# print X

# X = np.array(np.mat('1 2; 3 4'))
# X = [[0, 0, 2], [1, 0, 0], [0, 0, 1]]
# nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(X)
# distances, indices = nbrs.kneighbors(X)
# print indices


def build_graph(input, output, n_neighbors=5, algorithm='ball_tree'):

    
    input_fh = open(input, 'rb')
    output_fh = open(output, 'wb')

    lines = input_fh.readlines()[:10]
    size = len(lines)
    lines = ';'.join(lines)
    X = np.array(np.mat(lines))


    nbrs = NearestNeighbors(n_neighbors=n_neighbors+1, algorithm=algorithm).fit(X)
    # Because the query set matches the training set, the nearest neighbor of each point is the point itself, at a distance of zero.
    distances, indices = nbrs.kneighbors(X)

    distances = preprocessing.normalize(distances, norm='l2')


    for post_id in range(0, size):    
        post_indices = indices[post_id][1:]
        post_k_distances = distances[post_id][1:]
        

        # change to start from 1 for lab propagation library input format
        graph_item = [post_id+1, 0]

        post_neighbors = []
        for idx in range(n_neighbors):
            post_neighbors.append([post_indices[idx]+1, post_k_distances[idx]])
        graph_item.append(post_neighbors)

        output_fh.write(str(graph_item))



    # output.write(' '.join(vector) + '\n')


    input_fh.close()
    output_fh.close()

