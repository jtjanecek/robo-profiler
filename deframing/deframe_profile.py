import sys
sys.path.append('/home/fourbolt/Documents/uya/robo/src')

import numpy as np
import time
import json
import datetime

from utils import utils

data = {}
def read_json(server):
    with open(f'../logs/{server}.json', 'r') as f:
        loaded = json.loads(f.read())
    for i in range(len(loaded)):
        loaded[i][0] = utils.hex_to_bytes(loaded[i][0])
        for j in range(len(loaded[i][1])):
            loaded[i][1][j] = utils.hex_to_bytes(loaded[i][1][j])
    data[server] = loaded

read_json('mls')
read_json('dmetcp')

def deframe_accuracy(deframe_class):
    print("Checking accuracy ...")

    for server, packets in data.items():
        deframer = deframe_class()
        print(f" -- Checking {server} ...", end='   ')
        for input_data, results in packets:
            deframed = deframer.deframe(input_data)
            if deframed != results:
                print("\n")
                print("Incorrect match.")
                print(f" Input: {input_data}")
                print(f" Got: {deframed}")
                print(f" Expected: {results}")  
                raise AssertionError()
        print("Done")

def deframe_profile(deframe_class):
    for server, packets in data.items():
        deframer = deframe_class()
        for input_data, results in packets:
            deframed = deframer.deframe(input_data)

'''
for input_data, results in data['dmetcp']:
    for result in results:
        if result not in input_data:
            print(input_data, results)
            import sys; sys.exit()


'''
if __name__ == '__main__':
    from utils.rtbufferdeframer import RtBufferDeframer

    deframe_accuracy(RtBufferDeframer)

    print(f"{datetime.datetime.now()} | Running profiling ...")
    init_time = time.time()
    import timeit
    t = timeit.Timer('deframe_profile(RtBufferDeframer)', setup='from __main__ import deframe_profile; from utils.rtbufferdeframer import RtBufferDeframer')
    total_time = t.repeat(repeat=20, number=40)
    print("Profiled time:",total_time)
    print(f"Mean: {np.mean(total_time)}")
    print("Real time (min):", (time.time()-init_time) / 60)


