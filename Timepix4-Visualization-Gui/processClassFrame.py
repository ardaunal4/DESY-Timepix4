import numpy as np
#import daq
from numba import jit

def read24bitFrameFile(fileName):
    """
    It reads data from a directory with given path, decodes the data and it returns list of decoded data.
    """
    data = np.load(fileName)
    #frame_24bits_decoded = daq.eventdecode.processevents(data, PC24bit  = True) 
    frame_24bits_decoded = 0

    return frame_24bits_decoded

def Clean24bitData(DATA):
    """
    It cleans data if there is any other types and remove class types of the data
    """
    cleandData = []

    for item in DATA:
        if str(item[0]) == "PacketType.PC24bitData":
            cleandData.append(item)

    data = [item[1::] for item in cleandData] 

    return data

@jit
def CreateFrameImage(DATA):
    """
    In this function, image consists of only pixels which send out total count values.
    """
    nrows, ncols = 512, 448                                                                     
    image = np.zeros((nrows, ncols)) 

    for item in DATA:
        if item[2] >= 0.0:
            image[item[1], item[0]] += item[2]

    
    for c1 in range(nrows):
        for c2 in range(ncols):
            if image[c1, c2] != 0:
                image[c1, c2] = np.log10(image[c1, c2])

    return image 

def read816bitFrameFile(fileName, readoutmode):
    """
    It reads data from a directory with given path, decodes the data and it returns list of decoded data.
    """
    data = np.load(fileName)  

    if readoutmode == "16-bit mode":
        pass
        #mydec = daq.FrameDecoder(1, daq.ReadoutMode.Frame16bit)
    else:
        pass
        #mydec = daq.FrameDecoder(1, daq.ReadoutMode.Frame8bit)

    #image = mydec.framedecodesingle(data)
    image = 0
    
    return image
