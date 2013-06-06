import json
from pprint import pprint
import os
import glob
import numpy as np
from util import Utils

#Builds game features for multiple files.

if __name__ == '__main__':
#    filespath = '/home/sigurdurm/Downloads/anonymdata_b_noevents_split.*'
    filespath = '/home/sigurdurm/Downloads/multiple/sortedtimestamp/*split*'
#    
    files = glob.glob(filespath)
    for filename in files:
        fileout = filename + '.dat'
        d = {}
        with open(filename) as data_file:
            for line in data_file:
    #            pprint(line)        
                jdata = json.loads(line)
                
                #Working with sorted timestamp data
                user = jdata['user']
                event = jdata['event']
                
                if not d.has_key(user):
                    d[user] = [0,0,0]

                if event == 'actions:load:login': #logging into areas
                    d[user][0] = d[user][0] + 1
                elif event == 'actions:battle:battleBegin':
                    d[user][1] = d[user][1] + 1
                elif event[:12] == 'premiumSpent':
#                    elif event[:12] == 'premiumSpent' or event[:16] == 'actions:purchase':
#                        elif event[:16] == 'actions:purchase':
                    d[user][2] = d[user][2] + 1
#                
#    
        print '\n'    
        print 'writing out values %s' % len(d)
#        with open('users_trainingdata_just_purchase.txt', 'w') as filebyvalues:
        with open(fileout, 'w') as filebyvalues:
    #        i = 0
            for k,v in d.iteritems():
    #            filebyvalues.write('%s %s\n' % (str(k), ' '.join(map(str, v))))
                filebyvalues.write('%s\n' % ' '.join(map(str, v)))
    #            i += 1
    #            if i == 10:
    #                break
        
    
        print 'done.'
    print 'Alle done!'
    
    

    #Normalize files and pick random distinct initial centroids
    files = glob.glob(filespath + '.dat')
    for filename in files:
        data = np.loadtxt(filename)
        zscoredata = Utils.zscore(data)
        postfix = filename[-4:]     
        
        fileout = filename[:-4] + '_zscore' + postfix
        np.savetxt(fileout, zscoredata)
        
        k = 3 #3 features
        centroids = Utils.getInitialMeans(zscoredata, k)
        fileoutcentroids = filename[:-4] + '_zscore.centroids' + postfix
        np.savetxt(fileoutcentroids, centroids)
        print 'zscore saved: %s' % fileout
        
        
    