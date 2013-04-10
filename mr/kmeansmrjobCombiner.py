from mrjob.job import MRJob
import numpy as np
import os
from scipy.spatial import distance
import pdb

#Euclidian distance
def dist(x, c):
    return distance.euclidean(x, c)
        
    
class MRKMeansCombinerJob(MRJob):
    
    def __init__(self, *args, **kwargs):
        super(MRKMeansCombinerJob, self).__init__(*args, **kwargs)
        
#        self.filename = self.options.centroidsFilename
        #DEBUG purposes  local file (runner=inline, because it cannot find the uploaded file)
        self.filename = self.options.debugcentroidsPath
        
        #Read in initial means
        if os.path.isfile(self.filename):
#            print 'self.options.centroidsFilename %s' % self.options.centroidsFilename
#            pdb.set_trace()
            self.centroids = np.loadtxt(self.filename)
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
            '--dpath', dest='debugcentroidsPath', type='str',
            help='dpath: debug mode centroids file name')
            
        self.add_passthrough_option(
            '--doutput', dest='debugoutput', type='str',
            help='doutput: debug mode outputpath')
     
     
    #construct an array with all the data points
    def mapper(self, _, line):
        
        point = [[float(feature) for feature in line.split()]]
        self.points = np.append(self.points, point, axis=0)
        

    #calculate the distance to nearest cluster, emits cluster id and its point
    def mapper_final(self):
        labels = np.zeros(len(self.points), dtype=int)
        
         #finds the distance to nearest cluster
        distmatrix = distance.cdist(self.points, self.centroids, metric='euclidean')
        labels[:] = distmatrix.argmin(axis=1)
       
        #Plotting for debugging, when runner = inline
#        np.savetxt(self.options.debugoutput + 'mrpoints.txt', self.points)
        np.savetxt(self.options.debugoutput + 'mrlabels.txt', labels)
        
        #emitting closest centroid id and its data point        
        for i in xrange(len(self.points)):
            yield int(labels[i]), self.points[i].tolist()
            
        
    #calculates the mean and number of points per cluster inside a mapper node
    def combiner(self, key, values):
        points = np.array(list(values))
        newmean = np.zeros(len(points[0]))
        
        pointsSum = np.sum(points, axis=0)
        
#        pdb.set_trace()
        numPoints = len(points)
        newmean = pointsSum / numPoints
        
        #condensed distance matrix
        cdistmatrix = distance.pdist(points, metric='euclidean')
        
        diameter = 0
        if np.size(cdistmatrix) > 0:
            diameter = np.amax(cdistmatrix)
        
        yield int(key), [newmean.tolist(), numPoints, diameter]

    #calculating the new weighted means for each cluster key
    def reducer(self, key, values):
        
        #split values to mean and number of points
        meansAndnumPoints = list(values)
        totalWeightMeanSum, totalNumPoints = 0, 0

        maxdiameter = 0
        for item in meansAndnumPoints:
            mean = np.array(item[0])
            numPoints = item[1]
            diameter = item[2]
            if(diameter > maxdiameter):
                maxdiameter = diameter
                
            totalWeightMeanSum += numPoints * mean
            totalNumPoints += numPoints
            
        wmean = totalWeightMeanSum / totalNumPoints
        yield int(key), [wmean.tolist(), maxdiameter]
        


if __name__ == '__main__':
    MRKMeansCombinerJob.run()
    
    
        
        
    