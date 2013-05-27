import numpy as np
import os
from sklearn import metrics
from sklearn.metrics import pairwise_distances
from util.utilities import Utils

fn = os.path.join(os.path.dirname(__file__), 'data/zdata.txt')
print "opening file %s" % fn
points = np.loadtxt(fn)

#normalize using z-score or sigmoid
points = Utils.zscore(points)
#points = Utils.sigmoid(points)
#points = whiten(points)


minLabels = np.loadtxt(os.path.join(os.path.dirname(__file__), 'data/tmp/minLabels.txt'))

#print 'sc kmeans2 %s ' % metrics.silhouette_score(points, idx, metric='euclidean')
print 'sc kmeans user %s ' % metrics.silhouette_score(points, minLabels, metric='euclidean')