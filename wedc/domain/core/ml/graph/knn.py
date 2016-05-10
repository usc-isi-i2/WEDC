    
from sklearn.neighbors import NearestNeighbors
from sklearn import preprocessing
import numpy as np


def build_graph(input, output, n_neighbors=40, algorithm='ball_tree'):
    n_neighbors += 1
    input_fh = open(input, 'rb')
    output_fh = open(output, 'wb')
    lines = input_fh.readlines()[:100]
    size = len(lines)
    X = np.array(np.mat(';'.join(lines)))
    print X
    nbrs = NearestNeighbors(n_neighbors=n_neighbors, algorithm=algorithm).fit(X)
    # Because the query set matches the training set, the nearest neighbor of each point is the point itself, at a distance of zero.
    distances, indices = nbrs.kneighbors(X)
    distances = preprocessing.normalize(distances, norm='l2')

    for post_id in range(0, size):    
        post_indices = indices[post_id]
        post_k_distances = distances[post_id]
        # change to start from 1 for lab propagation library input format
        if max([float(_) for _ in lines[post_id].split(' ')]) == 0:
            graph_item = [post_id+1, 1]
        else:
            graph_item = [post_id+1, 0]
        post_neighbors = []
        for idx in range(n_neighbors):
            if post_id == post_indices[idx]:
                continue
            post_neighbors.append([post_indices[idx]+1, 1-post_k_distances[idx]])
        graph_item.append(post_neighbors)
        output_fh.write(str(graph_item)+'\n')

    input_fh.close()
    output_fh.close()

