from mr import *
import numpy as np
import os.path
from scipy.spatial import distance
from util.utilities import *

    
if __name__ == '__main__':
    
    k = 3
    maxiterations = 7
    delta = 0.1    
    
    #MapReduceJob params
    path = os.path.dirname(__file__)
    inputfile1 = os.path.join(path, 'data/data.txt')
    centroidsfilename = 'centroids.txt'
    centroidsinputfile = os.path.join(path, 'data/' + centroidsfilename)
    debugoutputpath = os.path.join(path, 'data/')
    mroutputdir = os.path.join(path, 'data/mroutput')
    
    dimensions = 2
    Utils.generateTestDataAndCentroids(k, dimensions, inputfile1, centroidsinputfile)
    
    #Create the Job
    runner = 'local'    
#    mr_job = MRKMeansJob(args=[inputfile1, '-r', runner, '--file', centroidsinputfile, '--cfile', centroidsfilenamejob, '--k', str(k)])
#    runner = 'inline'
    mr_job = MRKMeansCombinerJob(args=[inputfile1, '-r', runner, '--file', centroidsinputfile, '--cfile', centroidsfilename, '--k', str(k), '--doutput', debugoutputpath, '--dpath', centroidsinputfile, '--output-dir', mroutputdir])
    
    
    
    #Iterative process    
    #initializing
    newCentroids = np.zeros((k, dimensions))
    oldCentroids = np.loadtxt(centroidsinputfile)
    print "initial centroids: \n%s" % oldCentroids
    
    diameter= [0]*k
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
                    newCentroids[eval(values[0])] = eval(values[1])[0]
                    diameter[eval(values[0])] = eval(values[1])[1]
                mr_job.stdout.flush()
        
    
        print "new centroids: \n%s" % newCentroids
        
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
            
    
    #Plot initialdata
    points = np.loadtxt(inputfile1)
    #Inline
#    labels = np.loadtxt(debugoutputpath + 'mrlabels.txt')
#    Plot.plotPoints(points, labels, title='final')
#    Plot.plotMeans(newCentroids)
#    pylab.show()
    
    #Local
    #points = np.loadtxt(inputfile1)
    Plot.plotdataMrjob(points, newCentroids)
    