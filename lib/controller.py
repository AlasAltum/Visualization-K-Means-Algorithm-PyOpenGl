import sys

import glfw
import numpy as np


# A class to store the application control
class Controller:
    def __init__(self):
        self.point_size = 0.1
        self.cluster_size = 0.3
        self.mouse_pos = (0, 0)
        self._data_dimensions = 0
        self.x_axis = 0
        self.x_name = ""
        self.y_axis = 0
        self.y_name = ""
        self.z_axis = 0
        self.z_name = ""
        self.iterations = 0
        self.iteration_forward = False
        self.dataframe = 0

    def advance_iteration(self):
        self.iterations += 1

    def set_up(self, df):
        self._data_dimensions = len(df.columns) - 1


# We will use the global controller as communication with the callback function
_controller = Controller()


def on_key(window, key, scancode, action, mods):

    global _controller

    if key == glfw.KEY_RIGHT:
        _controller.iteration_forward = True

    elif key == glfw.KEY_X:
        _controller.x_axis = (_controller.x_axis + 1) % _controller._data_dimensions

    elif key == glfw.KEY_Y:
        _controller.y_axis = (_controller.y_axis + 1) % _controller._data_dimensions

    elif key == glfw.KEY_Z:
        _controller.z_axis = (_controller.z_axis + 1) % _controller._data_dimensions
