import pylab
from km.kmeans import KMeans
from util.utilities import *


if __name__ == '__main__':   
    # kmeans for 3 clusters
    km = KMeans(showsubplots=False)
    k,d,i = 3, 0.1, 10
    data, centroids = Utils.generateTestDataAndCentroids(k, dimensions=2)
    means, labels = km.run(data, numberOfClusters=k, threshold=d, maxiterations=i)
    print "final means: \n%s" % means
    
    #if not subplot:
    Plot.plotPoints(data, labels, title='final means')
    Plot.plotMeans(means)
    pylab.show()
