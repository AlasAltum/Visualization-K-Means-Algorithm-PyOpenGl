# coding=utf-8

"""
Clustering  

Respecto a los requisitos que planeo agregar: 
1) Se pueden entregar datos de varias dimensiones.
2) Los centroides de los clusters se representan de manera distinta a los puntos.
3) Cada punto variará su color (veré si combiene también la forma) según el cluster más cercano en esa iteración.
4) Se puede avanzar en la iteración con la flecha derecha. Quizás en una próxima iteración agregue la capacidad de retroceder en mi programa.
5) Se desplegará también información en la consola.
6) Al apretar la tecla X se cambian los ejes. 
"""


import sys
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

import glfw
import numpy as np
import OpenGL.GL.shaders
import argparse
from OpenGL.GL import *

import lib.basic_shapes as bs
import lib.easy_shaders as es
import lib.obj_handler as obj_reader
import lib.transformations as tr
from lib.controller import _controller, on_key
from lib.model import Cluster, get_closest_cluster

ALPHA = 0.1

# Execute just when this is the script called
# Not when it is imported
if __name__ == "__main__":

    # Argparse
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "--n_samples", metavar="N", type=int, help="Size of the sample", default=100
    )

    parser.add_argument(
        "--csv_filename",
        metavar="csv",
        help="Filename",
        default="temuco_cleaned_data.csv",
    )

    parser.add_argument(
        "--n_clusters", metavar="k", type=int, help="Number of clusters", default="4"
    )

    args = vars(parser.parse_args())

    n_samples = args['n_samples']
    csv_file = args['csv_filename']
    n_clusters = args['n_clusters']

    df = pd.read_csv(csv_file)
    # print(f'Data Sample:\n{df.head()}')

    # init_data.values[i] correspondos to the ith_row
    # Since OpenGL works with ranges from -1 to 1
    # We want all data to fit into [0, 1] interval
    min_max_scaler = MinMaxScaler(feature_range=(-1, 1))

    numeric_dimensions = 0
    # Apply transform only to numeric type of data
    # Filtering non numeric data
    for col_name, col_type in zip(df.columns, df.dtypes):

        if col_type != np.dtype("O"):
            df[[col_name]] = min_max_scaler.fit_transform(df[[col_name]])
            numeric_dimensions += 1

        else:
            df = df.drop(columns=col_name)

    # Take a sample
    df = df.sample(n=n_samples, random_state=5)
    df['Cluster'] = 0
    print(df)
    n_dimensions = numeric_dimensions

    # Creating the clusters and their positions
    clusters = tuple(Cluster(pos=(np.random.rand(n_dimensions) * 2 - 1)) for _ in range(n_clusters))
    _controller.set_up(df)

    # df.shape = (n_samples, n_cols)

    # Uncomment this to see data after filtering and sampling
    # print(f'Data Sample after filtering and sampling:\n{df}')

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 1200
    height = 800

    window = glfw.create_window(width, height, "Showing Clustering algorithm", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Defining shader programs
    pipeline = es.SimpleTransformColorChangeShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    # Setting up the projection transform
    gpuAxis = es.toGPUShape(bs.createAxis())
    gpuPoints = [] # es.toGPUShape(bs.createSmallColorQuad(1, 1, 1))

    # Generating the clusters
    for cluster in clusters:
        cluster.gpuShape = es.toGPUShape(bs.createColorTriangle(*cluster.color))
        gpuPoints.append(es.toGPUShape(bs.createSmallColorQuad(*cluster.color)))
    
    # Assign a cluster to each point 
    for point_index, point in enumerate(df.values):
        cluster_index, closest_cluster = get_closest_cluster(clusters, point[:-1])
        df['Cluster'].values[point_index] = cluster_index


    identity = tr.identity()

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Drawing axis
        glUniformMatrix4fv(
            glGetUniformLocation(pipeline.shaderProgram, "transform"),
            1,
            GL_TRUE,
            identity,
        )
        pipeline.drawShape(gpuAxis, mode=GL_LINES)


        # Drawing clusters
        for cl_index, cluster in enumerate(clusters):

            # Setting color
            glUniform3f(
                glGetUniformLocation(pipeline.shaderProgram, "color"), *cluster.color
                )

            # Draw every point which is closer to this cluster
            for point in df[df['Cluster'] == cl_index].values:
                # import pdb
                # pdb.set_trace()

                glUniformMatrix4fv(
                    glGetUniformLocation(pipeline.shaderProgram, "transform"),
                    1,
                    GL_TRUE,
                    tr.translate(point[_controller.x_axis],
                                point[_controller.y_axis],
                                point[_controller.z_axis]
                    ),
                )
                pipeline.drawShape(gpuPoints[cl_index])

            # now draw cluster
            glUniformMatrix4fv(
                glGetUniformLocation(pipeline.shaderProgram, "transform"),
                1,
                GL_TRUE,
                tr.translate(cluster.pos[_controller.x_axis],
                            cluster.pos[_controller.y_axis],
                            cluster.pos[_controller.z_axis]
                ),
            )
            pipeline.drawShape(cluster.gpuShape)

        if _controller.iteration_forward:

            mean_values  = df.groupby('Cluster').agg(np.mean) 

            # Recompute cluster positions:
            for cl_index, cluster in enumerate(clusters):
                try:
                    cluster.pos = cluster.pos * (1 - ALPHA) + mean_values.values[cl_index] * ALPHA

                except IndexError:
                    cluster.pos = cluster.pos # CC

            # Recompute closest cluster centroid for each point
            for point_index, point in enumerate(df.values):
                cluster_index, closest_cluster = get_closest_cluster(clusters, point[:-1])
                df['Cluster'].values[point_index] = cluster_index
            
            _controller.iterations += 1
            _controller.iteration_forward = False

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
