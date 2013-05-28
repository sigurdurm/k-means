import numpy as np
import os.path
from util import Utils,Plot,Logger
import sys
import boto
from mr import *
import subprocess
from pprint import pprint
import pylab
import time
import glob
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from datetime import date, datetime
import logging
import random

    
if __name__ == '__main__':
    
    running_aws = False
    
    k = 3
    maxiterations = 2
    delta = 0.01
    
    #Data Source    
#    filenamezscoredata = 'zdata-zscore.txt' #3
    filenamecentroids = 'centroids.txt'
#    filenameinitcentroids = 'initial_splits_aa_zscore.centroids.dat'
#    filenameinitcentroids = 'sortedbytimestamps_split.txtaa_zscore.centroids.dat'
#    filenameinitcentroids = '2_initialcentroids.txt'
    
    path = os.path.dirname(__file__)
    multiplefilepath = 'data/multiple/sorted/with outliers/'
#    multiplefilepath = 'data/multiple/sorted/wo outliers/'
#    multiplefilepath = 'data/multiple/genshiftmeans/'
    
    #Loading data points from multiple files, for SSE error in whole dataset
#    files = glob.glob(os.path.join(path, multiplefilepath + '*zscore.dat'))
#    files = glob.glob(os.path.join(path, multiplefilepath + '*.dat'))
#    files.sort()
#    plist = []
#    points = None
#    for f in files:
#        p = np.loadtxt(f)
#        if points == None:
#            points = p
#        else:
#            points = np.concatenate((points, p))
#    import pdb;pdb.set_trace()  
    #END Loading data points from multiple files, for SSE error in whole dataset
    
    #MapReduceJob params
    if running_aws == False:
#        runner = 'inline' #debug
        runner = 'local' #local hadoop cluster simulation
        mroutputdir = os.path.join(path, 'data/multiple/mroutput')
#        mrinputfile = os.path.join(path, filedata)
    else:
        runner = 'emr' #Amazon Elastic MapReduce
#        mrinputfile = 's3://mrkmeans/input/%s' % filenamezscoredata
        
    
    centroidsinputfile = os.path.join(path, multiplefilepath + filenamecentroids)
#    initialcentroidsinputfile = os.path.join(path, 'data/multiple/sorted/' + filenameinitcentroids)
#    initialcentroidsinputfile = os.path.join(path, 'data/multiple/genshiftmeans/' + filenameinitcentroids)
    
    
    #Use to generate initialcenteres for experiment
#    print 'initializing centers from file: %s' % files[0]  
#    initials = np.array(random.sample(points, 30))
#    pprint(initials)
#    for i in xrange(10):
#        c = initials[3*i:3*(i+1)]
#        np.savetxt('%s_initialcentroids.txt' % i, c)        
#    import pdb;pdb.set_trace() 


    #Creating a job Flow
#    import pdb;pdb.set_trace()    
#    proc = subprocess.Popen(['python', '/usr/lib/python2.7/dist-packages/mrjob/tools/emr/create_job_flow.py', '--hadoop-version=1.0.3'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#    procoutput = proc.communicate()[0]
#    print procoutput
#    listout = procoutput.split('\n')
#    jobflowid = listout[len(listout)-2]
#    print 'Persistent EMR JobFlowId created %s' % jobflowid
#    jobflowid =  'j-2WQYGNJHELRLK'
    
#    mroutputdir = 's3://%s-mrkmeans/output/' % jobflowid#EMR
#    mroutputdir = 's3://mrkmeans/output/'#EMR
    
    #Iterative process
    minSSE = sys.maxint
#    dimensions = 2
#    minInitialMeans = np.zeros((k, dimensions))
#    minMeans = np.zeros((k, dimensions))
    
    #Sort input files in alphabetical order    
    files = glob.glob(os.path.join(path, multiplefilepath + '*zscore.dat')) #with outliers!
