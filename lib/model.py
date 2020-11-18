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
    
    