
from collections import defaultdict
inputs = defaultdict(list)

with open('main.log','r') as f:
    for line in f:
        server = line.split("robo.")[-1].split()[0]
        if server in ['dmeudp','nat']:
            continue
        if '| I |' in line:
            inputs[server].append(['i',line.split("| I |")[-1].strip()])
        elif 'Deframe |' in line:
            inputs[server].append(['d',line.split("| ")[-1].strip()])
   

pairs = defaultdict(list)

for server in inputs.keys():
    while len(inputs[server]) != 0:
        i = inputs[server].pop(0)    
        d = []
        while len(inputs[server]) > 0 and inputs[server][0][0] != 'i':

            d.append(inputs[server].pop(0))

        pairs[server].append([i,d])

import json
for server, data in pairs.items():
    data = json.dumps(data)
    with open(f"{server}_deframe_data.json", 'w') as f:
        f.write(data)

for a in pairs['mls']:
    print(a) 
