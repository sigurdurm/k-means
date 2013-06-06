from mrjob.job import MRJob
import numpy as np
import os
import sys
import math

# Map, Combiner and Reduce
# Second version
   
class MRKMeansCombinerNaiveJob(MRJob):
    def __init__(self, *args, **kwargs):
        super(MRKMeansCombinerNaiveJob, self).__init__(*args, **kwargs)
        
        
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
        super(MRKMeansCombinerNaiveJob, self).configure_options()
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
     
    #Find nearest centroid for each point at a time
    def mapper(self, _, line):
        
        point = np.array([float(feature) for feature in line.split()])
        
        #find nearest centroid, where line is a data vector
        mindist = sys.maxint
        minCentroid = -1
        for idx in xrange(self.options.numberofclusters):
            d = 0
            for i in xrange(len(self.centroids[idx])):
                c = self.centroids[idx]
                d += abs(point[i] - c[i])**2
            
            d = math.sqrt(d)
            if(d < mindist):
                mindist = d
                minCentroid = idx
        
        yield minCentroid, point.tolist() #point - centroid point

        
    #calculates the intermediate sum and number of points per centroid
    def combiner(self, key, values):
        points = np.array(list(values))
        pointsSum = np.sum(points, axis=0)
        numPoints = len(points)
        
        yield int(key), [pointsSum.tolist(), numPoints]
        

    #calculating the new weighted means for each cluster key
    def reducer(self, key, values):
        
        #split values to intermediate sum and number of points
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
    MRKMeansCombinerNaiveJob.run()
    
    
        
        
    