import sys
sys.path.append('/home/fourbolt/Documents/uya/robo/src')

import json

from utils import utils

data = {}

for server in ['mls', 'dmetcp']:

    with open(f'{server}_deframe_data.json', 'r') as f:
        mls_data = json.loads(f.read())

    for i in range(len(mls_data)):
        mls_data[i][0][1] = utils.hex_to_bytes(mls_data[i][0][1])
        i_data = mls_data[i][0][1]

        d_data = []
        for j in range(len(mls_data[i][1])):
            d = utils.hex_to_bytes(mls_data[i][1][j][1])
            d_data.append(d)
        mls_data[i] = [i_data, d_data]
    data[server] = mls_data


def deframe_profile(deframe_class):
    print("Checking accuracy ...")

    deframer = deframe_class()
    
