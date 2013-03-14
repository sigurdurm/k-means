import os.path
from km.kmeans import KMeans
from sklearn import decomposition
import matplotlib.pyplot as plt
import pylab

fn = os.path.join(os.path.dirname(__file__), 'data/iris-dat.dat')
print "opening file %s" % fn

f = open(fn)
items = [map(int, line.strip().split()) for line in f.readlines()]
f.close()



pca = decomposition.PCA(n_components=2)
pca.fit(items)
data = pca.transform(items)

#print items

# run kmeans
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