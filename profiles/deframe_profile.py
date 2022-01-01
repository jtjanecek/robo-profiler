import sys
sys.path.append('/home/fourbolt/Documents/uya/robo/src')

import json

from utils import utils

data = {}

for server in ['mls', 'dmetcp']:

    with open(f'{server}_deframe_data.json', 'r') as f:
        mls_data = json.loads(f.read())

    mls_data_clean = []

    for i in range(len(mls_data)):
        mls_data[i][0][1] = utils.hex_to_bytes(mls_data[i][0][1])
        i_data = mls_data[i][0][1]

        d_data = []
        for j in range(len(mls_data[i][1])):
            d = utils.hex_to_bytes(mls_data[i][1][j][1])
            d_data.append(d)
        if d_data != []:
            mls_data_clean.append([i_data, d_data])
    data[server] = mls_data_clean

def deframe_accuracy(deframe_class):
    print("Checking accuracy ...")

    for server, packets in data.items():
        deframer = deframe_class()
        print(f" -- Checking {server} ...")
        for input_data, results in packets:
            deframed = deframer.deframe([input_data])
            if deframed != results:
                print("Incorrect match.")
                print(f" Input: {input_data}")
                print(f" Got: {deframed}")
                print(f" Expected: {results}")  
                raise AssertionError()

def deframe_profile(deframe_class):
    for server, packets in data.items():
        deframer = deframe_class()
        for input_data, results in packets:
            deframed = deframer.deframe([input_data])


if __name__ == '__main__':
    from utils.rtbufferdeframer import RtBufferDeframer

    deframe_accuracy(RtBufferDeframer)

    import timeit
    t = timeit.Timer('deframe_profile(RtBufferDeframer)', setup='from __main__ import deframe_profile; from utils.rtbufferdeframer import RtBufferDeframer')
    print(t.repeat(repeat=20, number=100))

