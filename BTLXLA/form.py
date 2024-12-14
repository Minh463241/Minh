from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Video display label
        self.labelVideo = QtWidgets.QLabel(self.centralwidget)
        self.labelVideo.setGeometry(QtCore.QRect(50, 50, 700, 400))
        self.labelVideo.setFrameShape(QtWidgets.QFrame.Box)
        self.labelVideo.setText("")
        self.labelVideo.setObjectName("labelVideo")

        # Open video button
        self.btnOpenVideo = QtWidgets.QPushButton(self.centralwidget)
        self.btnOpenVideo.setGeometry(QtCore.QRect(50, 470, 200, 40))
        self.btnOpenVideo.setObjectName("btnOpenVideo")

        # Start tracking button
        self.btnStartTracking = QtWidgets.QPushButton(self.centralwidget)
        self.btnStartTracking.setGeometry(QtCore.QRect(300, 470, 200, 40))
        self.btnStartTracking.setObjectName("btnStartTracking")

        # Start camera button
        self.btnStartCamera = QtWidgets.QPushButton(self.centralwidget)
        self.btnStartCamera.setGeometry(QtCore.QRect(50, 520, 200, 40))
        self.btnStartCamera.setObjectName("btnStartCamera")

        # Stop camera button
        self.btnStopCamera = QtWidgets.QPushButton(self.centralwidget)
        self.btnStopCamera.setGeometry(QtCore.QRect(300, 520, 200, 40))
        self.btnStopCamera.setObjectName("btnStopCamera")

        # Exit button
        self.btnExit = QtWidgets.QPushButton(self.centralwidget)
        self.btnExit.setGeometry(QtCore.QRect(550, 520, 200, 40))
        self.btnExit.setObjectName("btnExit")

        # Status label
        self.labelStatus = QtWidgets.QLabel(self.centralwidget)
        self.labelStatus.setGeometry(QtCore.QRect(50, 570, 700, 40))
        self.labelStatus.setFrameShape(QtWidgets.QFrame.Box)
        self.labelStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.labelStatus.setObjectName("labelStatus")

        # Accuracy label (new label for displaying accuracy)
        self.labelAccuracy = QtWidgets.QLabel(self.centralwidget)
        self.labelAccuracy.setGeometry(QtCore.QRect(50, 610, 700, 40))
        self.labelAccuracy.setFrameShape(QtWidgets.QFrame.Box)
        self.labelAccuracy.setAlignment(QtCore.Qt.AlignCenter)
        self.labelAccuracy.setObjectName("labelAccuracy")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "YOLO Object Tracker"))
        self.btnOpenVideo.setText(_translate("MainWindow", "Open Video"))
        self.btnStartTracking.setText(_translate("MainWindow", "Start Tracking"))
        self.btnStartCamera.setText(_translate("MainWindow", "Start Camera"))
        self.btnStopCamera.setText(_translate("MainWindow", "Stop Camera"))
        self.btnExit.setText(_translate("MainWindow", "Exit"))
        self.labelStatus.setText(_translate("MainWindow", "Status: Ready"))
        self.labelAccuracy.setText(_translate("MainWindow", "Accuracy: Not Detected"))
