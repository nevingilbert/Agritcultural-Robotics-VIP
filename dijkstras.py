import numpy as np
import pickle
from figures import plotPoints, plotPointsLine
from utils import Point

class dijkstras:
    # class Node:
        # def __init__(v, parent, path_len):
        #     self.v = v
        #     self.parent = parent
        #     self.path_len = path_len
        #
        # def get_parent():
        #     return self.parent
        #
        # def update_path_len(l):
        #     self.path_len = l

    def __init__(self, distance_matrix, start_v, end_v):
        self.distance_matrix = distance_matrix
        self.start_v = start_v
        self.end_v = end_v
        self.parents = [None]*len(distance_matrix)
        self.children = [[] for i in range(len(distance_matrix))]
        self.curr_shortest = [np.inf]*len(distance_matrix)
        self.curr_shortest[self.start_v] = 0

    def get_distance(self, v1, v2):
        """return distance if connected, and -1 if not connected"""
        return self.distance_matrix[v1][v2]

    def get_adj_vertices(self, v):
        """list of vertices adjcent to v"""
        return [i for i in range(len(self.distance_matrix[v]))
                if (self.parents[v] != i) & (self.distance_matrix[v][i] != -1) & (i != v)]
                    # not looping, not disconnected, not self

    def update_path_v(self, candidate_parent, v):
        """update the path if from parent to v is shorter than the known path to v
        otherwise don't change anything"""
        new_len = self.curr_shortest[candidate_parent] + self.distance_matrix[candidate_parent][v]
        # print('------------------')
        # print('-- candidate_parent: ', candidate_parent)
        # print('-- v: ', v)
        # print('-- new len: ', new_len)
        # print('-- old len: ', self.curr_shortest[v])
        if new_len < self.curr_shortest[v]:
            if self.parents[v] and (v in self.children[self.parents[v]]):
                self.children[self.parents[v]].remove(v)
            self.parents[v] = candidate_parent
            self.children[candidate_parent].append(v)
            self.curr_shortest[v] = new_len

            # update following nodes' shortest paths' length
            node_stack = []
            curr_node = v
            node_stack.append(v)
            explored_children = []
            while len(node_stack) > 0:
                # print('-- node_stack: ', node_stack)
                curr_node = node_stack.pop()
                # print('-- curr_node: ', curr_node)
                # print('-- curr_node\'s children: ', self.children[curr_node])
                for child in self.children[curr_node]:
                    if child not in explored_children:
                        self.curr_shortest[child] = self.curr_shortest[curr_node] + self.distance_matrix[child][curr_node]
                        node_stack.append(child)
                        explored_children.append(child)
        # print('-----------------')


    def calculate_dijkstras(self):
        prior = []
        explored = [False]*len(self.distance_matrix)
        explored[self.end_v] = True
        curr_node = self.start_v
        prior.append(curr_node)
        while len(prior) > 0:
            # print('====================')
            # print('prior: ', prior)
            curr_node = prior.pop()
            # print('curr_node: ', curr_node)
            explored[curr_node] = True
            adj_nodes = self.get_adj_vertices(curr_node)
            for adj_node in adj_nodes:
                # print('adj_node: ', adj_node)
                self.update_path_v(curr_node, adj_node)
                if not explored[adj_node]:
                    prior.append(adj_node)

    def get_shortestpath(self):
        """full path from start_v to end_v
        use DFS for future optimization"""
        path = []
        curr_node = self.end_v
        while curr_node != self.start_v:
            path.append(curr_node)
            curr_node = self.parents[curr_node]

        path.append(self.start_v)
        return [path[len(path) - i] for i in range(1,len(path)+1)]

distance_matrix_rtt = pickle.load(open('distance_matrix.pkl','rb'))
points = list(distance_matrix_rtt.keys())
distance_matrix = [[-1]*len(points) for _ in range(len(points))]

for p1 in points:
    distance_matrix[list(points).index(p1)][list(points).index(p1)] = 0
    for p2 in distance_matrix_rtt[p1].keys():
        distance_matrix[points.index(p1)][points.index(p2)] = distance_matrix_rtt[p1][p2]
        distance_matrix[points.index(p2)][points.index(p1)] = distance_matrix_rtt[p1][p2]

start_v = 0  
end_v = len(points) - 1

algo = dijkstras(distance_matrix, start_v, end_v)
algo.calculate_dijkstras()
path = algo.get_shortestpath()
plot = [[points[p] for p in path], [points[0], points[len(points) - 1]]]
print(plot[0])
plotPointsLine(plot, 'FINAL')