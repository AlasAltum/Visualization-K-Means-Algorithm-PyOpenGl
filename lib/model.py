# This module contains the logic
from numpy.random import rand
from numpy.linalg import norm

class Cluster:

    def __init__(self, pos, color = None):
        self.pos = pos
        self.color = rand(3) if color is None else color
        self.GPUshape = 0

    def distance_to_cluster(self, point):
        return norm(self.pos - point)
    

def get_closest_cluster(clusters, point):
    closest_cluster = float("inf")

    for index, cluster in enum(clusters):
        if norm(cluster.pos - point) < closest_cluster:
            closest_cluster = cluster

    return index, closest_cluster