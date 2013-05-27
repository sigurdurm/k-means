from sklearn import metrics
from sklearn.metrics import pairwise_distances
import os.path
import sys
from km.kmeans import KMeans
from sklearn import decomposition
import pylab
from util.utilities import Plot
from util.utilities import Utils
import numpy as np
import random
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from scipy.cluster.vq import *
from scipy.spatial import distance
from time import time
import glob


path = os.path.dirname(__file__)

#Calculate means from experiments
multiplefilepath = '/home/sigurdurm/Dropbox/Thesis/_Data/Experiments/incremental/genshiftmeans/SSEcurrentdataset/10_iteration/'
files = glob.glob(multiplefilepath + '*.dat')
files.sort()

points = np.zeros((0,10))
for f in files:
    print f
    p = np.loadtxt(f)
    p = p.reshape(10,1)
    print p
    if len(points) == 0:
        print 'none'
        points = p
    else:
        points = np.concatenate((points, p), axis=1)
        print points
        
pm = points.mean(axis=1)
with open(multiplefilepath + 'SSEmeans.txt', 'w') as f:
    print pm
    print map(int, pm)    
    for item in map(int, pm):
        f.write(str(item)+'\n') 

    
    
    