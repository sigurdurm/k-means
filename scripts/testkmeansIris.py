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
from scipy.spatial import distance
from time import time
import glob

k,d,i = 3, 0.01, 20

#load data set
#data = 'data/iris-dat.dat'
#data = 'data/zdata-zscore.txt'
data = 'data/zdata-zscore-wo-outliers.txt'
#data = 'data/zdata_incl_purchase.txt'
#data = 'data/gen_zscore_data_shuffle_880MB.txt'
#data = 'data/multiple/genshiftmeans/0_gendata_shiftingmeans_zscore.dat'
fn = os.path.join(os.path.dirname(__file__), data)
print "opening file %s" % fn
points = np.loadtxt(fn)
#fninitcentroids = 'data/initialcentroids.txt' #zdata
#fninitcentroids = 'data/gen_initial_centroids_shuffle_880MB.txt'

#points = Utils.sigmoid(points)

#normalize using z-score or sigmoid
#points = Utils.zscore(points)

#PCA
#pca = decomposition.PCA(n_components=2)
#pca.fit(points)
#points = pca.transform(points)
#

#multiplefilepath = 'data/multiple/genshiftmeans/'
    
#Loading data points from multiple files, for SSE error in whole dataset
#files = glob.glob(os.path.join(os.path.dirname(__file__), multiplefilepath + '*zscore.dat'))
#files.sort()
#        
#points = np.loadtxt(files[9])
#        
#cfiles = glob.glob(os.path.join(os.path.dirname(__file__), multiplefilepath + '*_initialcentroids*'))
#cfiles.sort()
#fninitcentroids = cfiles[9]





# run kmeans
km = KMeans(showsubplots=False)

initialMeans = np.zeros((k, len(points[0])))

minSSE = sys.maxint
minInitialMeans = np.zeros((k, len(points[0])))
minMeans = np.zeros((k, len(points[0])))
minLabels = np.zeros(len(points), dtype=int)



    
# initialize means
numOfExperiments = 5 #number of random initial means experiments
for count in xrange(numOfExperiments):
    if numOfExperiments == 1:
        initialMeans[:] = np.loadtxt(os.path.join(os.path.dirname(__file__), fninitcentroids))
    else:
        initialMeans[:] = Utils.getInitialMeans(points, k)    
        
    print "Initial Means: \n%s" % initialMeans
    print "Initial SSE: %s" % Utils.calcSSE(points, initialMeans)
    
    means = np.zeros((k, len(points[0])))
    means[:] = initialMeans
    finalmeans, labels, SSE = km.run(points, means, numberOfClusters=k, threshold=d, maxiterations=i)
    print "final means: %s" % finalmeans

    if SSE < minSSE:
        print '**New min SSE %s' % SSE
        minSSE = SSE
        minInitialMeans[:] = initialMeans
        print 'Min initial means\n%s' % initialMeans
        minMeans[:] = finalmeans
        minLabels[:] = labels
        
print "min SSE: %s" % minSSE
print "min Initial means:\n %s" % minInitialMeans
print "min means:\n %s" % minMeans