#    files = glob.glob(os.path.join(path, multiplefilepath + '*zscore_wo_outliers.dat')) #without outliers!
#    files = glob.glob(os.path.join(path, multiplefilepath + '*.dat'))
    files.sort()
    
    cfiles = glob.glob(os.path.join(path, multiplefilepath + '*_initialcentroids*'))
    cfiles.sort()    
    
    plotexperiments = []    
    
#    points = np.zeros(()) #Use for data seen so far experiment
    numexperiments = 10
    for x in xrange(numexperiments): # experiments
            
        fileoutpostfix = '_mrjobmultiple_%s_%si' % (x, maxiterations)
        logger = Logger.function_logger(str(x), fileoutpostfix, logging.DEBUG, logging.INFO, logging.DEBUG)
        
        #initializing
#        initialMeans = np.loadtxt(initialcentroidsinputfile) #separate initial file

        #Use when running multiple experiments        
        initialMeans = np.loadtxt(cfiles[x]) #separate initial file, #Deprecated
        initialcentroidsinputfile = cfiles[x]
        filenameinitcentroids = os.path.basename(initialcentroidsinputfile)

        #Use when running single experiment
        

        oldCentroids = initialMeans #separate initial centroids
        
        numberfiles = 10
        for count in xrange(numberfiles): #files
    
            mrinputfile = files[count]
            # Use for current data set experiment
            points = np.loadtxt(mrinputfile)
            
            #Use for data seen so far experiment
#            if count == 0:
#                points = np.loadtxt(mrinputfile)
#            else:
#                points = np.concatenate((points, np.loadtxt(mrinputfile)))
            #End Use for data seen so far experiment
                
            logger.debug('file %s: %s' % (count,mrinputfile))
            
    #        mrinputfile = os.path.join(path, 'data/%s' % inputfile1)
            #init random centroids 
    #        initialMeans = Utils.getInitialMeans(points, k)     
    #        np.savetxt(centroidsinputfile, initialMeans)
        
            
            
            pointsInCentroid = [0]*k
            total = 0
            for i in xrange(maxiterations):
                #MRJob params            
                params = [mrinputfile, '-r', runner, '--file', centroidsinputfile, '--cfile', filenamecentroids, '--k', str(k)]
        
                # Only initialize centroids in the first iteration
                if i == 0 and count == 0:
                    logger.debug('Experiment: %s. Using predefined initial centroids: %s' % (x,filenameinitcentroids))
                    params += ['--file', initialcentroidsinputfile, '--cinitfile', filenameinitcentroids]               
                else:
                    params += ['--cinitfile', 'none.txt']
                
                #Params for local or AWS
                if running_aws == False:
                        params += ['--output-dir', mroutputdir]
                else:
                    params += ['--pool-emr-job-flows']#, '--pool-name', 'kmeansmrjob']
        
                mr_job = MRKMeansCombinerJob(args=params)
            
                newCentroids = np.zeros((k, len(points[0])))
                start = time.time()
                logger.debug('iteration %d' % i)
                logger.debug( "initial centroids: \n%s" % oldCentroids)
                logger.debug( 'Running MR job with params:')
                logger.debug(params)
                
                with mr_job.make_runner() as jobrunner:
                    jobrunner.run()
            
                    #parse the new means from std.output from reducers
                    #TODO, possible switch out parsing the output from std.out to parsing output files from reducers.    
                    if not mr_job.options.no_output:
                        for line in jobrunner.stream_output():
        #                    mr_job.stdout.write(line)
        #                    import pdb; pdb.set_trace()
                            values = line.strip().split('\t')
        #                    newCentroids[eval(values[0])] = eval(values[1]) #getting centroid vector, from (key,value)
                            newCentroids[eval(values[0])] = eval(values[1])[0] #getting centroid vector from (key, valuelist)
                            pointsInCentroid[eval(values[0])] = eval(values[1])[1] #getting number of elements per centroid
        #                    diameter[eval(values[0])] = eval(values[1])[1] #getting the centroid diameter
                        mr_job.stdout.flush()
                        
                end = time.time()
                logger.debug('time: %f' % (end-start))
                total += (end-start)
                
                # no more initial centroids to mrjob. Intermediate centroids are used from now on.
                
                
            
                logger.debug("new centroids: \n%s" % newCentroids)
                logger.debug("points per centroid %s" % pointsInCentroid)
        #        print "new diameters: %s" % diameter
        
                
                #check if the means have changed, if so then exit
                diff = 0
                for i in xrange(k):
                    diff += distance.euclidean(newCentroids[i], oldCentroids[i])
                    
                logger.debug( 'means total diff %f:' % diff)
                if diff < delta:
                    break
                else:
                    oldCentroids[:] = newCentroids
                    np.savetxt(centroidsinputfile, newCentroids)
                    
            
            logger.debug( 'total time: %f' %total)
    
            #Calculate SSE
            SSE = 0
            SSE = Utils.calcSSE(points, newCentroids)
            logger.info('%.f' % SSE)
            logger.debug( 'Sum of Squared Error: %s' % SSE)
            
        
        #finds the distance to nearest cluster        
        distmatrix = distance.cdist(points, newCentroids, metric='euclidean')
        labels = distmatrix.argmin(axis=1)

        #Local
        #points = np.loadtxt(inputfile1)
