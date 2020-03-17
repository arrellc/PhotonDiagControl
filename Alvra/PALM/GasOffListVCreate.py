import json

GasOffList = {
    'SAROP11-CVME-PBPS1-EVR0:FrontUnivOut0-Ena-SP': 'Disabled',
    'SAROP11-CVME-PBPS1-EVR0:FrontUnivOut1-Ena-SP': 'Disabled'
}

with open('GasOff.json', 'w') as json_file:
    json.dump(GasOffList, json_file)