#Plot.plotPoints(points, minLabels, title='final')
#Plot.plotMeans(minMeans)
#pylab.show()

    
#files = glob.glob(os.path.join(os.path.dirname(__file__), 'data/multiple/genshiftmeans/*s.dat')) #Multiple files
#files = glob.glob(os.path.join(os.path.dirname(__file__), 'data/multiple/sorted/wo outliers/original/*outliers.dat')) #Multiple files
#files = glob.glob(os.path.join(os.path.dirname(__file__), 'data/multiple/sorted/wo outliers/*outliers.dat')) #Multiple files
##files = glob.glob('/home/sigurdurm/Downloads/multiple/sortedtimestamp/*.dat') #Multiple files
#files.sort() #Multiple files
#rows = 5
#columns = 2
#f, test = plt.subplots(rows, columns, sharex='col', sharey='row')
#c = 0
#r = 0
#for x in xrange(len(files)):
#    f = files[x] #Multiple files
#    points = np.loadtxt(f) #Multiple files
#    print points
##    points = Utils.zscore(points)
#    print points
#    #PCA
##    pca = decomposition.PCA(n_components=2)
##    pca.fit(points)
##    points = pca.transform(points)
#    #
#    #np.savetxt(os.path.join(os.path.dirname(__file__), 'data/tmp/minLabels.txt'), minLabels)
#    
#    #initialMeans[:] = np.loadtxt(os.path.join(os.path.dirname(__file__), fninitcentroids))
#    #initialMeans[:] = Utils.getInitialMeans(points, k)
#    print 'run scipy kmeans2'
#    start = time()  
#    res, idx = kmeans2(points,3)
#    #res, idx = kmeans2(points,k, i)
#    end = time()
#    total = (end-start)
#    print 'total scipy kmeans2 time: %f' %total
#    print 'kmeans2 final means:\n %s' % res
#            
#    #Used as it is the same as used in the MR k-means
#    print "SSE2: %s" % Utils.calcSSE(points, res)
#    
##    availcolors = [[0.4,1,0.4],[1,0.4,0.4],[0.5,0.5,1],[0.8,0.1,1],[0.8,1,0.1]]
##    colors = [availcolors[int(i)] for i in idx]
##    print 'r c, %s %s' % (r,c)
##    test[r][c].scatter(points[:,0],points[:,1], c=colors)
###    test[j][i].scatter(res[:,0],res[:,1], marker='o', s = 50, linewidths=2, c='none')
###    test[j][i].scatter(res[:,0],res[:,1], marker='x', s = 50, linewidths=2, c='y')
###    pylab.show()
##    
##    c += 1
##    if (x+1) % 2 == 0:
##        r += 1
##        c = 0
#
#    color = [0.4, 0.8, 0.2]
#    plt.title('Real game data %s' %(x+1))
#    availcolors = [[0.4,1,0.4],[1,0.4,0.4],[0.5,0.5,1],[0.8,0.1,1],[0.8,1,0.1]]
#    colors = [availcolors[int(i)] for i in idx]
#    plt.scatter(points[:,0],points[:,1], c=colors)
#    
#    plt.scatter(res[:,0],res[:,1], marker='o', s = 500, linewidths=2, c='none')
#    plt.scatter(res[:,0],res[:,1], marker='x', s = 500, linewidths=2)
#    plt.savefig('%s_%s.png' % (x,'realdata 2d'))
#    plt.cla()
#    pylab.show()

#    fig = plt.figure()
#    ax3D = fig.add_subplot(111, projection='3d')
#    availcolors = [[0.4,1,0.4],[1,0.4,0.4],[0.5,0.5,1],[0.8,0.1,1],[0.8,1,0.1]]
#    colors = [availcolors[int(i)] for i in idx]
#    ax3D.scatter(points[:, 0], points[:, 1], points[:, 2], s=10, c=colors, marker='o') 
#    ##
#    ax3D.plot(res[:,0],res[:,1],res[:,2], marker='o', markersize=20, linewidth=0, c='y', mfc='None')
#    ax3D.plot(res[:,0],res[:,1],res[:,2], marker='*', markersize=20, linewidth=0,  c='y')
##    pylab.show()
#    plt.title('Real game data %s' %(x+1))
#    #ax3D.set_xlabel('Logins')
#    #ax3D.set_ylabel('Battles')
#    #ax3D.set_zlabel('PremiumSpent')
#    plt.savefig('%s_%s.png' % (x,'realdata'))
#    plt.cla()
    


#pylab.show()
        
#    Plot.plotPoints(points, idx, title='Data Batch %s: shifting means' %x)
#    Plot.plotMeans(res)
#    pylab.show()
    
#Deprecated SSE calculations
#totalsse = 0            
#for xIdx in xrange(len(points)):
#    mindist = sys.maxint
#
#    for cIdx in xrange(len(res)):
#        d = np.sqrt(np.sum((points[xIdx] - res[cIdx])**2))
#        if(d < mindist):
#            mindist = d
#    
#    totalsse += mindist**2
#    
#print "SSE2: %s" % totalsse

#fig = plt.figure()
#ax3D = fig.add_subplot(111, projection='3d')
#availcolors = [[0.4,1,0.4],[1,0.4,0.4],[0.5,0.5,1],[0.8,0.1,1],[0.8,1,0.1]]
#colors = [availcolors[int(i)] for i in idx]
#ax3D.scatter(points[:, 0], points[:, 1], points[:, 2], s=10, c=colors, marker='o') 
###
#ax3D.plot(res[:,0],res[:,1],res[:,2], marker='o', markersize=20, linewidth=0, c='y', mfc='None')
#ax3D.plot(res[:,0],res[:,1],res[:,2], marker='*', markersize=20, linewidth=0,  c='y')
#pylab.show()

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




#Plot.plotPoints(points, minLabels, title='final')
#Plot.plotMeans(minMeans)
#plt.show()
