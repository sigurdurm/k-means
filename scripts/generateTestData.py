import os.path
from util.utilities import Utils, Plot
import numpy as np
import random
from scipy.spatial import distance
import matplotlib.pyplot as plt
import glob

def gen2dpoints(num, mean1, var1, mean2, var2):
    p1 = np.random.normal(mean1, var1, num)
    p2 = np.random.normal(mean2, var2, num)
    
    d1 = np.reshape(p1, (num,1))
    d2 = np.reshape(p2, (num,1))
    
    centroidpoints = np.append(d1, d2, axis=1)
    centroid = np.sum(centroidpoints, axis=0)/len(centroidpoints)
    
    return centroidpoints, centroid



##START Generate single file toy set data
#k = 3
#dimensions = 3
#fndata = os.path.join(os.path.dirname(__file__), 'data/gen_zscore_data_shuffle_220MB.txt')
#fninitcentroids = os.path.join(os.path.dirname(__file__), 'data/gen_initial_centroids_shuffle_220MB.txt')
#
##generate a data set
#points, cinit = Utils.generateTestDataAndCentroids(k, dimensions, fndata, fninitcentroids)
#print 'data points generated, shape (%s,%s)' % (len(points), dimensions)
#print 'centroids generated (%s,%s)' % (len(cinit), dimensions)
##END Generate single file toy set data


##START Generating random data in separate files with shifting means 
dir1 = 0.0
dir2 = 0.0
num2 = 1000
num3 = 1000
num = 1000
firstpoints = None
newmeans = None
for i in xrange(10):
    
    if i > 0:
        dir1 += random.random()*0.1
        num2 += num*0.1
        num3 -= num*0.1
        
    points1, centroid1 = gen2dpoints(num, mean1=1+dir1*0.75, var1=0.075, mean2=1+dir1*0.5, var2=0.075)
    #centroid 2
    
    points2, centroid2 = gen2dpoints(num2, mean1=1+dir1*0.1, var1=0.075, mean2=1+dir1*0.1, var2=0.075)
    #centroid 2
    
    points3, centroid3 = gen2dpoints(num3, mean1=1+dir1*1.25, var1=0.075, mean2=1+dir1*1.25, var2=0.075)
    
    #combine
    points = np.concatenate((points1, points2, points3))
    centroids = np.concatenate(([centroid1], [centroid2], [centroid3]))
    if i == 0:    
        initial = random.sample(points, 3)
#    Plot.plotdataMrjob(points, centroids)
#
#    
#    if i != 0:
#        centroids[:] = newmeans
#        
#    newmeans, numpoints = Utils.calcNewMeans(points, centroids)
#
#    distmatrix = distance.cdist(points, newmeans, metric='euclidean')
#    labels = distmatrix.argmin(axis=1)
#
#    Plot.plotPoints(points, labels, title='iteration %s' % i)
#    Plot.plotMeans(newmeans)
#    print newmeans
#    print numpoints

    #Save figure of the clusters
    color = [0.4, 0.8, 0.2]
    plt.title('Shift means %s' %(i+1))
    plt.scatter(points[:,0],points[:,1], c=color)
    
    plt.scatter(centroids[:,0],centroids[:,1], marker='o', s = 500, linewidths=2, c='none')
    plt.scatter(centroids[:,0],centroids[:,1], marker='x', s = 500, linewidths=2)
    plt.axis([0.6,2.2, 0.6,2.2])
    ax = plt.gca()
    ax.set_autoscale_on(False)
    plt.savefig('%s_%s.png' % (i,'genshiftmeans'))
    plt.cla()
    
    np.savetxt('%s_gendata_shiftingmeans.dat' % i, points)
#    
    #normalize using z-score
    points = Utils.zscore(points) 
    np.savetxt('%s_gendata_shiftingmeans_zscore.dat' % i, points)
    
    if i == 0:
        firstpoints = points

##END Generating random data in separate files with shifting means 


#Centroids 
#firstpoints = np.loadtxt('/home/sigurdurm/spyderws/k-means/scripts/data/multiple/genshiftmeans/0_gendata_shiftingmeans.dat')
#initials = np.array(random.sample(firstpoints, 30))
#for i in xrange(10):
#    c = initials[3*i:3*(i+1)]
#    np.savetxt('%s_initialcentroids.txt' % i, c)      
    
#files = glob.glob(os.path.join(path, '/home/sigurdurm/spyderws/k-means/scripts/data/multiple/genshiftmeans/ + '*.dat'))
#for f in files:
#
#files = glob.glob('/home/sigurdurm/spyderws/k-means/scripts/data/multiple/genshiftmeans/' + '*.dat')
#for filename in files:
#    data = np.loadtxt(filename)
#    zscoredata = Utils.zscore(data)
#    postfix = filename[-4:]     
#    
#    fileout = filename[:-4] + '_zscore' + postfix
#    np.savetxt(fileout, zscoredata)
#    
#    k = 3 #3 features
#    centroids = Utils.getInitialMeans(zscoredata, k)
#    fileoutcentroids = filename[:-4] + '_zscore.centroids' + postfix
#    np.savetxt(fileoutcentroids, centroids)
#    print 'zscore saved: %s' % fileout    
    

