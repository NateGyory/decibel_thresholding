import numpy as np
import pyaudio
import wave
import math
import statistics
import sys
import json
import multiprocessing
import time

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "output.wav"

max_db = -sys.maxsize - 1
min_db = sys.maxsize

json_dict = {'Min' : min_db,'Max': max_db, 'Decibels' : []}

def write_to_file():
    global json_dict
    with open('decibel_range_train.json', 'w') as outfile:
        json.dump(json_dict, outfile)
        outfile.close()

def callback(input_data, frame_count, time_info, flags):
    global max_db, min_db
    sound = np.fromstring(input_data, dtype=np.int16)
    chunk = sound.astype('int64')
    sqr = chunk**2
    mean = statistics.mean(sqr)
    sqrt = math.sqrt(mean)
    log = 20*math.log10(sqrt)
    if log > max_db:
        max_db = log
        json_dict['Max'] = log
        print('New Max:', max_db)

    if log < min_db:
        min_db = log
        json_dict['Min'] = log
        print('New Min:', min_db)

    json_dict['Decibels'].append(log)

    return input_data, pyaudio.paContinue


pa = pyaudio.PyAudio()
chosen_device_index = -1
for x in range(0,pa.get_device_count()):
    info = pa.get_device_info_by_index(x)
    if info["name"] == "pulse":
        chosen_device_index = info["index"]


stream = pa.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input_device_index=chosen_device_index,
                    input=True,
                    stream_callback=callback,
                    frames_per_buffer=CHUNK)

time.sleep(10)

write_to_file()
