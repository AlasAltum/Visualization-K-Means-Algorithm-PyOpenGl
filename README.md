# Visualization-K-Means-Algorithm-PyOpenGl
Representing K-Means Algorithm with PyOpenGL.

This script was made to show how the K Means Algorithm works.


## Installation
You need Python 3, and OpenGL in your GPU. Besides, you can install the packages by executing the following command in the directory where clustering_gl is located:

```
pip install -r requirements.txt
```

## How to execute:
By calling this file:
```
python clustering_gl.py --n_samples -csv_filanem --n_clusters

optional arguments:
  -h, --help          show this help message and exit
  --n_samples N       Size of the sample
  --csv_filename csv  Filename
  --n_clusters k      Number of clusters
```

You can choose a csv file which is going to be processed by pandas library. This will use take your data to perform the clustering algorithm.
The N samples argument lets you choose how many points to see. Prefer low N values for low performance computers.
The k is the number of clusters.

## Controls:
By pressing right arrow you can add an iteration, which reallocates the clusters according to the K means algorithm.

By pressing X and Y you can change the X axis or the Y axis.

# TODOs:

* Add a third dimension.
* Display the name of the axis each time an axis is changed.
* Show SSE for each cluster and all clusters at the end of each iteration.
* Graph SSE
* Make available to add more Clusters, so one can Graph SSE vs K number of clusters and choose the best K to fit the data.
