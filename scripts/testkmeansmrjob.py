from mr.kmeansmrjob import MRKMeansJob
import numpy as np
import os.path
from scipy.spatial import distance
from util.utilities import Utils

    
if __name__ == '__main__':
    
    k = 3
    maxiterations = 10
    delta = 0.1    
    
    #MapReduceJob params
    path = os.path.dirname(__file__)
    inputfile1 = os.path.join(path, 'data/data.txt')
    centroidsfilenamejob = 'centroids.txt'
    centroidsinputfile = os.path.join(path, 'data/centroids.txt')
    
    dimensions = 2
    Utils.generateTestDataAndCentroids(k, dimensions, inputfile1, centroidsinputfile)
    
    #Create the Job
#    runner = 'inline'
    runner = 'local'
    mr_job = MRKMeansJob(args=[inputfile1, '-r', runner, '--file', centroidsinputfile, '--cfile', centroidsfilenamejob, '--k', str(k)])
    #TODO, possible switch out parsing the output from std.out to parsing output files from reducers.    
    #output dir param
    #--output-dir
    
    #Iterative process    
    #initializing
    newCentroids = np.zeros((k, dimensions))
    oldCentroids = np.loadtxt(centroidsinputfile)
    

    for i in xrange(maxiterations):
        print 'iteration %d' % i
        with mr_job.make_runner() as runner:
            runner.run()
    
            if not mr_job.options.no_output:
                for line in runner.stream_output():
                    mr_job.stdout.write(line)
                    values = line.strip().split('\t')
                    newCentroids[eval(values[0])] = eval(values[1])
                mr_job.stdout.flush()
        
        #if centroids did not change then exit
        #check if the means have changed  
        diff = 0
        for i in xrange(k):
            diff += distance.euclidean(newCentroids[i], oldCentroids[i])
            
        print 'means diff %f:' % diff
        if diff < delta:
            break
        else:
            oldCentroids[:] = newCentroids
            np.savetxt(centroidsinputfile, newCentroids)
            
            
    
    #Plot initialdata
    points = np.loadtxt(inputfile1)
    Utils.plotdataMrjob(points, newCentroids)
    