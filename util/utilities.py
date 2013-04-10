import numpy as np
import random
import matplotlib.pyplot as plt
import pylab


class Utils():
    
    @staticmethod
    def zscore(xy):
        return (xy-xy.mean())/xy.std()
        
    @staticmethod
    def generateTestDataAndCentroids(k, dimensions, datafile=None, centroidsfile=None):
        #generating random data    
        pt1 = np.random.normal(1, 0.5, (100,dimensions))
        pt2 = np.random.normal(5, 1, (50,dimensions))
        pt3 = np.random.normal(10, 1, (100,dimensions))
         
        points = np.concatenate((pt1, pt2, pt3))
        
        #normalize using z-score
        #points = Utils.zscore(points)    
        
        #initialize centroids.
        centroids = np.array(random.sample(points, k))
        
        #write to file
        if datafile:
            np.savetxt(datafile, points)
        if centroidsfile:
            np.savetxt(centroidsfile, centroids)
        
        return points, centroids
    
   
        
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