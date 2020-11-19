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
    closest_cluster_dist = float("inf")
    closest_cluster = clusters[0]
    closest_index = 0

    for index, cluster in enumerate(clusters):
        dist = norm(cluster.pos - point)

        if dist < closest_cluster_dist:
            closest_index = index
            closest_cluster = cluster
            closest_cluster_dist = dist


    return closest_index, closest_cluster