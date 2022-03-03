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

current_file_num = json_dict_test['file_number']

# These buffers are used to store the anomaly wav file
anomaly_data = []
pre_buffer = []
post_buffer = []

# Counts to satify the respective buffers record for the right amount of time
anomaly_done_count = 0
post_buffer_done_count = 0

# Number of frames to satify time duration
THREE_SECONDS = 138
TWO_SECONDS = 92
ONE_SECOND = 46

# Need an anomaly flag in order to keep track of state.
anomaly_flag = False

def callback(input_data, frame_count, time_info, flags):
    global max_db, min_db, anomaly_data, pre_buffer, post_buffer,
           anomaly_done_count, TWO_SECONDS, anomaly_flag, ONE_SECOND,
           process_post_buffer, file_number, json_dict_test

    sound = np.fromstring(input_data, dtype=np.int16)
    chunk = sound.astype('int64')
    sqr = chunk**2
    mean = statistics.mean(sqr)
    sqrt = math.sqrt(mean)
    log = 20*math.log10(sqrt)

    # Record 1 second of noise for the post buffer
    if process_post_buffer:
        post_buffer.append(input_data)
        post_buffer_done_count += 1
        if post_buffer_done_count == ONE_SECOND:
            process_post_buffer = False

            # Save to file
            file_name = "anomaly_{}.wav".format(file_number)

            with wave.open(file_name, "wb") as out_f:
                out_f.setnchannels(1)
                out_f.setsampwidth(2) # number of bytes
                out_f.setframerate(48000)
                out_f.writeframesraw(b''.join(pre_buffer).join(anomaly_data).join(post_buffer))

            # incriment file_number and save
            file_number += 1
            with open('decibel_range_test.json', 'w') as outfile:
                json.dump(json_dict_test, outfile)
                outfile.close()

    # Anomaly has occured
    elif log > max_db:
        print('ANOMALY: ', log)
        anomaly_data.append(input_data)

        anomaly_flag = 1

    elif anomaly_flag:
        anomaly_data.append(input_data)
        anomaly_done_count += 1

        if anomaly_done_count == TWO_SECONDS:
            anomaly_flag = False
            anomaly_done_count = 0
            process_post_buffer = True

    # This is the case for adding to the pre_buffer
    else:
        if len(pre_buffer) >= (THREE_SECONDS * 1024):
            del pre_buffer[:1024]

        pre_buffer = input_data + pre_buffer



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
while(1)
