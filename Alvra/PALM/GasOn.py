import json
from epics import caget,caput
from time import sleep
fn =['ValveSetup.json', 'GasOn.json']

for name in fn:
    with open(name) as json_file:
    
        PV_list = json.load(json_file)

    for i in PV_list:
        caput(i,PV_list[i])
        sleep(5)
        print('Set:',i, 'to',caget(i))
