import numpy as np
import random
import matplotlib.pyplot as plt
import pylab
import math
from pprint import pprint
from scipy.spatial import distance    
import inspect
import logging
from datetime import datetime


class Utils():
    
    @staticmethod
    def calcSSE(points, centroids):
        distmatrix = distance.cdist(points, centroids, metric='euclidean')
        return np.sum(distmatrix.min(axis=1)**2)
        
    @staticmethod
    def calcNewMeans(points, oldmeans):
        pointsInClusters = np.zeros(len(oldmeans))
        meansNew = np.zeros((len(oldmeans), len(points[0])))            
        
        distmatrix = distance.cdist(points, oldmeans, metric='euclidean')
        labels = distmatrix.argmin(axis=1)
        for i in xrange(len(oldmeans)):
            b = labels == i #bool array, finding points per label/centroid
            assignedpoints = points[b]
            pointsInClusters[i] = len(assignedpoints)
            meansNew[i] = np.sum(assignedpoints, axis=0) / float(pointsInClusters[i])
        
    
        return meansNew, pointsInClusters
    
    @staticmethod
    def sigmoid(xy):
        return 1/(1+np.exp(-xy))
        
    @staticmethod
    def zscore(xy):
#        return (xy-xy.mean())/xy.std()
        return (xy-np.mean(xy, axis=0))/np.std(xy,axis=0)
        
    @staticmethod
    def generateTestDataAndCentroids(k, dimensions, datafile=None, centroidsfile=None):
        #generating random data
#        plist = []
#        for i in xrange(400):
#            pt1 = np.random.normal(1, 0.1, (10000,dimensions))
#            pt2 = np.random.normal(2, 0.1, (10000,dimensions))
#            pt3 = np.random.normal(4, 0.1, (10000,dimensions))
#            plist.append(pt1)
#            plist.append(pt2)
#            plist.append(pt3)

            
        pt1 = np.random.normal(1, 0.1, (1000000,dimensions))
        pt2 = np.random.normal(2, 0.2, (1000000,dimensions))
        pt3 = np.random.normal(4, 0.4, (1000000,dimensions))
        
#        points = plist[0]
#        for i in xrange(len(plist)):
#            if i == 0:
#                continue
#            
#            points = np.concatenate((points, plist[i]))
        
        points = np.concatenate((pt1, pt2, pt3))
        print 'before shuffle '
        print points
        np.random.shuffle(points)
        print 'after shuffle'
        print points
        
        #normalize using z-score
        points = Utils.zscore(points)    
        
        #initialize centroids.
        centroids = Utils.getInitialMeans(points, k)
        
        #write to file
        if datafile:
            np.savetxt(datafile, points)
        if centroidsfile:
            np.savetxt(centroidsfile, centroids)
        
        return points, centroids
    
    @staticmethod
    def getInitialMeans(points, k):
    
        initialMeans = np.zeros((k, len(points[0])))
        
        identicalFound = True
        while identicalFound:
            initialMeans[:] = np.array(random.sample(points, k))
            identicalFound = False
            for i in xrange(k-1):
                for j in xrange(k):
                    j = j + i
                    if i == j or j >= k:
                        continue
                    
                    if (initialMeans[i,:] == initialMeans[j,:]).all():
                        identicalFound = True
#                        print '*Indentical match found:'
#                        pprint(initialMeans[i,:])
#                        pprint(initialMeans[j,:])
                    
        print 'intialmeans found!'
        return initialMeans
    
   
        
class Plot():
    @staticmethod    
    def plotdataMrjob(points, centroids):
        color = [0.4, 0.8, 0.2]
        pylab.title('data and final means')
        pylab.scatter(points[:,0],points[:,1], c=color)
        
        plt.scatter(centroids[:,0],centroids[:,1], marker='o', s = 500, linewidths=2, c='none')
        plt.scatter(centroids[:,0],centroids[:,1], marker='x', s = 500, linewidths=2)
        pylab.show()
    
    @staticmethod    
    def plotMeans(means):
        # mark centroids as (X)
        plt.scatter(means[:,0],means[:,1], marker='o', s = 500, linewidths=2, c='none')
        plt.scatter(means[:,0],means[:,1], marker='x', s = 500, linewidths=2)
        
    @staticmethod    
    def plotPoints(data, labels, title):
        plt.title(title)
        availcolors = [[0.4,1,0.4],[1,0.4,0.4],[0.5,0.5,1],[0.8,0.1,1],[0.8,1,0.1]]
        colors = [availcolors[int(i)] for i in labels]
        dataarray = np.array(data)
        pylab.scatter(dataarray[:,0],dataarray[:,1], c=colors)
        
    @staticmethod
    def subplotClusters(data, labels, means, iteration, title ):
        rows = 4
        columns = 4
        
        plt.subplot(rows, columns, iteration)
        Plot.plotPoints(data, labels, title)
        Plot.plotMeans(means)
        
    @staticmethod
    def plotIntermediateClusters(data, labels, means, title):
        Plot.plotPoints(data, labels, title)
        Plot.plotMeans(means)
        pylab.show()


class Logger():
    @staticmethod
    def function_logger(name, fileoutpostfix, file_level, file_numbers, console_level = None):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG) #By default, logs all messages
    
        if console_level != None:
            ch = logging.StreamHandler() #StreamHandler logs to console
            ch.setLevel(console_level)
            ch_format = logging.Formatter('%(asctime)s - %(message)s')
            ch.setFormatter(ch_format)
            logger.addHandler(ch)
    
        strnow = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        
        fh = logging.FileHandler("{0}_{1}.log".format(strnow,fileoutpostfix))
        fh.setLevel(file_level)
        fh_format = logging.Formatter('%(asctime)s - %(lineno)d - %(levelname)-8s - %(message)s')
        fh.setFormatter(fh_format)
        logger.addHandler(fh)
        
        fhn = logging.FileHandler("{0}_{1}.dat".format(strnow,fileoutpostfix))
        fhn.setLevel(logging.INFO)
        logger.addHandler(fhn)
    
        return logger