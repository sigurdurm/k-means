import random
import numpy as np
import pylab
from scipy.spatial import distance
from util.utilities import Plot
from pprint import pprint


class KMeans():
    
    def __init__(self, showsubplots):
        self.showsubplots = showsubplots
        
    def calculateMeans(self, data, labels, numberOfClusters):
        means = np.zeros((numberOfClusters, len(data[0])))
        pointsInClusters = np.zeros(numberOfClusters)
        
        #Iterate through labels, for each label fecth cluster id and a data point
        #Calculate the weighted avg for each feature to form a new mean for that cluster id
        #TODO write more efficently
        for i in xrange(len(data)):
            cluster = labels[i]
            pointsInClusters[cluster] += 1
            point = data[i]
            for featureIdx in xrange(len(point)):
                means[cluster,featureIdx] += point[featureIdx]
            
        pprint('points in clusters %s' % pointsInClusters)       
        for clusterIdx in xrange(len(means)):
            means[clusterIdx] = means[clusterIdx] / float(pointsInClusters[clusterIdx])
        
        return means, pointsInClusters
        
        
    def calculateSSE(self, data, labels, numberOfClusters, means):
        totalsse = 0
        
        #TODO write more efficently
        for i in xrange(len(data)):
            cluster = labels[i]
            point = data[i]
            totalsse += distance.euclidean(point, means[cluster])**2

        return totalsse
        
    def doPlots(self, data, labels, means, iteration, title):
        if not self.showsubplots:
            Plot.plotIntermediateClusters(data, labels, means, title)
        else:
            Plot.subplotClusters(data, labels, means, iteration, title)
    
    
    def run(self, data, means, numberOfClusters, threshold, maxiterations):
        # initialize means
#        means = np.array(random.sample(data, numberOfClusters))
#        print "Initial Means: \n%s" % means
        
        pointsInClusters = np.zeros(numberOfClusters)
        SSE = 0
        labels = np.zeros(len(data), dtype=int)
        iteration = 0
        
        
        #plotting
#        self.doPlots(data, labels, means, iteration, title='iteration %i:' % (iteration))
#        import pdb;pdb.set_trace()
        while iteration < maxiterations:
            #initialize labels for each iteration
            iteration += 1
            print "Iteration %d" % iteration 
            
            #Calculating the distance to nearest cluster
            distmatrix = distance.cdist(data, means, metric='euclidean')
            labels[:] = distmatrix.argmin(axis=1)
                
            #calculate a new mean for each cluster
            meansNew, pointsInClusters = self.calculateMeans(data, labels, numberOfClusters)
            
            #check if the means have changed  
            meansDiff = 0  
            for i in xrange(numberOfClusters):
                pprint('%s %s' % (i, meansNew[i]))
                meansDiff += distance.euclidean(meansNew[i], means[i])
                
            print 'Means difference: %f' % meansDiff
            
            #calculate the within cluster variation, sum of squared distances between all objects in cluster and its centroid
            SSE = self.calculateSSE(data, labels, numberOfClusters, meansNew)
            print "SSE: %0.3f" % SSE
            
            #plotting
#            self.doPlots(data, labels, means, iteration, title='iteration %i meansdiff: %f' % (iteration, meansDiff))
                
            means[:] = meansNew
            if meansDiff < threshold:
                break
        
        #End of While loop
        #KMeans iterative process ends here
        
        #If mean difference under threshold or there are max iterations
        if iteration == maxiterations:
            print "Max iterations reached: %d" % iteration
        else:
            print "Means difference: %f is under threshold %f" % (meansDiff, threshold)
            
        #print "Clusters:"
        for i in xrange(numberOfClusters):
            print "Cluster %d, number of points %d" % (i, pointsInClusters[i])
        
        if self.showsubplots:
            Plot.subplotClusters(data, labels, means, iteration, title='final means')
            pylab.show()
            
        return means, labels, SSE
         
