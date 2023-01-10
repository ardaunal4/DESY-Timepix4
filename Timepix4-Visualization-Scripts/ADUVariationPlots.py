"""
@author: uenalard

This script can be used for noise analysis of the pixels according to giving files. 
It is not essential to vary threshold values. It is possible to use another variable, 
but for the plots some title names, x-axis and y-axis names should be changed. It is 
written for 24-bit raw data.
"""
import numpy as np
from ..eventdecode import processevents
import matplotlib.pyplot as plt
import os

global Pmatrix, nrows, ncols

def ReadFile(PATH):
    """
    It reads data from a directory with given path, decodes the data and it returns list of decoded data.
    """

    data = np.load(PATH)
    frame_24bits_decoded = processevents(np.array(data), PC24bit  = True) 

    return frame_24bits_decoded

def CleanData(DATA):
    """
    It cleans data if there is any other types and remove class types of the data.
    """
    cleandData = []

    for item in DATA:
        if str(item[0]) == "PacketType.PC24bitData":
            cleandData.append(item)
        else:
            pass

    data = [item[1::] for item in cleandData]                                                   # It removes the packet names.

    return data

def FillMatrix(DATA, fileNum):
    """
    This function fills the matrix which is globally defined in the code according to file number.
    It creates a 3D matrix where the third dimension is basically number of files. 
    """

    global Pmatrix

    for item in DATA:
        if item[2] != 0:
            Pmatrix[item[1], item[0], fileNum] += item[2]
        else:
            Pmatrix[item[1], item[0], fileNum] = 0

    for c1 in range(nrows):
        for c2 in range(ncols):
            if Pmatrix[c1, c2, fileNum] != 0:
                Pmatrix[c1, c2, fileNum] = np.log10(Pmatrix[c1, c2, fileNum])                  # After filling matrix, it scales count values into the logaritmic scale.
            else:
                pass

def PlotPixels(PixMatrix, fileNum, PlotPath):
    """
    This function plots noise distribution according to threshold values individually for every pixel.
    After plot it saves the plots into subfolder which is created at main.
    """

    for c1 in range(nrows):
        for c2 in range(ncols):
            if sum(PixMatrix[c1, c2, ::]) != 0:
                figName = PlotPath + '\\Pix_' + str(c1) + "-" + str(c2) + ".png"
                title = "Pixel at x=" + str(c1) + ", y=" + str(c2)
                plt.figure(figsize = (10, 8))
                plt.plot(range(fileNum), PixMatrix[c1, c2, ::], color = "blue")
                plt.xlabel("Dataset Number")
                plt.ylabel("Pixel Count Values(Log10 Scale)")
                plt.title(title)
                plt.grid("on")
                plt.savefig(figName)
                plt.clf()                                                                      # It is essential to clear figure everytime. Otherwise they will be overwritten on the same figure.
                plt.close()

def Histograms(FileNum):
    """
    This function create a bar chart for every every files in the directory and illustrates number
    of noisy pixels according to file number.
    """
    
    global Pmatrix

    count_list = []
    for c0 in range(FileNum):
        counter = 0
        for c1 in range(nrows):
            for c2 in range(ncols):
                if Pmatrix[c1, c2, c0] != 0:
                    counter += 1
        count_list.append(counter)

    plt.figure(figsize = (10, 8))
    plt.bar(range(FileNum), count_list, facecolor='g', alpha=0.75)
    plt.title("Threshold vs Noisy Pixel Num")
    plt.xlabel("File Num")
    plt.ylabel("Number Of Pixels")
    plt.grid(True)
    plt.show()                                                                                     # This function only shows the bar chart, does not save it. It is possible to save it via toolbar.
                    
def Configuration(FilePath, fileNum, fileNumCount):
    """
    This function manipulates the raw data with calling functions above.
    """

    global Pmatrix
    DATA              = ReadFile(FilePath)
    CleanedData       = CleanData(DATA)
    FillMatrix(CleanedData, fileNumCount)

if __name__ == "__main__":

    path = "C:\\Users\\uenalard\\Desktop\\LocalCodes\\DATA\\2022-08-01_24bit_VThreshold_scan"
    os.chdir(path)                                                                             # Changes to path internally according to given path above

    subFolder = path + "\\PixPlots"                                                            # It is a new folder name for Windows. '/' should be used in a Linux OS.

    try:                        
        os.mkdir(subFolder)                                                                    # It creates a subfolder named above.
    except OSError:
        print ("Creation of the directory %s failed" % subFolder)
    else:
        print ("Successfully created the directory %s " % subFolder)

    file_num = len([name for name in os.listdir() if name.endswith('.bin')])                   # Number of the files which ends with '.bin'

    nrows, ncols = 512, 448                                                                      
    Pmatrix = np.zeros((nrows, ncols, file_num))               

    file_num_counter = 0                                                                       

    for file in os.listdir():
        if file.endswith('.bin'):
            file_path =f"{path}\\{file}"
            Configuration(file_path, file_num, file_num_counter)
            file_num_counter += 1 

    # PlotPixels(Pmatrix, file_num, subFolder)                                                  # It plots number of count values versus threshold value.
    Histograms(file_num)                                                                        # It plots a histogram like bar chart to illustrate evaluation of pixel noise according to threshold values