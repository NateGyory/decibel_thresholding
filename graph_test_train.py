import json
import numpy as np
import matplotlib.pyplot as pp

decibel_arr = []
anomaly_arr = []

with open('decibel_range_train.json') as json_file:
    data = json.load(json_file)
    decibel_arr = data['Decibels']

with open('decibel_range_test.json') as json_file:
    data = json.load(json_file)
    anomaly_arr = data['Anomalies']

val = 0.
train_ar = np.array(decibel_arr)
anomaly_ar = np.array(anomaly_arr)
pp.suptitle('Anomalies', fontsize=20)
pp.xlabel('Decibels', fontsize=18)
pp.plot(train_ar, len(train_ar) * [val], "bo")
pp.plot(anomaly_ar, len(anomaly_ar) * [val], "rx")
pp.show()
