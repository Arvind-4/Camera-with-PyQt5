from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

import sys
import time 
import os
import pathlib

class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		
		self.availableCameras = QCameraInfo.availableCameras()
		if not self.availableCameras:
			exit(0)
		self.status = QStatusBar()
		self.setStatusBar(self.status)

		self.savePath = ''
		self.viewFinder = QCameraViewfinder()
		self.setCentralWidget(self.viewFinder)
		self.selectCamera(0)

		toolBar = QToolBar('Camera Tool Bar')
		toolBar.setIconSize(QSize(40,40))
		self.addToolBar(toolBar)

		clickAction = QAction(QIcon('Images/Capture.png'), 'Click Photo', self)
		clickAction.setStatusTip('This will Capture Pictures')
		clickAction.setToolTip('Capture Pictures')
		clickAction.triggered.connect(self.clickPhoto)
		toolBar.addAction(clickAction)

		changeFolderAction = QAction(QIcon('Images/Save.png'),'Set Save Location', self)
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
		self.capture.error.connect(lambda d,i:
								   self.status.showMessage(
								   	f'Image Captured {str(self.saveSeq)}'))
		self.currentCameraName = self.availableCameras[i].description()
		self.saveSeq = 0

	def clickPhoto(self):
		timeStamp = time.strftime('Date %d %b %Y Time %H %M %S')
		fileName = f'Webcam {self.currentCameraName} {timeStamp} .jpg'
		self.capture.capture(os.path.join(self.savePath, fileName))		
		self.saveSeq += 1

	def changeFolderName(self):
		path = QFileDialog.getExistingDirectory(self, "Picture Location", "")
		folderName = 'Pictures'
		mode = 0o666
		path = os.path.join(path, folderName)
		if not os.path.exists(folderName):
			os.mkdir(path, mode)
		if path:
			self.savePath = path 
			self.saveSeq = 0

	def alert(self, msg):
		error = QErrorMessage(self)
		error.showMessage(msg)

def main():
	App = QApplication(sys.argv)
	App.setStyle('Fusion')
	window = MainWindow()
	window.setWindowTitle('Camera --by Arvind')
	window.setWindowIcon(QIcon('Images/Logo.png'))
	window.resize(1100,700)
	window.show()
	sys.exit(App.exec_())

if __name__ == '__main__':
	main()