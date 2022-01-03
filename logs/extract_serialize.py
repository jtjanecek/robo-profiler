import json
import sys
sys.path.append("/home/fourbolt/Documents/uya/robo/src")
from enums.rtid import RtId
from utils import utils

def serialize(data: bytes) -> bytes:
    rt_info = RtId.map[data[0]]

    serialized = rt_info['serializer'].serialize(data)

    return serialized


for server_name in ['mls']:
    with open(f"{server_name}_deframe.json", 'r') as f:
        data = json.loads(f.read())
    all_packets = []
    for i in data:
        for j in i[1]:
            if type(j) == list:
                for z in j:
                    all_packets.append(z)
            else:
                all_packets.append(j)

    all_packets = [utils.hex_to_bytes(packet) for packet in all_packets]

    serialized = []
    for packet in all_packets:
        s = serialize(packet)

        for key in s.keys():
            if type(s[key]) == bytes:
                s[key] = utils.bytes_to_hex(s[key])
            if 'payload' in s.keys():
                for key in s['payload'].keys():
                    if type(s['payload'][key]) == bytes:
                        s['payload'][key] = utils.bytes_to_hex(s['payload'][key])
 
        serialized.append([utils.bytes_to_hex(packet), s])

    with open(f'{server_name}_serialized.json', 'w') as f:
        f.write(json.dumps(serialized, indent=4))

    #with open(f"{server_name}_serialized", 'w') as f:


