import json
from pprint import pprint
import os


if __name__ == '__main__':
#    path = os.path.dirname(__file__)
#    inputfile1 = os.path.join(path, '../data/data.txt')

#    filename = '/home/sigurdurm/Dropbox/Thesis/_Data/Examples/user_design.txt'
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
            user = jdata['data']['user_id']
#            event = raw[3:] #strip gb: and fb: prefix
#            pprint(user)
#            pprint(prefix)
#            if prefix != 'gp:' and prefix != 'fb:':
#                if dunknown.has_key(raw):d
#                    dunknown[raw] = dunknown[raw] + 1
#                else:
#                    dunknown[raw] = 1
#            else :    
    #            print(event)
            if d.has_key(user):
                d[user] = d[user] + 1
            else:
                d[user] = 1
    
        
    print '\n'    
    print 'Players'
    with open('Players.txt', 'w') as filebyvalues:
        for k,v in sorted(d.items(), key=lambda x: x[1], reverse=True):
#            print v,k
            filebyvalues.write(str(v))
            filebyvalues.write('\t')
            filebyvalues.write(k)
            filebyvalues.write('\n')
        
        filebyvalues.write(str(len(d)))
       
        