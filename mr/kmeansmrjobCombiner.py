from mrjob.job import MRJob
import numpy as np
import os
from scipy.spatial import distance
#import pdb

#Euclidian distance
def dist(x, c):
    return distance.euclidean(x, c)
        
    
class MRKMeansCombinerJob(MRJob):
    
    def __init__(self, *args, **kwargs):
        super(MRKMeansCombinerJob, self).__init__(*args, **kwargs)
        
#        print 'inside constructor'
        
#        self.filename = self.options.centroidsFilename
        #DEBUG purposes  (runner=inline)
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
        
    
    def mapper(self, _, line):
        if False: yield # I'm a generator!
        
        point = [[float(feature) for feature in line.split()]]
        self.points = np.append(self.points, point, axis=0)
        
    
    def mapper_final(self):
#        print 'Mapper final'
        labels = np.zeros(len(self.points), dtype=int)
        
         #Calculating the distance to nearest cluster
        distmatrix = distance.cdist(self.points, self.centroids, metric='euclidean')
        labels[:] = distmatrix.argmin(axis=1)

        #emitting closest centroid and data point        
        for i in xrange(len(labels)):
            label = labels[i]
            point = self.points[i]
            yield int(label), list(point)
            
        
    def combiner(self, key, values):
        data = list(values)
        newcentroid = [0]*2
        for point in data:
            for featureidx in xrange(len(point)):
                newcentroid[featureidx] += point[featureidx]
        
        for i in xrange(len(newcentroid)):
            newcentroid[i] = newcentroid[i] / len(data)
            
        #TODO return also number of points
#        print "combiner key, newcentroid (%d, %s)" % (key, newcentroid)
        yield key, newcentroid

    #calculating the new means for each cluster key
    def reducer(self, key, values):
        data = list(values)
#        print 'Reducer key, values (%d, %s)' % (key, data)
        
        newcentroid = [0]*2
        for point in data:
            for featureidx in xrange(len(point)):
                newcentroid[featureidx] += point[featureidx]
        
        for i in xrange(len(newcentroid)):
            newcentroid[i] = newcentroid[i] / len(data)
            
        yield key, newcentroid
        


if __name__ == '__main__':
    MRKMeansCombinerJob.run()
    
    
        
        
    