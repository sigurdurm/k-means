import os.path
from km.kmeans import KMeans
from sklearn import decomposition
import pylab
from util.utilities import Plot

fn = os.path.join(os.path.dirname(__file__), 'data/iris-dat.dat')
print "opening file %s" % fn

f = open(fn)
items = [map(int, line.strip().split()) for line in f.readlines()]
f.close()

pca = decomposition.PCA(n_components=2)
pca.fit(items)
points = pca.transform(items)

#print items

# run kmeans
km = KMeans(showsubplots=False)
k,d,i = 3, 0.1, 10
means, labels = km.run(points, numberOfClusters=k, threshold=d, maxiterations=i)
print "final means: %s" % means


Plot.plotPoints(points, labels, title='final')
Plot.plotMeans(means)
pylab.show()
