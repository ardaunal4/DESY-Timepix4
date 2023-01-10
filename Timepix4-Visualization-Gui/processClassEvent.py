#import daq
import numpy as np
from numba import jit

def readFile(fileName):
    """
    It reads data from a directory with given path, decodes the data and it returns list of decoded data.
    """
    data = np.load(fileName)
    #event_decoded = daq.eventdecode.processevents(data)   
    event_decoded = 0

    return event_decoded

def totImageConf(Data):

    cleandData = []

    for item in Data:
        if str(item[0]) == 'PacketType.PixelData':
            cleandData.append(item[1:5])

    return cleandData

def cleanData(DATA):
    """
    It cleans data if there is any other types and remove class types of the data
    """
    cleandData = []

    for item in DATA:
        if str(item[0]) == 'PacketType.PixelData':
            cleandData.append(item[1:5])

    sortedData = sorted(cleandData, key=lambda x: x[2])
    return sortedData

@jit
def eventList(DATA):

    timeStamps = []
    for item in DATA:
        if item[2] not in timeStamps:
            timeStamps.append(item[2]) 

    finalEventList = []       
    eventList = []

    for time in timeStamps:
        for item in DATA :
            if time == item[2]:
                eventList.append(item)
            
        finalEventList.append(eventList)
        eventList = []
        
    return finalEventList

@jit
def CreateImage(DATA):
    """
    In this function, image consists of only pixels which send out total count values.
    """
    nrows, ncols = 512, 448                                                                     
    image = np.zeros((nrows, ncols)) 

    for item in DATA:
        if item[3] > 0.0:
            image[item[1], item[0]] += item[3]

    for row in range(nrows):
        for col in range(ncols):
            if image[row, col] > 0:
                image[row, col] = np.log10(image[row, col])

    return image 
