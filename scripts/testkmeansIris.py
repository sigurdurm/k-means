from sklearn import metrics
from sklearn.metrics import pairwise_distances
import os.path
import sys
from km.kmeans import KMeans
from sklearn import decomposition
import pylab
from util.utilities import Plot
from util.utilities import Utils
import numpy as np
import random
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from scipy.cluster.vq import *
from numpy import linalg as LA
from scipy.spatial import distance


data = 'data/iris-dat.dat'
#data = 'data/zdata.txt'
#data = 'data/zdata_incl_purchase.txt'
fn = os.path.join(os.path.dirname(__file__), data)
print "opening file %s" % fn

#f = open(fn)
#items = [map(int, line.strip().split()) for line in f.readlines()]
#f.close()

points = np.loadtxt(fn)
#import pdb;pdb.set_trace()

#normalize using z-score or sigmoid
points = Utils.zscore(points)
#points = Utils.sigmoid(points)
#points = whiten(points)

#PCA
#pca = decomposition.PCA(n_components=2)
#pca.fit(points)
#points = pca.transform(points)



# run kmeans
km = KMeans(showsubplots=False)
k,d,i = 3, 0.1, 10
initialMeans = np.zeros((k, len(points[0])))

minSSE = sys.maxint
minInitialMeans = np.zeros((k, len(points[0])))
minMeans = np.zeros((k, len(points[0])))
minLabels = np.zeros(len(points), dtype=int)

# initialize means
for count in xrange(10):
    initialMeans[:] = Utils.getInitialMeans(points, k)    
    print "Initial Means: \n%s" % initialMeans
    
    means = np.zeros((k, len(points[0])))
    means[:] = initialMeans
    finalmeans, labels, SSE = km.run(points, means, numberOfClusters=k, threshold=d, maxiterations=i)
    print "final means: %s" % finalmeans
    
    if SSE < minSSE:
        print '**New min SSE %s' % SSE
        minSSE = SSE
        minInitialMeans[:] = initialMeans
        pprint('Min initial means\n%s' % initialMeans)
        minMeans[:] = finalmeans
        minLabels[:] = labels
        
print "min SSE: %s" % minSSE
print "min Initial means: %s" % minInitialMeans
print "min means: %s" % minMeans

np.savetxt(os.path.join(os.path.dirname(__file__), 'data/tmp/minLabels.txt'), minLabels)

res, idx = kmeans2(points,k)
print 'kmeans2 means %s' % res
totalsse = 0
        
#TODO write more efficently
for i in xrange(len(points)):
    cluster = idx[i]
    point = points[i]
    totalsse += np.sqrt(np.sum((point - res[cluster])**2))**2
    
print "min SSE2: %s" % minSSE

#fig = plt.figure()
#ax3D = fig.add_subplot(222, projection='3d')
#availcolors = [[0.4,1,0.4],[1,0.4,0.4],[0.5,0.5,1],[0.8,0.1,1],[0.8,1,0.1]]
#colors = [availcolors[int(i)] for i in idx]
#ax3D.scatter(points[:, 0], points[:, 1], points[:, 2], s=10, c=colors, marker='o') 
###
#ax3D.plot(res[:,0],res[:,1],res[:,2], marker='o', markersize=20, linewidth=0, c='none')
#ax3D.plot(res[:,0],res[:,1],res[:,2], marker='x', markersize=20, linewidth=0)
#
#fig = plt.figure()
#ax3D = fig.add_subplot(111, projection='3d')
#availcolors = [[0.4,1,0.4],[1,0.4,0.4],[0.5,0.5,1],[0.8,0.1,1],[0.8,1,0.1]]
#colors = [availcolors[int(i)] for i in minLabels]
#ax3D.scatter(points[:, 0], points[:, 1], points[:, 2], s=30, c=colors, marker='o') 
###
#ax3D.plot(minMeans[:,0],minMeans[:,1],minMeans[:,2], marker='o', markersize=40, linewidth=0, c='none')
#ax3D.plot(minMeans[:,0],minMeans[:,1],minMeans[:,2], marker='x', markersize=40, linewidth=0)



#print 'sc kmeans2 %s ' % metrics.silhouette_score(points, idx, metric='euclidean')
#print 'sc kmeans user %s ' % metrics.silhouette_score(points, minLabels, metric='euclidean')

#Plot.plotPoints(points, idx, title='final kmeans2')
#Plot.plotMeans(res)
#pylab.show()

Plot.plotPoints(points, minLabels, title='final')
Plot.plotMeans(minMeans)
pylab.show()
