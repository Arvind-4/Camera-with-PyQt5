from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

import sys
import time
import pathlib

BASE_DIR = pathlib.Path().home()
FOLDER_NAME = 'Images'

SAVE_PATH = BASE_DIR / FOLDER_NAME
SAVE_PATH.mkdir(exist_ok=True, parents=True)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.availableCameras = QCameraInfo.availableCameras()
        if not self.availableCameras:
            exit(0)
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.savePath = None
        self.viewFinder = QCameraViewfinder()
        self.setCentralWidget(self.viewFinder)
        self.selectCamera(0)

        toolBar = QToolBar('Camera Tool Bar')
        toolBar.setIconSize(QSize(40, 40))
        self.addToolBar(toolBar)

        clickAction = QAction(QIcon('Images/Capture.png'), 'Click Photo', self)
        clickAction.setStatusTip('This will Capture Pictures')
        clickAction.setToolTip('Capture Pictures')
        clickAction.triggered.connect(self.clickPhoto)
        toolBar.addAction(clickAction)

        changeFolderAction = QAction(QIcon('Images/Save.png'), 'Set Save Location', self)
        changeFolderAction.setStatusTip('This will Change the Save Location')
        changeFolderAction.setToolTip('Change Save Location')
        changeFolderAction.triggered.connect(self.changeFolderName)
        toolBar.addAction(changeFolderAction)

        cameraSelector = QComboBox()
        cameraSelector.setToolTip('Select Camera')
        cameraSelector.setStatusTip('Choose Camera to take Pictures')
        cameraSelector.setToolTipDuration(2500)
        cameraSelector.addItems([camera.description()
                                 for camera in self.availableCameras])
        toolBar.addWidget(cameraSelector)

    def selectCamera(self, i):
        self.camera = QCamera(self.availableCameras[i])
        self.camera.setViewfinder(self.viewFinder)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        self.camera.error.connect(lambda:
                                  self.alert(self.camera.errorString()))
        self.camera.start()
        self.capture = QCameraImageCapture(self.camera)
        self.capture.error.connect(lambda d, i:
                                   self.status.showMessage(
                                       f'Image Captured {str(self.saveSeq)}'))
        self.currentCameraName = self.availableCameras[i].description()
        self.saveSeq = 0

    def clickPhoto(self):
        timeStamp = time.strftime('Date %d %b %Y Time %H %M %S')
        fileName = f'Webcam {self.currentCameraName} {timeStamp} .jpg'
        if self.savePath:
            savePath = self.savePath / fileName
        else:
            savePath = SAVE_PATH / fileName
        self.saveImage(str(savePath))
        print('Image saved on ', str(savePath))
        self.saveSeq += 1

    def changeFolderName(self):
        path = QFileDialog.getExistingDirectory(self, "Picture Location", "")
        mode = 0o666
        path = pathlib.Path(path)
        self.savePath = path
        self.savePath.mkdir(exist_ok=True, parents=True, mode=mode)

    def saveImage(self, savePath:str):
        self.capture.capture(savePath)

    def alert(self, msg):
        error = QErrorMessage(self)
        error.showMessage(msg)


def main():
    App = QApplication(sys.argv)
    App.setStyle('Fusion')
    window = MainWindow()
    window.setWindowTitle('Camera --by Arvind')
    window.setWindowIcon(QIcon('Images/Logo.png'))
    window.resize(1100, 700)
    window.show()
    sys.exit(App.exec())


if __name__ == '__main__':
    main()
