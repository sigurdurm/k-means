from mr import *
import numpy as np
import os.path
from util.utilities import *
import sys

    
if __name__ == '__main__':
    k = 3
    maxiterations = 10
    delta = 0.1
    
    #MapReduceJob params
    path = os.path.dirname(__file__)
    cfn = 'centroids-zscore.txt'
#    cfn = 'zcentroids.txt'
    centroidsinputfile = os.path.join(path, 'data/' + cfn)
    debugoutputpath = os.path.join(path, 'data/')
    
    #Loading points and normalize
    fn = 'data/iris-dat.dat'
#    fn = 'data/zdata.txt'
    points = np.loadtxt(os.path.join(path, fn))
    points = Utils.zscore(points) #normalize using z-score
    
    #Local/Inline
#    runner = 'inline'
    runner = 'local'
    fzscore = 'data/iris-dat-zscore.dat' #4
#    fzscore = 'data/zdata-zscore.txt' #3
    mroutputdir = os.path.join(path, 'data/mroutput')
    mrinputfile = os.path.join(path, fzscore)
    np.savetxt(mrinputfile, points) #Store normalized file locally

    
    #EMR
#    runner = 'emr'
#    mroutputdir = 's3://mrkmeans/output/'
#    inputfile1 = 's3://mrkmeans/input/zdata_zscore_mrdata.txt'
#    inputfile1 = 's3://mrkmeans/input/zdata_zscore_mrdata.txt'


    
    
    
    #Generate toyset data
#    dimensions = 2
#    Utils.generateTestDataAndCentroids(k, dimensions, inputfile1, centroidsinputfile)

    
    #Create the MR Job
#    mr_job = MRKMeansJob(args=[inputfile1, '-r', runner, '--file', centroidsinputfile, '--cfile', centroidsfilenamejob, '--k', str(k)])
    mr_job = MRKMeansCombinerJob(args=[mrinputfile, '-r', runner, '--file', centroidsinputfile, '--cfile', cfn, '--k', str(k), '--doutput', debugoutputpath, '--dpath', centroidsinputfile, '--output-dir', mroutputdir])
    
    minSSE = sys.maxint
    minInitialMeans = np.zeros((k, len(points[0])))
    minMeans = np.zeros((k, len(points[0])))
    #Iterative process    
    for count in xrange(10):

        #init means    
        initialMeans = Utils.getInitialMeans(points, k)     
        np.savetxt(centroidsinputfile, initialMeans)
    
        #initializing
        newCentroids = np.zeros((k, len(points[0])))
        oldCentroids = np.loadtxt(centroidsinputfile)
        print "initial centroids: \n%s" % oldCentroids
        
    #    diameter= [0]*k
        pointsInCentroid = [0]*k
        for i in xrange(maxiterations):
            print 'iteration %d' % i
            with mr_job.make_runner() as runner:
                runner.run()
        
                #parse the new means from std.output from reducers
                #TODO, possible switch out parsing the output from std.out to parsing output files from reducers.    
                if not mr_job.options.no_output:
                    for line in runner.stream_output():
    #                    mr_job.stdout.write(line)
    #                    import pdb; pdb.set_trace()
                        values = line.strip().split('\t')
    #                    newCentroids[eval(values[0])] = eval(values[1]) #getting centroid vector, from (key,value)
                        newCentroids[eval(values[0])] = eval(values[1])[0] #getting centroid vector from (key, valuelist)
                        pointsInCentroid[eval(values[0])] = eval(values[1])[1] #getting number of elements per centroid
    #                    diameter[eval(values[0])] = eval(values[1])[1] #getting the centroid diameter
                    mr_job.stdout.flush()
            
        
            print "new centroids: \n%s" % newCentroids
            print "points per centroid %s" % pointsInCentroid
    #        print "new diameters: %s" % diameter
    
            
            #check if the means have changed, if so then exit
            diff = 0
            for i in xrange(k):
                diff += distance.euclidean(newCentroids[i], oldCentroids[i])
                
            print 'means total diff %f:' % diff
            if diff < delta:
                break
            else:
                oldCentroids[:] = newCentroids
                np.savetxt(centroidsinputfile, newCentroids)
                
            
        
            #Calculate SSE, TODO refactor
            labels = []
            SSE = 0
            #find nearest centroid, where line is a data vector
            
            for xIdx in xrange(len(points)):
                mindist = sys.maxint
                minCentroidIdx = None
            
                for cIdx in xrange(len(newCentroids)):
                    d = np.sqrt(np.sum((points[xIdx] - newCentroids[cIdx])**2))
                    if(d < mindist):
                        mindist = d
                        minCentroidIdx = cIdx
                
                labels.append(minCentroidIdx)
                SSE += mindist**2
                
                
            print 'SSE %s' % SSE

        
        if SSE < minSSE:
            print '**New min SSE %s' % SSE
            minSSE = SSE
            minInitialMeans[:] = initialMeans
            pprint('Min initial means\n%s' % initialMeans)
            minMeans[:] = newCentroids
#            minLabels[:] = labels

    
    print "min SSE: %s" % minSSE
    print "min Initial means: %s" % minInitialMeans
    print "min means: %s" % minMeans
    
        
    #Plot initialdata
#    points = np.loadtxt(inputfile1)
        
    
    
    #Inline
#    labels = np.loadtxt(debugoutputpath + 'mrlabels.txt')
    Plot.plotPoints(points, labels, title='final')
    Plot.plotMeans(newCentroids)
    pylab.show()


    
            
    
    #Local
    #points = np.loadtxt(inputfile1)
#    Plot.plotdataMrjob(points, newCentroids)
    