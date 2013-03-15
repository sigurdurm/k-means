from mrjob.job import MRJob
import numpy as np
import os
from scipy.spatial import distance

#Euclidian distance
def dist(x, c):
    return distance.euclidean(x, c)
        
    
class MRKMeansJob(MRJob):
    
    def __init__(self, *args, **kwargs):
        super(MRKMeansJob, self).__init__(*args, **kwargs)
        
        #Read in initial means
#        if self.options.centroidsFilename == None:
#            print 'No filename to initialized centroids given!'
        if os.path.isfile(self.options.centroidsFilename):
            self.centroids = np.loadtxt(self.options.centroidsFilename)
            self.options.numberofclusters = len(self.centroids)
#            print 'Initialized centroids read in: \n%s' % self.centroids
#        else:
#            print 'Initialized centroids file not found!'
            
        
    def configure_options(self):
        super(MRKMeansJob, self).configure_options()
        #Not used for now. len(self.centroids) sets the k in the constructor
        self.add_passthrough_option(
            '--k', dest='numberofclusters', type='int',
            help='k: number of centroids')
            
        self.add_passthrough_option(
            '--cfile', dest='centroidsFilename', type='str',
            help='cfile: centroids file name')
        
    
    def mapper(self, key, line):       
        #split line to a vectorl
        point = [float(feature) for feature in line.split()]
        
        #find nearest centroid, where line is a data vector
        mindist = 0
        minCentroid = None
        for idx in xrange(self.options.numberofclusters):
            d = dist(point, self.centroids[idx])
            if(d < mindist or minCentroid == None):
                mindist = d
                minCentroid = idx
                
        #(id, data pairs to the reducer)
        yield minCentroid, point 
        

    #calculating the new means for each cluster key
    def reducer(self, key, values):
        data = list(values)
        
        newcentroid = [0]*2
        for point in data:
            for featureidx in xrange(len(point)):
                newcentroid[featureidx] += point[featureidx]
        
        for i in xrange(len(newcentroid)):
            newcentroid[i] = newcentroid[i] / len(data)
            
        yield key, newcentroid


if __name__ == '__main__':
    MRKMeansJob.run()
    
    
        
        
    