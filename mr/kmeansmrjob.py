from mrjob.job import MRJob
import numpy as np
import os
from scipy.spatial import distance

#Euclidian distance
def dist(x, c):
    return distance.euclidean(x, c)
        
        
# Map and Reduce
# First version

class MRKMeansJob(MRJob):
    
    def __init__(self, *args, **kwargs):
        super(MRKMeansJob, self).__init__(*args, **kwargs)
        
        #DEBUG purposes  local file (runner=inline, because it cannot find the uploaded file)
        #DEBUG inline
#        self.centroids = np.loadtxt('/home/sigurdurm/spyderws/k-means/scripts/data/initialcentroids.txt')
#        self.options.numberofclusters = len(self.centroids)
#        self.points = np.zeros((0,len(self.centroids[0])))
        
        self.cfilename = self.options.centroidsFilename    
        self.cinitfilename = self.options.initcentroidsFilename
#        
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
        super(MRKMeansJob, self).configure_options()
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
        
    
    def mapper(self, key, line):       
        #split line to a vectorl
        point = [float(feature) for feature in line.split()]
        
        #find nearest centroid
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
        
        newcentroid = [0]*3
        for point in data:
            for featureidx in xrange(len(point)):
                newcentroid[featureidx] += point[featureidx]
        
        for i in xrange(len(newcentroid)):
            newcentroid[i] = newcentroid[i] / len(data)
            
        yield key, newcentroid


if __name__ == '__main__':
    MRKMeansJob.run()
    
    
        
        
    