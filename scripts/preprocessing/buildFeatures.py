import json
from pprint import pprint
import os

#Build features to a single file

if __name__ == '__main__':
#    path = os.path.dirname(__file__)
#    inputfile1 = os.path.join(path, '../data/data.txt')

#    filename = '/home/sigurdurm/Dropbox/Thesis/_Data/Examples/user_design.json'
    filename = '/home/sigurdurm/Downloads/anonymdata_b_noevents.txt'
    
    d = {}
    dunknown = {}
    
    with open(filename) as data_file:
        for line in data_file:
#            pprint(line)        
            jdata = json.loads(line)
            
            if jdata['category'] != 'user': #Ignore user categories
            
    #            import pdb;pdb.set_trace()
                raw = jdata['data']['event_id']
                prefix = raw[:3]
                event = raw[3:] #strip gb: and fb: prefix
                
                if prefix == 'gp:' or prefix == 'fb:':
                    user = jdata['data']['user_id']
                    
                    if not d.has_key(user):
                        d[user] = [0,0,0]
                        
                    if event == 'actions:load:login': #logging into areas
                        d[user][0] = d[user][0] + 1
                    elif event == 'actions:battle:battleBegin':
                        d[user][1] = d[user][1] + 1
#                    elif event[:12] == 'premiumSpent' or event[:16] == 'actions:purchase':
                    elif event[:16] == 'actions:purchase':
                        d[user][2] = d[user][2] + 1
#                
#    
    print '\n'    
    print 'writing out values %s' % len(d)
    with open('users_trainingdata_just_purchase.txt', 'w') as filebyvalues:
#        i = 0
        for k,v in d.iteritems():
#            filebyvalues.write('%s %s\n' % (str(k), ' '.join(map(str, v))))
            filebyvalues.write('%s\n' % ' '.join(map(str, v)))
#            i += 1
#            if i == 10:
#                break
        
    
    print 'done.'