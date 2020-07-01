import json

####
# user inputs
####
# edit the dict below e.g.
# ToAdd = {
#    'SAROP11-PALM118:HVDT1-SP.VAL': 0,
#    'SAROP11-PALM118:HVDT2-SP.VAL': 0,

ToAdd = {
    'SAROP11-PALM118:VALVE1-POWER-SP': 1,
    'SAROP11-PALM118:VALVE2-POWER-SP': 1,
    'SAROP11-PALM118:VALVE1-HV-ON-SP': 1,
    'SAROP11-PALM118:VALVE2-HV-ON-SP': 1
}

####
fn = 'GasOn.json'

with open(fn) as json_file:
    Current_json = json.load(json_file)
    Current_json.update(ToAdd)

#with open('fn', 'w') as json_file:
#    json.dump(Current_json, json_file)

print('Json updated:', json.dumps(Current_json))
