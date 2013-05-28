import json
from pprint import pprint
import os
import numpy as np
from util import Utils
import glob
import random


def removeoutliers_zscore(points):
    print 'num outliers: %s' % (len(points) - len((np.abs(points) > 3).any(1)))
    po = points[~(np.abs(points) > 3).any(1)]
    print 'removed : %s' % (len(points) - len(po))
    return po
    
def removeoutliers(points):
    print 'total number of points: %s' % len(points)    
    tmpzscoredata = Utils.zscore(points) #To find outliers
    po = points[~(np.abs(tmpzscoredata) > 3).any(1)] #filter out outlier rows
    print 'removed : %s' % (len(points) - len(po))
    return po
    
def printtofile(points, fn):
    with open(fn, 'w') as f:
        f.write(str(list(points))) 
        
def writeoutStdAndAvg(pwo):
    
        print 'calculate avg and std. for the last file. num: %s' % i
        pstd = np.std(pwo, axis=0)
        printtofile(pstd, 'std_original_for_convert.txt')
        pavg = np.average(pwo, axis=0)
        printtofile(pavg, 'avg_original_for_convert.txt')

if __name__ == '__main__':
#    path = os.path.dirname(__file__)
#    inputfile1 = os.path.join(path, '../data/data.txt')

    
#    filename = '/home/sigurdurm/Dropbox/Thesis/_Data/Examples/user_design.json'
#    filename = '/home/sigurdurm/spyderws/k-means/scripts/data/zdata-zscore.txt'
    filename = '/home/sigurdurm/spyderws/k-means/scripts/data/zdata.txt'
    
    #1
    print 'remove outliers from the single original file...'    
    print 'open fn: %s' % filename
    points = np.loadtxt(filename)
    pwo = removeoutliers(points)
    zscoredata = Utils.zscore(pwo)
#    np.savetxt('zdata-zscore-wo-outliers.txt', po)
    np.savetxt('zdata-wo-outliers.txt', pwo)
    np.savetxt('zdata-zscore-wo-outliers.txt', zscoredata)
    
    initialc = np.array(random.sample(zscoredata, 3))
    print 'saving intial centroids: \n%s' % initialc
    np.savetxt('initialcentroids_zdata-zscore-wo-outliers.txt', initialc) 
#    
#    #2
#    print 'remove outliers from multiple split files...'
    
#    filespath = '/home/sigurdurm/spyderws/k-means/scripts/data/multiple/sorted/with outliers/*zscore.dat'
#    filespath = '/home/sigurdurm/Downloads/multiple/sortedtimestamp/*.dat'
#    #Normalize files and pick random distinct initial centroids
#    files = glob.glob(filespath)
#    files.sort()
#    for i in xrange(len(files)):
#        filename = files[i]
#        data = np.loadtxt(filename)
#        pwo = removeoutliers(data)
#        
#        #calculate avg and std. for the last file. 
#        #use that those informatoin to convert the z-score back to original score
#        if i == len(files)-1:
#            writeoutStdAndAvg(pwo)
#        
#        zscoredata = Utils.zscore(pwo)
#        postfix = filename[-4:]     
#        
#        fileout = filename[:-4] + '_zscore_wo_outliers' + postfix
#        np.savetxt(os.path.basename(fileout), zscoredata)
#        if i == 0: #store the points from first file, for centroid generation
#            print zscoredata
#            firstpoints = zscoredata
#        
#        k = 3 #3 features
#        initialc = np.array(random.sample(zscoredata, k))
#        fileoutcentroids = filename[:-4] + '_zscore_wo_outliers.centroids' + postfix
#        np.savetxt(os.path.basename(fileoutcentroids), initialc)
#        print 'wo outliers saved: %s' % os.path.basename(fileout)
#        
#    #3  
#    #Use to generate initialcenteres for experiment
#    print 'initializing centers from the first file'
#
#    print firstpoints
#    initials = np.array(random.sample(firstpoints, 30))
#    pprint(initials)
#    for i in xrange(10):
#        c = initials[3*i:3*(i+1)]
#        np.savetxt('%s_initialcentroids.txt' % i, c)        
        
    
    print 'All done.'