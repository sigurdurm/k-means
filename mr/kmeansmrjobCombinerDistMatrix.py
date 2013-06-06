from mrjob.job import MRJob
import numpy as np
import os
from scipy.spatial import distance

# Map and Reduce
# Alternative version - Distane matrix
    
class MRKMeansCombinerDistMatrixJob(MRJob):
    def __init__(self, *args, **kwargs):
        super(MRKMeansCombinerDistMatrixJob, self).__init__(*args, **kwargs)
        
        self.cfilename = self.options.centroidsFilename    
        self.cinitfilename = self.options.initcentroidsFilename

        if os.path.isfile(self.cinitfilename):
            self.centroids = np.loadtxt(self.cinitfilename)
            self.options.numberofclusters = len(self.centroids)
            self.points = np.zeros((0,len(self.centroids[0])))
        elif os.path.isfile(self.cfilename):
            self.centroids = np.loadtxt(self.cfilename)
            self.options.numberofclusters = len(self.centroids)
            self.points = np.zeros((0,len(self.centroids[0])))
            
        
    def configure_options(self):
        super(MRKMeansCombinerDistMatrixJob, self).configure_options()
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
     
    #construct an array with all the data points
    def mapper(self, _, line):
        #This first line makes this function a generator function rather than a
        #normal function, which MRJob requires in its mapper functions. You need
        #to do this when all the output comes from the mapper_final.
        if False: yield
        
        point = [[float(feature) for feature in line.split()]]
        
        #Store points in memory
        self.points = np.append(self.points, point, axis=0)

        
    #calculate the nearest centroid for all points
    def mapper_final(self):
        
        #finds the distance to nearest cluster        
        distmatrix = distance.cdist(self.points, self.centroids, metric='euclidean')
        labels = distmatrix.argmin(axis=1)
        
        for i in xrange(self.options.numberofclusters):
            b = labels == i #bool array, finding points per label/centroid
            assignedpoints = self.points[b] #filter with boolean array
            pointsSum = np.sum(assignedpoints, axis=0)
            
            yield (i, [pointsSum.tolist(), len(assignedpoints)])
            

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
    MRKMeansCombinerDistMatrixJob.run()
    
    
        
        
    