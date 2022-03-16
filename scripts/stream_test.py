import numpy as np
import pyaudio
import wave
import math
import statistics
import sys
import json
import time

import wave


# pyaudio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "output.wav"

# Read Max and Min decibel values from the training config
file = open(r'../config/decibel_range_train.json', 'r')
json_dict_train = json.load(file)
file.close()

max_db = json_dict_train['Max']
min_db = json_dict_train['Min']

# Read current file number from the testing config
file = open(r'../config/decibel_range_test.json', 'r')
json_dict_test = json.load(file)
file.close()

file_number = json_dict_test['file_number']

# Buffer used to store anomaly sound data
anomaly_data = []

# Only record Anomaly if the anomalous sound lasts atleast 2 seconds
anomaly_done_count = 0

# Number of frames to satify time duration
TWO_SECONDS = 92

def callback(input_data, frame_count, time_info, flags):
    global max_db, min_db, anomaly_data, anomaly_done_count, TWO_SECONDS, file_number, json_dict_test

    # dB calculation
    sound = np.fromstring(input_data, dtype=np.int16)
    chunk = sound.astype('int64')
    sqr = chunk**2
    mean = statistics.mean(sqr)
    sqrt = math.sqrt(mean)
    log = 20*math.log10(sqrt)

    # Anomaly has occured
    if log > max_db:
        print('ANOMALY: ', log)
        anomaly_data.append(input_data)

        anomaly_done_count += 1

    # Anomaly Done
    elif anomaly_done_count > TWO_SECONDS:

        file_name = "../anomalies/anomaly_{}.wav".format(file_number)

        with wave.open(file_name, "wb") as out_f:
            out_f.setnchannels(1)
            out_f.setsampwidth(2) # number of bytes
            out_f.setframerate(48000)
            out_f.writeframesraw(b''.join(anomaly_data))

        # incriment file_number and save
        file_number += 1
        with open('../config/decibel_range_test.json', 'w') as outfile:
            json_dict_test['file_number'] = file_number
            json.dump(json_dict_test, outfile)
            outfile.close()

        anomaly_data.clear()
        anomaly_done_count = 0

    # No anomaly
    else:
        anomaly_done_count = 0
        anomaly_data.clear()

    return input_data, pyaudio.paContinue


##########
#  Main  #
##########

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

# Need to spin loop indefinately
while True:
    pass

