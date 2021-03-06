from mrjob.job import MRJob
import numpy as np
import os
import sys
from scipy.spatial import distance
import math

#Euclidian distance
def dist(x, c):
#    return np.sqrt(np.sum((x - c)**2)) #x: vector, c:vector
    #return distance.euclidean(x, c) #Twice as slower than above.
    #return np.linalg.norm(x-c) #little bit slower, avg. 0.5sec per iteration on zdata
    return np.sqrt(np.sum((x-c)**2,axis=1))  #x: vector, c:array


# Map, Combiner and Reduce
# Final version with Vectorisation (NumPy)
    
class MRKMeansCombinerJob(MRJob):
    def __init__(self, *args, **kwargs):
        super(MRKMeansCombinerJob, self).__init__(*args, **kwargs)
        
        #DEBUG purposes  local file (runner=inline, because it cannot find the uploaded file)
        #DEBUG inline
#        self.centroids = np.loadtxt('/home/sigurdurm/spyderws/k-means/scripts/data/centroids.txt')
#        self.options.numberofclusters = len(self.centroids)
#        self.points = np.zeros((0,len(self.centroids[0])))
        
        self.cfilename = self.options.centroidsFilename    
        self.cinitfilename = self.options.initcentroidsFilename
        
#        Read in initial means
        if os.path.isfile(self.cinitfilename):
            self.centroids = np.loadtxt(self.cinitfilename)
            self.options.numberofclusters = len(self.centroids)
            self.points = np.zeros((0,len(self.centroids[0])))
        elif os.path.isfile(self.cfilename):
            self.centroids = np.loadtxt(self.cfilename)
            self.options.numberofclusters = len(self.centroids)
            self.points = np.zeros((0,len(self.centroids[0])))
            
        
    def configure_options(self):
        super(MRKMeansCombinerJob, self).configure_options()
        #Not used for now. len(self.centroids) sets the k in the constructor
        self.add_passthrough_option(
            '--k', dest='numberofclusters', type='int',
            help='k: number of centroids')
            
        self.add_passthrough_option(
            '--cfile', dest='centroidsFilename', type='str',
            help='cfile: centroids file name')
            
        self.add_passthrough_option(
            '--cinitfile', dest='initcentroidsFilename', type='str',
            help='cinitfile: centroids file name')
     
    def mapper(self, _, line):
        point = np.array([float(feature) for feature in line.split()])
        d = dist(point, self.centroids) #calculating distance per point
        minCentroid = d.argmin() #gets the minimum distance centroid id

        yield int(minCentroid), point.tolist() #point - centroids
        

    #calculates the intermediate sum and number of points per centroid
    def combiner(self, key, values):

        points = np.array(list(values))
        pointsSum = np.sum(points, axis=0)
        numPoints = len(points)
        yield int(key), [pointsSum.tolist(), numPoints]
        

    #calculating the new weighted means for each cluster key
    def reducer(self, key, values):
        
        #split values to mean and number of points
        SumsAndnumPoints = list(values)
        totalSum, totalNumPoints = 0, 0
        
        for item in SumsAndnumPoints:

            pointSum = np.array(item[0])
            numPoints = item[1]
            totalSum += pointSum
            totalNumPoints += numPoints
            
        wmean = totalSum / totalNumPoints
        
        yield (int(key), [wmean.tolist(), totalNumPoints])


if __name__ == '__main__':
    MRKMeansCombinerJob.run()
    
    
        
        
    