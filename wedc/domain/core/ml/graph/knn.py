    
from sklearn.neighbors import NearestNeighbors
from sklearn import preprocessing
import numpy as np


def do_knn(post_vectors, output, n_neighbors=20, algorithm='ball_tree'):
    size = len(post_vectors)
    X = np.array(np.mat(';'.join(post_vectors)))
    
    nbrs = NearestNeighbors(n_neighbors=n_neighbors, algorithm=algorithm).fit(X)
    # Because the query set matches the training set, the nearest neighbor of each point is the point itself, at a distance of zero.
    distances, indices = nbrs.kneighbors(X)
    distances = preprocessing.normalize(distances, norm='l2')

    # sort post by weight
    post_dict = {}
    k_rate = 0.005
    top_k = int(k_rate * size)

    graph = []
    for post_id in range(0, size):
        line = post_vectors[post_id].strip().split(' ') 
        post_indices = indices[post_id]
        post_k_distances = distances[post_id]

        post_dict[str(post_id)] = sum(post_k_distances)

        # change to start from 1 for lab propagation library input format
        if max([float(_) for _ in line]) == 0:
            graph_item = [post_id+1, 1]
        else:
            graph_item = [post_id+1, 0]
        post_neighbors = []
        for idx in range(n_neighbors):
            if post_id == post_indices[idx]:
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

    return post_dict[:top_k], top_k


def build_graph(input, output, n_neighbors=20, algorithm='ball_tree'):
    n_neighbors += 1

    with open(input, 'rb') as f:
        lines = f.readlines()
        return do_knn(lines, output)

