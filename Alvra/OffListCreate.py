import json

OffList = {
    'SAROP11-PALM118:HVMCP1-SP.VAL': 0,
    'SAROP11-PALM118:HVMCP2-SP.VAL': 0
}

with open('OffList.json', 'w') as json_file:
    json.dump(OffList, json_file)
