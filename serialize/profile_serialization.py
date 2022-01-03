import json
import sys
sys.path.append("/home/fourbolt/Documents/uya/robo/src")
from enums.rtid import RtId
from utils import utils

import numpy as np
import datetime
import time

def serialize(data: bytes) -> bytes:
    rt_info = RtId.map[data[0]]

    serialized = rt_info['serializer'].serialize(data)

    return serialized

def hexize(s):
    for key in s.keys():
        if type(s[key]) == bytes:
            s[key] = utils.bytes_to_hex(s[key])
        if 'payload' in s.keys():
            for key in s['payload'].keys():
                if type(s['payload'][key]) == bytes:
                    s['payload'][key] = utils.bytes_to_hex(s['payload'][key])

with open(f"../logs/mls_serialized.json", 'r') as f:
    data = json.loads(f.read())

def check_accuracy():
    print("Checking accuracy ...")

    for input_data, result in data:
        input_data = utils.hex_to_bytes(input_data)
        
        serialized = serialize(input_data)
        hexize(serialized)
        
        if serialized != result:
            print("\n")
            print("Incorrect match.")
            print(f" Input: {input_data}")
            print(f" Got: {serialized}")
            print(f" Expected: {result}")  
            raise AssertionError()
    print("Done")

def serialize_profile():
    for input_data, result in data:
        input_data = utils.hex_to_bytes(input_data)
        
        serialized = serialize(input_data)

if __name__ == '__main__':

    check_accuracy()


    print(f"{datetime.datetime.now()} | Running profiling ...")
    init_time = time.time()
    import timeit
    t = timeit.Timer('serialize_profile()', globals = globals())
    total_time = t.repeat(repeat=20, number=100)
    print("Profiled time:",total_time)
    print(f"Mean: {np.mean(total_time)}")
    print("Real time (min):", (time.time()-init_time) / 60)






