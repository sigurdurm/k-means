import json
from pprint import pprint
import os


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
            
            if jdata['category'] == 'user': #Ignore user categories
                continue
            
#            import pdb;pdb.set_trace()
            raw = jdata['data']['event_id']
            prefix = raw[:3]
            event = raw[3:] #strip gb: and fb: prefix
            if prefix != 'gp:' and prefix != 'fb:':
                if dunknown.has_key(raw):
                    dunknown[raw] = dunknown[raw] + 1
                else:
                    dunknown[raw] = 1
            else :    
    #            print(event)
    
                if d.has_key(event):
                    d[event] = d[event] + 1
                else:
                    d[event] = 1
                    
                premium = event[:12]
                if premium != 'premiumSpent':
                    continue
                
                if d.has_key(premium):
                    d[premium] = d[premium] + 1
                else:
                    d[premium] = 1
                
    
    print '\n'    
    print 'sort by values\n'
    with open('sortedbycounts.txt', 'w') as filebyvalues:
        for k,v in sorted(d.items(), key=lambda x: x[1], reverse=True):
#            print v,k
            filebyvalues.write(str(v))
            filebyvalues.write('\t')
            filebyvalues.write(k)
            filebyvalues.write('\n')
            
    print '\n'
    print 'sort by keys\n'
    with open('sortedbyevents.txt', 'w') as filebyvalues:
        for k,v in sorted(d.items()):
#            print k,v
            filebyvalues.write(k)
            filebyvalues.write('\t')
            filebyvalues.write(str(v))
            filebyvalues.write('\n')
            
            
    print '\n'
    print 'sort by keys unknown\n'
    with open('sortedbyeventsUnknown.txt', 'w') as filebyvalues:
        for k,v in sorted(dunknown.items()):
#            print k,v
            filebyvalues.write(k)
            filebyvalues.write('\t')
            filebyvalues.write(str(v))
            filebyvalues.write('\n')
        
        filebyvalues.write('Total\n')
        filebyvalues.write(str(len(dunknown)))
    
#        pprint(jdata)