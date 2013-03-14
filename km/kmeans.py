import random
import numpy as np
import matplotlib.pyplot as plt
import pylab
from scipy.spatial.distance import *


class KMeans():
    
    def __init__(self, showsubplots):
        self.showsubplots = showsubplots
        
    
    def plotMeans(self, means):
        # mark centroids as (X)
        plt.scatter(means[:,0],means[:,1], marker='o', s = 500, linewidths=2, c='none')
        plt.scatter(means[:,0],means[:,1], marker='x', s = 500, linewidths=2)
        
        
    def plotPoints(self, data, labels, title):
        plt.title(title)
        availcolors = [[0.4,1,0.4],[1,0.4,0.4],[0.5,0.5,1],[0.8,0.1,1],[0.8,1,0.1]]
        colors = [availcolors[i] for i in labels]
        dataarray = np.array(data)
        pylab.scatter(dataarray[:,0],dataarray[:,1], c=colors)
        
        
    def subplotClusters(self, data, labels, means, iteration, title ):
        rows = 4
        columns = 4
        
        plt.subplot(rows, columns, iteration)
        self.plotPoints(data, labels, title)
        self.plotMeans(means)
        
        
    def plotIntermediateClusters(self, data, labels, means, title):
        self.plotPoints(data, labels, title)
        self.plotMeans(means)
        pylab.show()
        
        
    def sse(self, item, mean):
        diff = item - mean
        diff = diff**2
        return np.sum(diff)
        
        
    def distance(self, item, mean):
        return euclidean(item, mean)        
        
    
    def calculateMeans(self, data, labels, numberOfClusters):
        means = np.zeros((numberOfClusters, len(data[0])))
        pointsInClusters = np.zeros(numberOfClusters)
        
        for i in xrange(len(data)):
            cluster = labels[i]
            pointsInClusters[cluster] += 1
            point = data[i]
            for featureIdx in xrange(len(point)):
                means[cluster,featureIdx] += point[featureIdx]
            
        for clusterIdx in xrange(len(means)):
            mean = means[clusterIdx]
            mean /= float(pointsInClusters[clusterIdx])
        
        return means, pointsInClusters
        
        
    def calculateSSE(self, data, labels, numberOfClusters, means):
        totalsse = 0
        
        for i in xrange(len(data)):
            cluster = labels[i]
            point = data[i]
            totalsse += self.sse(point, means[cluster])

        return totalsse
    
    
    def run(self, data, numberOfClusters, threshold, maxiterations):
        # initialize means
        means = np.array(random.sample(data, numberOfClusters))
        print "Initial Means: \n%s" % means
        
        labels = np.zeros(len(data), dtype=int)
        iteration = 0
        
        #plotting
        title = 'iteration %i:' % (iteration)
        if not self.showsubplots:
            self.plotIntermediateClusters(data, labels, means, title)
        else:
            self.subplotClusters(data, labels, means, iteration, title)
        
        while iteration < maxiterations:
            #initialize labels for each iteration
            iteration += 1
            print "Iteration %d" % iteration 
            
            #Calculating the distance to nearest cluster
            distmatrix = cdist(data, means, metric='euclidean')
            labels[:] = distmatrix.argmin(axis=1)
                
            #calculate a new mean for each cluster
            meansNew, pointsInClusters = self.calculateMeans(data, labels, numberOfClusters)
            
            #check if the means have changed  
            meansDiff = 0  
            
            for i in xrange(numberOfClusters):
                meansDiff += self.distance(meansNew[i], means[i])
                
            print 'Means difference: %f' % meansDiff
            
            #calculate the within cluster variation, sum of squared distances between all objects in cluster and its centroid
            SSE = self.calculateSSE(data, labels, numberOfClusters, meansNew)
            print "SSE: %f" % SSE
            
            #plotting
            title = 'iteration %i meansdiff: %f' % (iteration, meansDiff)
            if not self.showsubplots:
                self.plotIntermediateClusters(data, labels, meansNew, title)
            else:
                self.subplotClusters(data, labels, meansNew, iteration, title)
                
            means[:] = meansNew
            if meansDiff < threshold:
                break
        
        #End of While loop
        #KMeans ends here
        
        #Difference under threshold or there are max iterations
        if iteration == maxiterations:
            print "Max iterations reached: %d" % iteration
        else:
            print "Means difference: %f is under threshold %f" % (meansDiff, threshold)
            
        #print "Clusters:"
        for i in xrange(numberOfClusters):
            print "Cluster %d, number of points %d" % (i, pointsInClusters[i])
        
        if self.showsubplots:
            self.subplotClusters(data, labels, means, iteration, title)
            pylab.show()
            
        return means, labels
         

        
        

