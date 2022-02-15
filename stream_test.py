import numpy as np
import pyaudio
import wave
import math
import statistics
import sys
import json
import time

import wave


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "output.wav"

file = open(r'./decibel_range_train.json', 'r')
json_dict_train = json.load(file)
file.close()

json_dict_test = {'Anomalies' : []}

max_db = json_dict_train['Max']
min_db = json_dict_train['Min']
anomaly_data = []

def write_to_file():
    global json_dict_test, anomaly_data
    with open('decibel_range_test.json', 'w') as outfile:
        json.dump(json_dict_test, outfile)
        outfile.close()

    with wave.open("anomaly.wav", "wb") as out_f:
        out_f.setnchannels(1)
        out_f.setsampwidth(2) # number of bytes
        out_f.setframerate(48000)
        out_f.writeframesraw(b''.join(anomaly_data))

def callback(input_data, frame_count, time_info, flags):
    global max_db, min_db, json_dict_test, anomaly_data
    sound = np.fromstring(input_data, dtype=np.int16)
    chunk = sound.astype('int64')
    sqr = chunk**2
    mean = statistics.mean(sqr)
    sqrt = math.sqrt(mean)
    log = 20*math.log10(sqrt)
    if log > max_db:
        print('ANOMALY: ', log)
        json_dict_test["Anomalies"].append(log)
        anomaly_data.append(input_data)

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
