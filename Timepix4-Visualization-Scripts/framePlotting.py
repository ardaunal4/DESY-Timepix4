"""
Created on Fri July 29 09:10:10 2022

@author: uenalard
"""
import numpy as np
from ..eventdecode import processevents
import matplotlib.pyplot as plt
import matplotlib.image as img

data = []

# Reading data from a file
dtype = np.dtype('B')
try:
    with open(r"C:\Users\uenalard\Desktop\LocalCodes\DATA\2022-07-28_30MHz_24bit_countthreshold_1024.bin", "rb") as f:
        data = np.fromfile(f, dtype)
except IOError:
    print('Error While Opening the file!')

frame_24bits_decoded = processevents(np.array(data), PC24bit  = True)            # Decoding

# There were tuple type datas in the dataset, thus I cleaned them.
for i in range(2):
    for item in frame_24bits_decoded:
        if str(type(item)) != "<class 'list'>":
            frame_24bits_decoded.remove(item)
        else:
            pass
    
data = [item[1::] for item in frame_24bits_decoded]                                          # Remove class types of the data

# If a pixel readed out by 2 times, its counter values is added below
for item1 in data:
    for item2 in data:
        if item1[0] == item2[0] and item1[1] == item2[1]:
            item1[2] += item2[2]
            data.remove(item2)

values = []
# I scale values in logarithmic scale to see all values in the image
for item in data:
    if item[2] != 0:                                                                         # If value is nonzero, then logarithmic rescale occurs
        item[2] = np.log(item[2])
    else:
        item[2] = -10                                                                        # If value is equal to zero, then it is assigned as -10
    values.append(item[2])
 
nrows, ncols = 512, 448                                                                      # Image size
image = np.zeros((nrows, ncols))                                                             # Creating a blank image

# Filling image
for item in data:
    image[item[1], item[0]] = item[2]

fig = plt.figure(figsize = (10, 8))                                                          # Create a figure
plt.title("2022-07-28_30MHz_24bit_countthreshold_256")                                       # Put a title
plt.imshow(image, cmap = 'viridis', vmin = -10, vmax = max(values))
cax = plt.axes([0.9, 0.1, 0.060, 0.8])
plt.colorbar(cax = cax)                                                                      # Scaling values
plt.show()