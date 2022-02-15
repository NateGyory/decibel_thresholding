import json
import numpy as np
import matplotlib.pyplot as pp

decebel_arr = []

with open('decibel_range_train.json') as json_file:
    data = json.load(json_file)
    decebel_arr = data['Decibels']

val = 0. # this is the value where you want the data to appear on the y-axis.
ar = np.array(decebel_arr) # just as an example array
pp.suptitle('Training Decibel Range', fontsize=20)
pp.xlabel('Decibels', fontsize=18)
pp.plot(ar, len(ar) * [val], "x")
pp.show()
