from collections import defaultdict
inputs = defaultdict(list)


def bytes_to_hex(data:bytes):
    return data.hex().upper()

def hex_to_bytes(hex:str):
    return bytes(bytearray.fromhex(hex))

with open('main.log','r') as f:
    for line in f:
        server = line.split("robo.")[-1].split()[0]
        if server in ['dmeudp','nat']:
            continue
        if '| I |' in line:
            inputs[server].append(['i',line.split("| I |")[-1].strip()])
        elif 'Deframe |' in line:
            inputs[server].append(['d',line.split("| ")[-1].strip()])
   
'''
Deframe
'''

pairs = defaultdict(list)

for server in inputs.keys():
    while len(inputs[server]) != 0:
        i = inputs[server].pop(0)    
        d = []
        while len(inputs[server]) > 0 and inputs[server][0][0] != 'i':

            d.append(inputs[server].pop(0))

        pairs[server].append([i,d])

import json

data = {}
for server in ['mls', 'dmetcp']:
    
    mls_data = pairs[server]

    mls_data_clean = []

    for i in range(len(mls_data)):
        i_data = mls_data[i][0][1]

        d_data = []
        for j in range(len(mls_data[i][1])):
            d = mls_data[i][1][j][1]
            d_data.append(d)
        if d_data != []:
            mls_data_clean.append([i_data, d_data])

    with open(f'{server}_deframe.json', 'w') as f:
        f.write(json.dumps(mls_data_clean, indent=4))
    

