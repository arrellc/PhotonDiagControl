import json
from epics import caget,caput
fn = 'OffList.json'

with open(fn) as json_file:
    
    PV_list = json.load(json_file)

for i in PV_list:
    caput(i,PV_list[i])
    print('Set:',i, 'to',caget(i))
