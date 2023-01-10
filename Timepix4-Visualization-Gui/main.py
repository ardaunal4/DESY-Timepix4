from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPoint, QRect, QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont
import qdarkstyle
import sys, os, platform
import numpy as np 
from time import sleep
from processClassEvent import *
from processClassFrame import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import warnings
warnings.filterwarnings("ignore")

class TabBar(QTabBar):

    def tabSizeHint(self, index):

        s = QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s

    def paintEvent(self, event):

        painter = QStylePainter(self)
        opt = QStyleOptionTab()

        for i in range(self.count()):

            self.initStyleOption(opt, i)
            painter.drawControl(QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QRect(QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QStyle.CE_TabBarTabLabel, opt)
            painter.restore()

class TabWidget(QTabWidget):

    def __init__(self, *args, **kwargs):

        QTabWidget.__init__(self, *args, **kwargs)
        self.setTabBar(TabBar(self))
        self.setTabPosition(QTabWidget.West)

class Window(QMainWindow): 

    def __init__(self):

        super().__init__()
        self.setGeometry(50, 50, 900, 600) 
        self.setWindowTitle("Timepix4 Visualization")
        self.setWindowIcon(QIcon('DesyLogo.png'))
        self.UI()
        self.variables()
        self.show()

    def variables(self):

        self.PATH  = ""
        self.PATH2 = ""
        self.fileList = []
        self.threadPtr = 0
        self.videoPtr = 0
        self.tabPtr = 0

    def UI(self):

        self.mainLayout()
        self.WelcomeLayout()
        self.setCentralWidget(self.mainWidget)
        self.tabWidget1()
        self.tabWidget2()
        self.widgets()
        self.layoutEVENT()
        self.layoutFRAME()
        self.handleButtonRemove()

    def tabWidget1(self):

        self.tab1 = QWidget()
        self.tabs.addTab(self.tab1, "Event Mode")
    
    def tabWidget2(self):

        self.tab2 = QWidget()
        self.tabs.addTab(self.tab2, "Frame Mode")

    def widgets(self):

        """
        *******************************************************************************************
        TAB1 Widgets
        """

        self.EventImFigure()
        self.EventVidFigure()

        self.playBtn = QPushButton()
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.setEnabled(False)
        self.playBtn.clicked.connect(self.playVideo)

        self.videoSlider = QSlider(Qt.Horizontal)
        self.videoSlider.setEnabled(False)
        self.videoSlider.setRange(0,0)

        self.plot_qlabel = QLabel("Show Image")
        self.plot_button = QPushButton("Show Image", self)
        self.plot_button.setEnabled(False)
        self.plot_button.clicked.connect(self.showIm)

        self.eventModeCBLabel = QLabel("Visualization Mode")
        self.eventModeCB      = QComboBox(self)
        self.eventModeCB.addItem("ToA mode")
        self.eventModeCB.addItem("ToT mode")
        self.eventModeCB.adjustSize()
        self.selectionEventCombobox()
        
        self.imSlider = QSlider(Qt.Vertical, self)
        self.imSlider.setEnabled(False)
        self.imSlider.valueChanged[int].connect(self.updateIm)
        self.imSlider.setValue(0)

        self.choosePathLabel = QLabel("Choose Folder")
        self.choosePath = QPushButton("", self)
        self.choosePath.clicked.connect(self.ChooseFile)
        self.choosePath.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))

        img = mpimg.imread('DesyLogo.png')
        self.axImage.imshow(img)

        timepixIm = mpimg.imread('Timepix4.jpg')
        self.axVideo.imshow(timepixIm)

        """
        *******************************************************************************************
        TAB2 Widgets
        """
        self.FrameImFigure()
        self.axFrameImage.imshow(img)

        self.choosePathLabeltab2 = QLabel("Choose Folder")
        self.choosePathtab2      = QPushButton("", self)
        self.choosePathtab2.clicked.connect(self.ChooseFiletab2)
        self.choosePathtab2.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))

        self.startProcessLabel  = QLabel("Start")
        self.startProcessButton = QPushButton("", self)
        self.startProcessButton.clicked.connect(self.StartAnalysis)
        self.startProcessButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        self.frameModeCBLabel = QLabel("Readout Mode")
        self.frameModeCB      = QComboBox(self)
        self.frameModeCB.addItem("24-bit mode")
        self.frameModeCB.addItem("8-bit mode")
        self.frameModeCB.addItem("16-bit mode")
        self.frameModeCB.adjustSize()
        
        self.frameModeCB.setFixedSize(200, 100)
        self.frameModeCB.currentIndexChanged.connect(self.selectionCombobox)

        self.listwidget = QListWidget()
        self.listwidget.itemActivated.connect(self.listClick)

        self.pbar = QProgressBar(self)
        self.pbarVal = 0
        self.pbar.setValue(self.pbarVal)

        self.saveImagesLabel  = QLabel("Save Images")
        self.saveImagesButton = QPushButton("", self)
        self.saveImagesButton.clicked.connect(self.saveImages)
        self.saveImagesButton.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))

    """
    *******************************************************************************************
    Main Menu Pushbutton Functions
    """

    def menuAnim(self):

        self.tabPtr += 1
        if self.tabPtr %2 == 0:
            self.handleButtonRemove()
        else:
            self.handleButtonRestore()

    def handleButtonRemove(self):

        self.tabs.setParent(None)
        self.main_layout.addWidget(self.imLabel)
        self.main_layout.addWidget(self.entLabel)
        self.main_layout.addWidget(self.entLabel2)
        self.main_layout.addWidget(self.freeLabel)
        self.main_layout.addWidget(self.freeLabel2)
        self.main_layout.addWidget(self.freeLabel3)
        self.main_layout.addWidget(self.designlabel2)
        self.main_layout.addWidget(self.designlabel)

    def handleButtonRestore(self):

        self.main_layout.addWidget(self.tabs)
        self.imLabel.setParent(None)
        self.entLabel.setParent(None)
        self.entLabel2.setParent(None)
        self.freeLabel.setParent(None)
        self.freeLabel2.setParent(None)
        self.freeLabel3.setParent(None)
        self.designlabel2.setParent(None)
        self.designlabel.setParent(None)

    """
    *******************************************************************************************
    TAB1  Funcions
    """

    def EventImFigure(self):

        self.imFig    = plt.figure()
        self.imFig.patch.set_facecolor('lightcyan')
        self.imCanvas = FigureCanvas(self.imFig)
        self.toolbar  = NavigationToolbar(self.imCanvas, self)
        self.axImage  = self.imFig.add_subplot(111)

    def showIm(self):
        
        self.selectionEventCombobox()
        if self.comboboxEventVar == "ToA mode":
            self.Configuration(self.PATH)
            self.imFig.clf()
            self.axImage = self.imFig.add_subplot(111)
            self.axImgVar = self.axImage.imshow(self.image0, cmap = "viridis")
            self.imFig.colorbar(self.axImgVar, ax = self.axImage, location = 'right', 
                                anchor=(0, 0.3), shrink=0.7)
            self.imCanvas.draw()
            self.imFig.canvas.flush_events()
        else:
            self.Configuration(self.PATH)
            self.imFig.clf()
            self.axImage = self.imFig.add_subplot(111)
            self.axImgVar = self.axImage.imshow(self.totImage, cmap = "viridis")
            self.imFig.colorbar(self.axImgVar, ax = self.axImage, location = 'right', 
                                anchor=(0, 0.3), shrink=0.7)
            self.imCanvas.draw()
            self.imFig.canvas.flush_events()

    def selectionEventCombobox(self):
        self.comboboxEventVar = self.eventModeCB.currentText()
    
    @jit
    def updateIm(self):

        sliderVal = self.imSlider.value()
        self.image = CreateImage(self.eventList[sliderVal])
        self.axImgVar.set_data(self.image)
        self.imCanvas.draw()
        self.imFig.canvas.flush_events()

    def EventVidFigure(self):

        self.vidFig = plt.figure(figsize=(15, 15))
        self.vidFig.patch.set_facecolor('lightcyan')
        self.vidCanvas = FigureCanvas(self.vidFig)
        self.axVideo = self.vidFig.add_subplot(111)
        self.axVideo.axis("off")
        
    def initVideo(self):

        self.vidFig.clf()
        self.axVideo = self.vidFig.add_subplot(111)
        self.axVideo.axis("off")
        self.axVideoVar = self.axVideo.imshow(self.image0, cmap = "viridis", interpolation='none')
        self.vidCanvas.draw()
        self.vidCanvas.flush_events()

    def animate(self, i):

        if self.threadPtr %2 == 1:
            self.videoSlider.setValue(i)
            curIm = CreateImage(self.eventList[i])
            self.axVideoVar.set_data(curIm)
            self.vidCanvas.draw()
            self.vidFig.canvas.flush_events()
        else:
            self.videoPtr = i
            return -1

    def playVideo(self):

        if self.threadPtr == 0:
            self.initVideo()

        self.threadPtr += 1
        if self.threadPtr==1:
            for counter in range(len(self.eventList)-1):
                self.animate(counter)
        else:
            for counter in range(len(self.eventList)-1-self.videoPtr):
                currentVar = counter+self.videoPtr
                self.animate(currentVar)

    def Configuration(self, Path):

        try:
            DATA           = readFile(Path)
        except:
            QMessageBox.information(self, "WARNING!", "INVALID Directory!")
            return -1

        if self.comboboxEventVar == "ToA mode":
            CleanedData    = cleanData(DATA)
            self.eventList = eventList(CleanedData)
            self.image0 = CreateImage(self.eventList[0])
            QMessageBox.information(self, "SUCCESS!", "File is successfully uploaded!")
            
            self.imSlider.setEnabled(True)
            self.playBtn.setEnabled(True)
            self.playBtn.setStyleSheet("background-color: gray")
            self.videoSlider.setEnabled(True)
            self.imSlider.setMinimum(0)
            self.imSlider.setMaximum(len(self.eventList)-1)
            self.videoSlider.setRange(0, len(self.eventList)-1)
            self.threadPtr = 0
        else:
            ToTCleanedData = totImageConf(DATA)
            self.totImage = CreateImage(ToTCleanedData)
            
    def ChooseFile(self):

        self.PATH, _ = QFileDialog.getOpenFileName(self, 'Open Bin File', r"<Default dir>", "Bin files (*.bin)")
        self.plot_button.setEnabled(True)

    """
    *******************************************************************************************
    Main Menu Layout Functions
    """

    def mainLayout(self):

        self.main_layout = QVBoxLayout()
        self.tabs = TabWidget()
        self.menuButton = QPushButton()
        self.menuButton.setIcon(self.style().standardIcon(QStyle.SP_FileDialogListView))
        self.menuButton.clicked.connect(self.menuAnim)
        self.menuButton.setFixedSize(QSize(50, 20))
        self.main_layout.addWidget(self.menuButton)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.tabs)
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.main_layout)

    def WelcomeLayout(self):

        self.welcomeVLayout = QVBoxLayout()
        self.pixmap = QPixmap('DesyLogo.png')
        self.newpixmap = self.pixmap.scaled(300, 300, Qt.KeepAspectRatio)
        self.imLabel = QLabel(self)
        self.imLabel.setPixmap(self.newpixmap)
        self.imLabel.setAlignment(Qt.AlignCenter)

        self.freeLabel = QLabel("                           ")
        self.freeLabel.setGeometry(250, 500, 100, 100)
        self.freeLabel.setFont(QFont('Times', 50, QFont.Bold))
        self.freeLabel2 = QLabel("                           ")
        self.freeLabel2.setGeometry(250, 600, 100, 100)
        self.freeLabel2.setFont(QFont('Times', 50, QFont.Bold))
        self.freeLabel3 = QLabel("                           ")
        self.freeLabel3.setGeometry(250, 700, 100, 100)
        self.freeLabel3.setFont(QFont('Times', 50, QFont.Bold))

        self.designlabel = QLabel("designed by Arda Unal")
        self.designlabel.setAlignment(Qt.AlignCenter)
        self.designlabel.setFont(QFont('Times', 20, italic=True))
        self.designlabel.setStyleSheet("color: black")

        self.designlabel2 = QLabel("2022 Summer Student Program")
        self.designlabel2.setAlignment(Qt.AlignCenter)
        self.designlabel2.setFont(QFont('Times', 20, italic=True))
        self.designlabel2.setStyleSheet("color: black")

        self.entLabel = QLabel("WELCOME")
        self.entLabel.setFont(QFont('Times', 50, QFont.Bold))
        self.entLabel.setStyleSheet("color: darkCyan")
        self.entLabel.setAlignment(Qt.AlignCenter)
        self.entLabel2 = QLabel("VISUALIZATION GUI FOR TIMEPIX4")
        self.entLabel2.setFont(QFont('Times', 50, QFont.Bold))
        self.entLabel2.setStyleSheet("color: darkCyan")
        self.entLabel2.setAlignment(Qt.AlignCenter)

    """
    *******************************************************************************************
    Event Tab Layout Function
    """

    def layoutEVENT(self):

        self.tab1mainLayout = QHBoxLayout()
        self.tab1leftLayout = QFormLayout()
        self.tab1rightLayout = QFormLayout()
        self.tab1leftHbox1 = QHBoxLayout()
        self.tab1plotVBox = QVBoxLayout()
        self.tab1plotHBox = QHBoxLayout()
        self.tab1videoHBox = QHBoxLayout()
        self.tab1videoVBox = QVBoxLayout()
        
        # Leftab1t Layout
        self.tab1leftlayoutGroupBox = QGroupBox("") 
        self.tab1plotVBox.addWidget(self.toolbar)
        self.tab1plotVBox.addWidget(self.imCanvas)
        self.tab1plotHBox.addLayout(self.tab1plotVBox) 

        self.tab1plotHBox.addWidget(self.imSlider)
        self.tab1leftLayout.addRow(self.tab1plotHBox)
        
        self.tab1leftHbox1.addWidget(self.choosePathLabel)
        self.tab1leftHbox1.addWidget(self.choosePath)
        self.tab1leftHbox1.addStretch()
        self.tab1leftHbox1.addWidget(self.eventModeCBLabel)
        self.tab1leftHbox1.addWidget(self.eventModeCB)

        self.tab1leftHbox1.addStretch()
        self.tab1leftHbox1.addWidget(self.plot_qlabel)
        self.tab1leftHbox1.addWidget(self.plot_button)
        self.tab1leftLayout.addRow(self.tab1leftHbox1)
        self.tab1leftlayoutGroupBox.setLayout(self.tab1leftLayout)

        self.tab1rightlayoutGroupBox = QGroupBox("VIDEO")
        self.tab1rightlayoutGroupBox.setStyleSheet("background-color:black;")
        self.tab1videoVBox.addWidget(self.vidCanvas) 
        self.tab1videoHBox.addWidget(self.playBtn)
        self.tab1videoHBox.addWidget(self.videoSlider)
        self.tab1videoVBox.addLayout(self.tab1videoHBox) 
        self.tab1rightLayout.addRow(self.tab1videoVBox)  
        self.tab1rightlayoutGroupBox.setLayout(self.tab1rightLayout)
        
        self.tab1mainLayout.addWidget(self.tab1leftlayoutGroupBox, 50)
        self.tab1mainLayout.addWidget(self.tab1rightlayoutGroupBox, 50)
        self.tab1.setLayout(self.tab1mainLayout)

    """
    *******************************************************************************************
    TAB2  Funcions
    """
    def FrameImFigure(self):

        self.frameFig = plt.figure(figsize=(12, 10))
        self.frameFig.patch.set_facecolor('lightcyan')
        self.frameCanvas = FigureCanvas(self.frameFig)
        self.toolbarFrame = NavigationToolbar(self.frameCanvas, self)
        self.axFrameImage = self.frameFig.add_subplot(111)
        
    def ChooseFiletab2(self):

        try:
            self.PATH2 = QFileDialog.getExistingDirectory(self)
        except:
            QMessageBox.information(self, "WARNING!", "INVALID Directory!")
            return -1

    def selectionCombobox(self):
        self.comboboxVar = self.frameModeCB.currentText()
    
    def listClick(self, item):

        if self.pbar.value() == 100:
            if platform.system() == "Windows":
                filename = str(item.text())
                for char in filename:
                    if char == "/":
                        char = "\\"
                print(filename)
            elif platform.system() == "Linux" or platform.system() == "Darwin":
                filename = str(item.text())
                for char in filename:
                    if char == "\\":
                        char = "/"
            else:
                QMessageBox.information(self, "WARNING!", "UNKNOWN OS!")
            self.conf24bit(filename)
        else:
            QMessageBox.information(self, "WARNING!", "Process is not completed!")
            return -1

    def saveImages(self):
        
        if self.pbar.value() == 100:
            if platform.system() == "Windows":
                for item in self.fileList:
                    for char in item:
                        if char == "/":
                            char = "\\"
                    self.saveImsConfig(item)
            elif platform.system() == "Linux" or platform.system() == "Darwin":
                for item in self.fileList:
                    for char in item:
                        if char == "\\":
                            char = "/"
                    self.saveImsConfig(item)
            else:
                QMessageBox.information(self, "WARNING!", "UNKNOWN OS!")
        else:
            QMessageBox.information(self, "WARNING!", "Save images process could not be completed!")
            return -1
        
        QMessageBox.information(self, "SUCCESS!", "Images are saved successfully!")

    def saveImsConfig(self, file_name):

        svImPath, FileName = os.path.split(file_name) 
        if platform.system() == "Windows":   
            subFolder = svImPath + "\\IMAGES"
            figName = subFolder + "\\" + FileName[0:-4] + ".png"
        elif platform.system() == "Linux" or platform.system() == "Darwin":   
            subFolder = svImPath + "/IMAGES"
            figName = subFolder + "/" + FileName[0:-4] + ".png"
        else:
            QMessageBox.information(self, "WARNING!", "UNKNOWN OS!")
        
        try:                        
            os.mkdir(subFolder)
        except OSError:
            pass

        try:
            data24bit = read24bitFrameFile(file_name)
        except:
            QMessageBox.information(self, "WARNING!", "INVALID Directory!")
            return -1
    
        cleaned24bitdata = Clean24bitData(data24bit)
        image24bit = CreateFrameImage(cleaned24bitdata)
        fig = plt.figure(figsize = (10, 8))                                                                         
        plt.imshow(image24bit, cmap = 'viridis')                                                                                 
        cax = plt.axes([0.9, 0.1, 0.060, 0.8])
        plt.colorbar(cax = cax)                                                              
        fig.savefig(figName)
        plt.close()

    def StartAnalysis(self):

        self.listwidget.clear()
        self.pbarVal = 0
        self.pbar.setValue(self.pbarVal)
        self.accessFiles()

    def configFrame(self, file_name):
        
        self.selectionCombobox()

        if self.comboboxVar == "24-bit mode":
            self.conf24bit(file_name)
        elif self.comboboxVar == "16-bit mode":
            self.conf816bit(file_name, "16-bit mode")
        else:
            self.conf816bit(file_name, "8-bit mode")
    
    def accessFiles(self):

        os.chdir(self.PATH2)
        self.numberOfFiles = len([name for name in os.listdir() if name.endswith('.bin')])

        if platform.system() == "Windows":
            for file in os.listdir():
                if file.endswith('.bin'):
                    file_path =f"{self.PATH2}/{file}"
                    print(file_path)
                    self.listwidget.addItem(file_path)
                    self.configFrame(file_path)
                    self.fileList.append(file_path)
                    
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            for file in os.listdir():
                if file.endswith('.bin'):
                    file_path =f"{self.PATH2}/{file}"
                    self.listwidget.addItem(file_path)
                    self.configFrame(file_path)
                    self.fileList.append(file_path)  
        else:
            QMessageBox.information(self, "FAIL!", "Unknown OS!")
            return -1

    def conf24bit(self, filename):

        try:
            data24bit = read24bitFrameFile(filename)
        except:
            QMessageBox.information(self, "WARNING!", "INVALID Directory!")
            return -1
    
        cleaned24bitdata = Clean24bitData(data24bit)
        image24bit = CreateFrameImage(cleaned24bitdata)
        self.configPlot(image24bit)
        self.pbarVal += 100/int(self.numberOfFiles)
        self.pbar.setValue(self.pbarVal)
        sleep(0.1)

    def configPlot(self, image):  

        self.frameFig.clf()
        self.axFrameImage = self.frameFig.add_subplot(111)
        framImageVar = self.axFrameImage.imshow(image, cmap = "viridis")
        self.frameFig.colorbar(framImageVar, ax = self.axFrameImage, location = 'right')
        self.frameCanvas.draw()
        self.frameFig.canvas.flush_events()

    def conf816bit(self, filename, readoutmode):
        
        print(filename)
        try:
            image816bit = read816bitFrameFile(filename, readoutmode)
            print(image816bit)
        except:
            QMessageBox.information(self, "WARNING!", "INVALID Directory!")
            return -1

        self.configPlot(image816bit)
        self.pbarVal += 100/int(self.numberOfFiles)
        self.pbar.setValue(self.pbarVal)
        sleep(1)

    """
    *******************************************************************************************
    Frame tab layout function
    """

    def layoutFRAME(self):

        self.tab2mainLayout   = QHBoxLayout()
        self.tab2leftLayout   = QFormLayout()
        self.tab2rightLayout  = QFormLayout()
        self.tab2leftHbox1    = QHBoxLayout()
        self.tab2plotVBox     = QVBoxLayout()
        self.tab2plotHBox     = QHBoxLayout()
        self.listVBox         = QVBoxLayout()
        self.tab2leftHbox2    = QHBoxLayout()

        self.tab2leftlayoutGroupBox = QGroupBox("") 
        self.tab2leftHbox1.addWidget(self.choosePathLabeltab2)
        self.tab2leftHbox1.addWidget(self.choosePathtab2)
        self.tab2leftHbox1.addStretch()
        self.tab2leftHbox1.addWidget(self.frameModeCBLabel)
        self.tab2leftHbox1.addWidget(self.frameModeCB)
        self.tab2leftHbox1.addStretch()
        self.tab2leftHbox1.addWidget(self.startProcessLabel)
        self.tab2leftHbox1.addWidget(self.startProcessButton)
        self.tab2leftLayout.addRow(self.tab2leftHbox1)
        self.listVBox.addWidget(self.listwidget)
        self.tab2leftLayout.addRow(self.listVBox)
        self.tab2leftHbox2.addWidget(self.pbar)
        self.tab2leftLayout.addRow(self.tab2leftHbox2)
        self.tab2leftlayoutGroupBox.setLayout(self.tab2leftLayout)

        self.tab2rightlayoutGroupBox = QGroupBox("")
        self.tab2plotVBox.addWidget(self.toolbarFrame) 
        self.tab2plotVBox.addWidget(self.frameCanvas)
        self.tab2rightLayout.addRow(self.tab2plotVBox)  
        self.tab2plotHBox.addWidget(self.saveImagesLabel)
        self.tab2plotHBox.addWidget(self.saveImagesButton)
        self.tab2plotHBox.addStretch()
        self.tab2rightLayout.addRow(self.tab2plotHBox) 
        self.tab2rightlayoutGroupBox.setLayout(self.tab2rightLayout)
        
        self.tab2mainLayout.addWidget(self.tab2leftlayoutGroupBox, 50)
        self.tab2mainLayout.addWidget(self.tab2rightlayoutGroupBox, 50)
        self.tab2.setLayout(self.tab2mainLayout)

class ProxyStyle(QProxyStyle):

    def drawControl(self, element, opt, painter, widget):
        
        if element == QStyle.CE_TabBarTabLabel:
            ic = self.pixelMetric(QStyle.PM_TabBarIconSize)
            r = QRect(opt.rect)
            w =  0 if opt.icon.isNull() else opt.rect.width() + self.pixelMetric(QStyle.PM_TabBarIconSize)
            r.setHeight(opt.fontMetrics.width(opt.text) + w)
            r.moveBottom(opt.rect.bottom())
            opt.rect = r
        QProxyStyle.drawControl(self, element, opt, painter, widget)

def main():

    QApplication.setColorSpec(QApplication.CustomColor)
    app = QApplication(sys.argv)
    app.setStyle(ProxyStyle())
    app.setStyleSheet(qdarkstyle.load_stylesheet()) 
    window = Window()
    sys.exit(app.exec_())

if __name__ == "__main__":

    main()