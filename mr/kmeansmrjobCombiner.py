from mrjob.job import MRJob
import numpy as np
import os
import sys
from scipy.spatial import distance

#Euclidian distance
def dist(x, c):
#    return np.sqrt(np.sum((x - c)**2))
    #return distance.euclidean(x, c) #Twice as slower than above, zdata.
    #return np.linalg.norm(x-c) #little bit slower, avg. 0.5sec per iteration on zdata
    return np.sqrt(np.sum((x-c)**2,axis=1))  
    
class MRKMeansCombinerJob(MRJob):
    
#    centroids = None
    
    def __init__(self, *args, **kwargs):
        super(MRKMeansCombinerJob, self).__init__(*args, **kwargs)
        
        #DEBUG purposes  local file (runner=inline, because it cannot find the uploaded file)
        #DEBUG inline
#        self.centroids = np.loadtxt('/home/sigurdurm/spyderws/k-means/scripts/data/centroids.txt')
#        self.options.numberofclusters = len(self.centroids)
#        self.points = np.zeros((0,len(self.centroids[0])))
        
        self.cfilename = self.options.centroidsFilename    
        self.cinitfilename = self.options.initcentroidsFilename
        
#        import pdb;pdb.set_trace()
#        Read in initial means
        if os.path.isfile(self.cinitfilename):
            self.centroids = np.loadtxt(self.cinitfilename)
            self.options.numberofclusters = len(self.centroids)
            self.points = np.zeros((0,len(self.centroids[0])))
        elif os.path.isfile(self.cfilename):
            self.centroids = np.loadtxt(self.cfilename)
            self.options.numberofclusters = len(self.centroids)
            self.points = np.zeros((0,len(self.centroids[0])))
            
        
#        if self.centroids != None:
#            self.options.numberofclusters = len(self.centroids)
#            self.points = np.zeros((0,len(self.centroids[0])))
            
        
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
     
    #construct an array with all the data points
    def mapper(self, _, line):
        
        #This first line makes this function a generator function rather than a
        #normal function, which MRJob requires in its mapper functions. You need
        #to do this when all the output comes from the mapper_final.
#        if False: yield
        
        #using scipy version
#        point = [[float(feature) for feature in line.split()]]
#        self.points = np.append(self.points, point, axis=0)
    
        #calculating distance per point
        point = np.array([float(feature) for feature in line.split()])
        
        #find nearest centroid, where line is a data vector
#        mindist = sys.maxint
#        minCentroid = -1
        
        #p diff array version
        d = dist(point, self.centroids)
        minCentroid = d.argmin()

        #point diff point version (vector)        
#        for idx in xrange(self.options.numberofclusters):
#            d = np.sqrt(np.sum((point - self.centroids[idx])**2))
#            if(d < mindist):
#                mindist = d
#                minCentroid = idx
                
        #(id, data pairs to the reducer)
        yield int(minCentroid), point.tolist() #point - centroids
#        yield minCentroid, point.tolist() #point - centroid point
        

    #using scipy
    #calculate the distance to nearest cluster, emits cluster id and its point
#    def mapper_final(self):
##        labels = np.zeros(len(self.points), dtype=int)
#        
#        #Deprecated when using utils
##        distmatrix = distance.cdist(self.points, self.centroids, metric='euclidean')
##        labels[:] = distmatrix.argmin(axis=1)
#        
#        #finds the distance to nearest cluster        
#        distmatrix = distance.cdist(self.points, self.centroids, metric='euclidean')
#        labels = distmatrix.argmin(axis=1)
#        for i in xrange(self.options.numberofclusters):
#            b = labels == i #bool array, finding points per label/centroid
#            assignedpoints = self.points[b]
#            pointsSum = np.sum(assignedpoints, axis=0)
#            yield (i, [pointsSum.tolist(), len(assignedpoints)])
##            yield i, assignedpoints.tolist()
#       
#        #Plotting for debugging, when runner = inline
##        np.savetxt(self.options.debugoutput + 'mrpoints.txt', self.points)
##        np.savetxt(self.options.debugoutput + 'mrlabels.txt', labels)
#        
#        #Deprecated when using utils
#        #emitting closest centroid id and its data point        
##        for i in xrange(len(self.points)):
##            yield int(labels[i]), self.points[i].tolist()
            
        
    #Not used with distance matrix
    #calculates the mean and number of points per cluster inside a mapper node
    def combiner(self, key, values):
        points = np.array(list(values))
        
        pointsSum = np.sum(points, axis=0)
        numPoints = len(points)
        #not necessary     
#        newmean = np.zeros(len(points[0]))
#        newmean = pointsSum / numPoints
        
        #condensed distance matrix
#        cdistmatrix = distance.pdist(points, metric='euclidean')
#        diameter = 0
#        if np.size(cdistmatrix) > 0:
#            diameter = np.amax(cdistmatrix)
#        yield int(key), [pointsSum.tolist(), numPoints, diameter]
        
        yield int(key), [pointsSum.tolist(), numPoints]




    #calculating the new weighted means for each cluster key
    def reducer(self, key, values):
        
        #split values to mean and number of points
        meansAndnumPoints = list(values)
        totalWeightMeanSum, totalNumPoints = 0, 0
        
#        maxdiameter = 0
        for item in meansAndnumPoints:
            #deprecated
#            mean = np.array(item[0])
            pointSum = np.array(item[0])
            numPoints = item[1]
            #deprecated
#            diameter = item[2]
#            if(diameter > maxdiameter):
#                maxdiameter = diameter
            #deprecated    
#            totalWeightMeanSum += numPoints * mean
            #make more efficient using numpy
            totalWeightMeanSum += pointSum
            totalNumPoints += numPoints
            
        wmean = totalWeightMeanSum / totalNumPoints
#        yield int(key), [wmean.tolist(), maxdiameter]
        yield (int(key), [wmean.tolist(), totalNumPoints])

    #Mapper Reducer only version.
#    def reducer(self, key, values):
#        points = list(values)
#        
#        points = np.array(points)
#        pointsSum = np.sum(points, axis=0)
#        numPoints = len(points)
#        
#        wmean = pointsSum / numPoints
#        
#        yield int(key), wmean.tolist()
        

if __name__ == '__main__':
    MRKMeansCombinerJob.run()
    
    
        
        
    