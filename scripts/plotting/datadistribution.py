import os.path
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt
from util.utilities import Utils
from collections import Counter
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from numpy.random import random
import scipy.stats as stats




#data = 'zdata.txt'
data = 'zdata_incl_purchase.txt'
fn = os.path.join(os.path.dirname(__file__), data)
print "opening file %s" % fn

points = np.loadtxt(fn)
#import pdb;pdb.set_trace()

#normalize using z-score
#points = Utils.zscore(points)
#points = Utils.sigmoid(points)

#pca = decomposition.PCA(n_components=2)
#pca.fit(points)
#points = pca.transform(points)

#Histogram
#Login
#title = "Login Histogram"
#xlabel = 'Logins'
#plt.hist(points[:,0], bins=(0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,220), normed=False, rwidth=0.8) #max20
#plt.hist(points[:,0], bins=(20,30,40,50,60,70,80,90,100,110,120,130,140,150,175,200,220), normed=False, rwidth=0.8) #min20
#Battle
#title = "Battle Histogram"
#xlabel = 'Battles'
#plt.hist(points[:,1], bins=(0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100), normed=False, rwidth=0.8)
#plt.hist(points[:,1], bins=(20,30,40,50,60,70,80,90,100,110,120,130,140,150,175,200,250,300,350,400,440), normed=False, rwidth=0.8) #min20
#Premium
#title = "In-game Purchases Histogram"
#xlabel = 'Purchases'
#plt.hist(points[:,2], bins=(0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100), normed=False, rwidth=0.8)
##plt.hist(points[:,2], bins=(20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100), normed=False, rwidth=0.8) #min20
#
#plt.title(title)
#plt.xlabel(xlabel)
#plt.ylabel('Count of Players')
#plt.show()

#BoxPlots
#plt.boxplot(points[:,1]) #vertical
#plt.boxplot(points[:,2],0,'rs',0) #horizontal
#plt.boxplot(points[:,0])
#plt.boxplot(points) #multiple plots
#plt.show()


# 3D Plot
fig = plt.figure()
ax3D = fig.add_subplot(111, projection='3d')
ax3D.scatter(points[:, 0], points[:, 1], points[:, 2], s=30, marker='o') 
ax3D.set_xlabel('Logins')
ax3D.set_ylabel('Battles')
ax3D.set_zlabel('PremiumSpent')
plt.show()

#mpl.rcParams['legend.fontsize'] = 10
#
#fig = plt.figure(1)
#fig.clf()
#ax = Axes3D(fig)
#datasets = random((8,100,3))*512
#my_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
#
#colors = ['k', "#B3C95A", 'b', '#63B8FF', 'g', "#FF3300",
#          'r', 'k']
#index = 0
##for data, curr_color in zip(points, colors):
#    ax.plot(points[:, 0], points[:, 1], 
#                   points[:, 2], 'o', c=curr_color, label=my_labels[index])
#    index += 1
#
#ax.set_zlim3d([-1, 9])
#ax.set_ylim3d([-1, 9])
#ax.set_xlim3d([-1, 9])
#
#ax.set_xticks(range(0,11))
#ax.set_yticks([1,2,8])
#ax.set_zticks(np.arange(0,9,.5))
#
#ax.legend(loc = 'upper left')
#
#plt.draw()
#
#plt.show()


