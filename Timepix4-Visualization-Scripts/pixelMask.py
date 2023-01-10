"""
@author: uenalard

This script detects count values of pixels and create a mask matrix as numpy file.
Then it is possible upload this mask matrix into Zynq and use it. For multiple files,
one should change the code in such a way that all mask numpy files should have different 
names.
"""
import numpy as np
from eventdecode import processevents
import matplotlib.pyplot as plt
import os

def ReadFile(PATH):
    """
    It reads data from a directory with given path, decodes the data and it returns list of decoded data.
    """
    data = np.load(PATH)
    frame_24bits_decoded = processevents(np.array(data), PC24bit  = True) 

    return frame_24bits_decoded

def CleanData(DATA):
    """
    It cleans data if there is any other types and remove class types of the data
    """
    cleandData = []

    for item in DATA:
        if str(item[0]) == "PacketType.PC24bitData":
            cleandData.append(item)

    data = [item[1:3] for item in cleandData] 

    return data

def masking(DATA):
    """
    Pixel mask function.
    """
    nrows, ncols = 512, 448                                                                      
    Pmatrix = np.zeros((nrows, ncols))

    for y in range(512):
        for x in range(448):
            count = DATA.count((x, y))                               # It counts number of packages which sent by the pixel.
            if count > 1:                                            # If pixel sends more than 1 package, by putting 1 to this coordinate, it masks this pixel.
                Pmatrix[y, x] = 1
            else:
                Pmatrix[y, x] = 0

    Pmatrix = Pmatrix.astype(np.uint8)                               # This code converts matrix, that is created above, data type into 8-bit unsigned integer

    return Pmatrix

def Configuration(FilePath, fileNumCount):

    DATA              = ReadFile(FilePath)
    CleanedData       = CleanData(DATA)
    pmatrix           = masking(CleanedData)
    path, filename    = os.path.split(FilePath)
    file_name         = path  + '\\maskMatrix.npy'

    with open(file_name, 'wb') as f:
        np.save(f, pmatrix)

if __name__ == "__main__":

    path = "C:\\Users\\uenalard\\Desktop\\LocalCodes\\DATA\\2022-08-18_24bit_PixelCTExp"
    os.chdir(path)

    file_num = len([name for name in os.listdir() if name.endswith('.bin')])
    file_num_counter = 0

    for file in os.listdir():
        if file.endswith('.bin'):
            file_path =f"{path}\\{file}"
            Configuration(file_path, file_num_counter)
            file_num_counter += 1 