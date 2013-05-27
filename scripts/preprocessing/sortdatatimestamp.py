import json
from pprint import pprint
import os


class TimestampEvent():
    def __init__(self, ts, user, event):
        self.ts = ts
        self.user = user
        self.event = event
        
    def __repr__(self):
        return json.dumps(self.__dict__)

if __name__ == '__main__':
#    path = os.path.dirname(__file__)
#    inputfile1 = os.path.join(path, '../data/data.txt')

#    filename = '/home/sigurdurm/Dropbox/Thesis/_Data/Examples/user_design.json'
    filename = '/home/sigurdurm/Downloads/anonymdata_b_noevents.txt'
    
    d = {}
    listts = []
    
    with open(filename) as data_file:
        for line in data_file:
#            pprint(line)        
            jdata = json.loads(line)
            
            if jdata['category'] != 'user': #Ignore user categories
            
                raw = jdata['data']['event_id']
                prefix = raw[:3]
                event = raw[3:] #strip gb: and fb: prefix
                
                if prefix == 'gp:' or prefix == 'fb:':
                    ts = jdata['arrival_ts']                    
                    user = jdata['data']['user_id']
                    listts.append(TimestampEvent(ts, user, event))
                    
                    
    print '\n'    
    print 'sort by ts\n'
    print 'num elements: %s' % len(listts)
    listts.sort(key = lambda tsevent: tsevent.ts)
    print 'write to file...'
    with open('sortedbytimestamps.txt', 'w') as filebyvalues:
        for itemts in listts:
            filebyvalues.write(repr(itemts))
            filebyvalues.write('\n')
    
                
    
    print 'done'    
    
    
#        pprint(jdata)