"""
Created on Fri July 29 09:10:10 2022

@author: uenalard

This script can be used to plot 2 images for every 24 bit raw data in the given path. 
Images are automatically saved into subfolder.
"""
import numpy as np
import eventdecode
import matplotlib.pyplot as plt
import matplotlib.image as img
import os


def ReadFile(PATH):
    """
    It reads data from a directory with given path, decodes the data and it returns list of decoded data.
    """
    data = np.load(PATH)
    frame_24bits_decoded = eventdecode.processevents(np.array(data), PC24bit  = True)   

    return frame_24bits_decoded

def CleanData(DATA):
    """
    It cleans data if there is any other types and remove class types of the data.
    """
    cleandData = []

    for item in DATA:
        if str(item[0]) == "PacketType.PC24bitData":
            cleandData.append(item)

    data = [item[1::] for item in cleandData] 

    return data

def CreateImageWithZeros(DATA):
    """
    In this function, image matrix consists of only pixels which send out zero values.
    """
    nrows, ncols = 512, 448                                                                      
    image = np.zeros((nrows, ncols))

    for item in DATA:
        if item[2] == 0:
            image[item[1], item[0]] += 1

    return image    

def CreateImageWithCountValues(DATA):
    """
    In this function, image consists of only pixels which send out total count values.
    """
    nrows, ncols = 512, 448                                                                     
    image = np.zeros((nrows, ncols)) 

    for item in DATA:
        if item[2] != 0.0:
            image[item[1], item[0]] += item[2]

    
    for c1 in range(nrows):
        for c2 in range(ncols):
            if image[c1, c2] != 0:
                image[c1, c2] = np.log10(image[c1, c2])

    return image  

def SaveImages(ImageMatrix, PlotPath, FileName, Check):
    """
    In this function, created image will be saved.
    """
    if Check == 1:
        figName = PlotPath + '\\' + FileName[0:-4] + "_Count" + ".png"
        figTitle = FileName[0:-4] + " Count"
    else:
        figName = PlotPath + '\\' + FileName[0:-4] + "_Zeros" + ".png"
        figTitle = FileName[0:-4] + " Zeros"

    values = []
    for y in range(512):
        for x in range(448):
            values.append(ImageMatrix[y, x])

    fig = plt.figure(figsize = (10, 8))                                                                         
    plt.title(figTitle) 
    plt.imshow(ImageMatrix, cmap = 'viridis', vmin = min(values), vmax = max(values))                                                                                 
    cax = plt.axes([0.9, 0.1, 0.060, 0.8])
    plt.colorbar(cax = cax)                                                              
    plt.savefig(figName)
    plt.clf()
    plt.close()

def Configuration(FilePath):

    DATA              = ReadFile(FilePath)
    CleanedData       = CleanData(DATA)
    ImageWithZeros    = CreateImageWithZeros(CleanedData)
    ImageWithoutZeros = CreateImageWithCountValues(CleanedData)

    PATH, FileName = os.path.split(FilePath) 
    subFolder = PATH + "\\IMAGES"

    SaveImages(ImageWithoutZeros, subFolder, FileName, 1)
    SaveImages(ImageWithZeros, subFolder, FileName, 0)

if __name__ == "__main__":

    path = "C:\\Users\\uenalard\\Desktop\\LocalCodes\\DATA\\24bitMaskData"
    os.chdir(path)

    subFolder = path + "\\IMAGES"
    
    try:                        
        os.mkdir(subFolder)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s " % path)

    for file in os.listdir():
        if file.endswith('.bin'):
            file_path =f"{path}\\{file}"
            Configuration(file_path)    