#        Plot.plotPoints(points, labels, title='final kmeans2')
#        Plot.plotMeans(newCentroids)
#        strnow = datetime.now().strftime("%Y-%m-%d_%H%M%S")
#        plt.savefig('%s_%s.png' % (strnow,fileoutpostfix))
#        plt.close()

        plotexperiments.append([points, labels, newCentroids])        
        
#    
#        fig = plt.figure()
#        ax3D = fig.add_subplot(111, projection='3d')
#        availcolors = [[0.4,1,0.4],[1,0.4,0.4],[0.5,0.5,1],[0.8,0.1,1],[0.8,1,0.1]]
#        colors = [availcolors[int(i)] for i in labels]
#        ax3D.scatter(points[:, 0], points[:, 1], points[:, 2], s=10, c=colors, marker='o') 
#        ##
#        ax3D.plot(newCentroids[:,0],newCentroids[:,1],newCentroids[:,2], marker='o', markersize=20, linewidth=0, c='y', mfc='None')
#        ax3D.plot(newCentroids[:,0],newCentroids[:,1],newCentroids[:,2], marker='*', markersize=20, linewidth=0, c='y')
#        plt.show()
    
        logger.debug( 'Done.')
    
    logger.debug( 'All Done.')
    
for i in xrange(10):
   
    pr = plotexperiments[i]
    fig = plt.figure()
    ax3D = fig.add_subplot(111, projection='3d')
    availcolors = [[0.4,1,0.4],[1,0.4,0.4],[0.5,0.5,1],[0.8,0.1,1],[0.8,1,0.1]]
    colors = [availcolors[int(i)] for i in pr[1]]
    ax3D.scatter(pr[0][:, 0], pr[0][:, 1], pr[0][:, 2], s=10, c=colors, marker='o') 
    ##
    ax3D.plot(pr[2][:,0],pr[2][:,1],pr[2][:,2], marker='o', markersize=20, linewidth=0, c='y', mfc='None')
    ax3D.plot(pr[2][:,0],pr[2][:,1],pr[2][:,2], marker='*', markersize=20, linewidth=0, c='y')
#    plt.suptitle('Main title')

#    Plot.plotPoints(pr[0], pr[1], title='Experiment %s' % i)
#    Plot.plotMeans(pr[2])

    fileoutpostfix = '_mrjobmultiple_%s_%si' % (i, maxiterations)
    strnow = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    plt.savefig('%s_%s.png' % (strnow,fileoutpostfix))
#    plt.close()
    


#Terminate persistent idle job flow
#python -m mrjob.tools.emr.terminate_idle_job_flows
    