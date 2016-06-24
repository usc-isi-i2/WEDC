# -*- coding: utf-8 -*-
# @Author: ZwEin
# @Date:   2016-06-20 14:39:06
# @Last Modified by:   ZwEin
# @Last Modified time: 2016-06-24 11:30:48


# import sys
# from math import log
# from math import sqrt
# from operator import itemgetter

from knn import KNNGraph

class Graph():

    WEDC_GRAPH_TYPE_LSH = 'lsh'
    WEDC_GRAPH_TYPE_KNN = 'knn'

    def __init__(self, graph_type='knn'):
        self.set_graph_type(graph_type)


    def set_graph_type(self, graph_type='knn'):
        # lsh / knn
        st = graph_type.lower()
        if graph_type.lower() not in [WEDC_GRAPH_TYPE_LSH, WEDC_GRAPH_TYPE_KNN] :
            raise Exception(graph_type + ' is not a source type, which should be "lsh" or "knn"')

        self.graph_type = graph_type

        if graph_type == WEDC_GRAPH_TYPE_LSH:
            pass # to be implemented
        elif graph_type == WEDC_GRAPH_TYPE_KNN:
            self.graph = KNNGraph()

    def build(self, graph_input, output=None, n_neighbors=10):
        pass

        


    
