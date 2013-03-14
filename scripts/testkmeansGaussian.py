import numpy as np

import matplotlib.pyplot as plt
import pylab
from km.kmeans import KMeans

def zscore(xy):
    return (xy-xy.mean())/xy.std()

# generate 3 sets of normally distributed points around
# different means with different variances
pt1 = np.random.normal(1, 0.1, (200,2))
pt2 = np.random.normal(5, 1.5, (500,2))
pt3 = np.random.normal(10, 1, (200,2))
 
data = np.concatenate((pt1, pt2, pt3))

   

#normalize z-score
#data = zscore(data)
 
# kmeans for 3 clusters
km = KMeans(showsubplots=False)
k,d,i = 3, 0.1, 10
means, labels = km.run(data, numberOfClusters=k, threshold=d, maxiterations=i)
print "final means: %s" % means

#if not subplot:
availcolors = [[0.4,1,0.4],[1,0.4,0.4],[0.5,0.5,1],[0.8,0.1,1],[0.8,1,0.1]]
colors = [availcolors[cluster] for cluster in labels]
pylab.title('final means')
pylab.scatter(data[:,0],data[:,1], c=colors)
 
# mark centroids as (X)
plt.scatter(means[:,0],means[:,1], marker='o', s = 500, linewidths=2, c='none')
plt.scatter(means[:,0],means[:,1], marker='x', s = 500, linewidths=2)
pylab.show()

