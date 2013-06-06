import numpy as np
import os.path
from util import Utils,Plot
import sys
from mr import *
import subprocess
from pprint import pprint
import pylab
from time import time


#Run MR kmeans on single data file

#MRJob Types 
#MRKMeansCombinerJob 
#MRKMeansCombinerNaiveJob 
#MRKMeansCombinerDistMatrixJob 
#MRKMeansJob #kmeansmrjob.py
    
if __name__ == '__main__':

    #Run on AWS or not
    running_aws = False
    
#    if(len(sys.argv) > 1):
#        running_aws = bool(sys.argv[1])
#        print 'running AWS: %s' %running_aws
    
    k = 3
    maxiterations = 1
    delta = 0.01
    dimensions = 3

    #Data Source    
#    filenamedata = 'data/iris-dat.dat'
#    filenamezscoredata = 'iris-dat-zscore.dat' #4
#    filenamedata = 'data/zdata.txt'

    filenamezscoredata = 'zdata-zscore.txt' #3
    filenameinitcentroids = 'initialcentroids.txt' #zdata
#    filenamezscoredata = 'gen_zscore_data.txt' #generated test #3
#    filenameinitcentroids = 'gen_initial_centroids.txt' #generated test #3 
#    filenamezscoredata = 'gen_zscore_data_2.txt' #generated test #3
#    filenameinitcentroids = 'gen_initial_centroids_2.txt' #generated test #3
#    filenamezscoredata = 'gen_zscore_data_shuffle.txt' #generated test #3
#    filenameinitcentroids = 'gen_initial_centroids_shuffle.txt' #generated test #3
#    filenamezscoredata = 'gen_zscore_data_shuffle_220MB.txt' #generated test #3
#    filenameinitcentroids = 'gen_initial_centroids_shuffle_220MB.txt' #generated test #3

    filenameintermediatecentroids = 'centroids.txt'
    
    #Loading data points
    path = os.path.dirname(__file__)
    filedata = 'data/%s' % filenamezscoredata
    print 'loading file... %s' % filedata
    points = np.loadtxt(os.path.join(path, filedata))
#    points = Utils.zscore(points) #normalize using z-score
    
    #MapReduceJob paramsd
    if running_aws == False:
#        runner = 'inline' #debug
        runner = 'local' #local hadoop cluster simulation
        mroutputdir = os.path.join(path, 'data/mroutput')
        mrinputfile = os.path.join(path, filedata)
    else:
        runner = 'emr' #Amazon Elastic MapReduce
        mrinputfile = 's3://mrkmeans/input/%s' % filenamezscoredata
    
    intermediatecentroidsinputfile = os.path.join(path, 'data/' + filenameintermediatecentroids)
    initialcentroidsinputfile = os.path.join(path, 'data/' + filenameinitcentroids)
    
    
    #Iterative process
    minSSE = sys.maxint
    minInitialMeans = np.zeros((k, dimensions))
    minMeans = np.zeros((k, dimensions))
    oldCentroids = np.zeros((k, dimensions))
    
    numexperiments = 1 #Number of experiments, with random initial centroids
    for count in xrange(numexperiments):
        #initializing
        initialMeans = np.loadtxt(initialcentroidsinputfile) #separate initial file

        oldCentroids[:] = initialMeans #separate initial centroids
        newCentroids = np.zeros((k, dimensions))
        
        print "initial centroids: \n%s" % oldCentroids
        
        pointsInCentroid = [0]*k
        total = 0
        for i in xrange(maxiterations):
            #MRJob params            
            params = [mrinputfile, '-r', runner, '--file', intermediatecentroidsinputfile, '--cfile', filenameintermediatecentroids, '--k', str(k)]

            # Only initialize centroids in the first iteration
            if i == 0:            
                params += ['--file', initialcentroidsinputfile, '--cinitfile', filenameinitcentroids]               
            else:
                params += ['--cinitfile', 'none.txt']
            
            #Params for local or AWS
            if running_aws == False:
                    params += ['--output-dir', mroutputdir]
            else:
                params += ['--pool-emr-job-flows']#, '--pool-name', 'kmeansmrjob']

            mr_job = MRKMeansJob(args=params)
            
            start = time()
            print 'iteration %d' % i
            print 'Running MR job with params:'
            pprint(params)
            
            with mr_job.make_runner() as jobrunner:
                jobrunner.run()
        
                #parse the new means from std.output from reducers
                if not mr_job.options.no_output:
                    for line in jobrunner.stream_output():
                        values = line.strip().split('\t')
#                        newCentroids[eval(values[0])] = eval(values[1]) #getting centroid vector, from (key,value)
                        newCentroids[eval(values[0])] = eval(values[1])[0] #getting centroid vector from (key, valuelist)
                        pointsInCentroid[eval(values[0])] = eval(values[1])[1] #getting number of elements per centroid
                    mr_job.stdout.flush()
                    
            end = time()
            print 'Running time: %f' % (end-start)
            total += (end-start)
            
            # no more initial centroids to mrjob. Intermediate centroids are used from now on.
            print "New centroids from MR job: \n%s" % newCentroids
            print "Points per centroid %s" % pointsInCentroid
            
            #check if the means have changed, if so then exit
            diff = np.sum(np.sqrt(np.sum((newCentroids - oldCentroids)**2, axis=1)))
            print 'Means diff (new-old) %f:' % diff
            
            if diff < delta:
                break
            else:
                oldCentroids[:] = newCentroids
                np.savetxt(intermediatecentroidsinputfile, newCentroids) #save intermediate centroids
                

        print 'Total Running time: %f' %total
        
        SSE = Utils.calcSSE(points, newCentroids)
        print 'Sum of Squared Error: %s' % SSE

        if SSE < minSSE:
            print '**New min SSE %s' % SSE
            minSSE = SSE
            minInitialMeans[:] = initialMeans
#            print 'New min initial means\n%s' % initialMeans)
            minMeans[:] = newCentroids

    
    print "min SSE: %s" % minSSE
    print "min Initial means: %s" % minInitialMeans
    print "min means: %s" % minMeans
    
        
    #Plot initialdata
#    points = np.loadtxt(inputfile1)
        
    
    #Inline
#    labels = np.loadtxt(debugoutputpath + 'mrlabels.txt')
#    Plot.plotPoints(points, labels, title='final')
#    Plot.plotMeans(newCentroids)
#    pylab.show()
            
    
    #Local
    #points = np.loadtxt(inputfile1)
#    Plot.plotdataMrjob(points, newCentroids)


#Terminate persistent idle job flow
#python -m mrjob.tools.emr.terminate_idle_job_flows

#Create alive job flow without need to use jobflowid
#python -m mrjob.tools.emr.create_job_flow --pool-emr-job-flows
    