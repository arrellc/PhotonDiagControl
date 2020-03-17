import json

GasOnList = {
    'SAROP11-CVME-PBPS1-EVR0:FrontUnivOut0-Ena-SP': 'Enabled',
    'SAROP11-CVME-PBPS1-EVR0:FrontUnivOut1-Ena-SP': 'Enabled'
}

with open('GasOn.json', 'w') as json_file:
    json.dump(GasOnList, json_file)
