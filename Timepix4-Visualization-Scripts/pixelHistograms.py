"""
@author: uenalard

This script can be used to create a histogram which illustrates number packets sends
by the pixels versus number of pixels which send that much packets. It is written for 
24-bit raw data.
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

def countPackets(DATA):
    """
    This function counts packets pixel by pixel and add them into a list.
    """
    packetList = []

    for y in range(512):
        for x in range(448):
            count = DATA.count((x, y)) # .count function is one of the built in function in Python which counts given element in the list.
            if count != 0:
                packetList.append(count)

    return packetList

def Histograms(data, PlotPath, fileNum):
    
    figName = PlotPath + '\\DATA_' + str(fileNum) + ".png"
    title = "Data" + str(fileNum)
    plt.figure(figsize = (10, 8))
    plt.hist(data, facecolor='g', edgecolor="red", alpha=0.75)
    plt.title("Number of Packets Acquired")
    plt.xlabel("Number of Packets")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.title(title)
    plt.savefig(figName)
    plt.clf()
    plt.close() 

def Configuration(FilePath, folder, fileNumCount):

    DATA              = ReadFile(FilePath)
    CleanedData       = CleanData(DATA)
    packages = countPackets(CleanedData)
    Histograms(packages, folder, fileNumCount)

if __name__ == "__main__":

    path = "C:\\Users\\uenalard\\Desktop\\LocalCodes\\DATA\\2022-08-18_24bit_PixelCTExp"
    os.chdir(path)

    subFolder = path + "\\PixPlots"
    try:                        
        os.mkdir(subFolder)
    except OSError:
        print ("Creation of the directory %s failed" % subFolder)
    else:
        print ("Successfully created the directory %s " % subFolder)

    file_num = len([name for name in os.listdir() if name.endswith('.bin')])

    file_num_counter = 0

    for file in os.listdir():
        if file.endswith('.bin'):
            file_path =f"{path}\\{file}"
            Configuration(file_path, subFolder, file_num_counter)
            file_num_counter += 1 