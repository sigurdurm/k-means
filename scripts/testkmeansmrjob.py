from mr.kmeansmrjob import MRKMeansJob
import numpy as np
import random
import math
import matplotlib.pyplot as plt
import pylab
import os.path

#Euclidian distance
def distance(x, c):
    total = 0
    for idx in xrange(len(x)):
        total += (x[idx] - c[idx])**2
    
    return math.sqrt(total) 
        
def zscore(xy):
    return (xy-xy.mean())/xy.std()
    
def plotdata(points, centroids):
    color = [0.4,0.8,0.2]
    pylab.title('data and final means')
    pylab.scatter(points[:,0],points[:,1], c=color)
    
    plt.scatter(newCentroids[:,0],newCentroids[:,1], marker='o', s = 500, linewidths=2, c='none')
    plt.scatter(newCentroids[:,0],newCentroids[:,1], marker='x', s = 500, linewidths=2)
    pylab.show()


if __name__ == '__main__':
    
    dimensions = 2
#    #generating random data    
#    pt1 = np.random.normal(1, 0.1, (100,dimensions))
#    pt2 = np.random.normal(5, 1, (500,dimensions))
#    pt3 = np.random.normal(10, 1, (100,dimensions))
#     
#    points = np.concatenate((pt1, pt2, pt3))
#    
#    #normalize z-score
#    points = zscore(points)    
#    
#    #write to file
#    np.savetxt('data.txt', points)
    
    
    k = 3
    maxiterations = 10
    delta = 0.1
        
    #initializing the new centroids array 
    newCentroids = np.zeros((k, dimensions))
    
    #Create the Job
#    runner = 'inline'
    path = os.path.dirname(__file__)
    runner = 'local'
    inputpath = os.path.join(path, 'data/data.txt')
    centroidsfilename = 'centroids.txt'
    centroidspath = os.path.join(path, 'data/centroids.txt')
    mr_job = MRKMeansJob(args=[inputpath, '-r', runner, '--file', centroidspath, '--cfile', centroidsfilename, '--k', str(k)])
    
    #initialize centroids and write them to a file.
    data = np.loadtxt(inputpath)
    oldCentroids = np.array(random.sample(data, k))
    print 'initialized centroids: \n %s' % oldCentroids
    np.savetxt(centroidspath, oldCentroids)

    #iterate process    
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
            diff += distance(newCentroids[i], oldCentroids[i])
            
        print 'means diff %f:' % diff
        if diff < delta:
            break
        else:
            oldCentroids[:] = newCentroids
            np.savetxt(centroidspath, newCentroids)
            
            
    
    #Plot initialdata
    points = np.loadtxt(inputpath)
    plotdata(points, newCentroids)
    