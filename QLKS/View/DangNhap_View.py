from PyQt6 import QtCore, QtGui, QtWidgets


class DangNhap(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 403)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.btn_Thoat = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_Thoat.setGeometry(QtCore.QRect(250, 240, 121, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btn_Thoat.setFont(font)
        self.btn_Thoat.setObjectName("btn_Thoat")

        self.btn_DangNhap = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_DangNhap.setGeometry(QtCore.QRect(470, 240, 121, 51))
        self.btn_DangNhap.setFont(font)
        self.btn_DangNhap.setObjectName("btn_DangNhap")

        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 80, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(110, 160, 131, 31))
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.lineEdit_Username = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_Username.setGeometry(QtCore.QRect(250, 80, 361, 31))
        self.lineEdit_Username.setObjectName("lineEdit_Username")

        self.lineEdit_pass = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_pass.setGeometry(QtCore.QRect(250, 160, 361, 31))
        self.lineEdit_pass.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_pass.setObjectName("lineEdit_pass")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Đăng Nhập"))
        self.btn_Thoat.setText(_translate("MainWindow", "Thoát"))
        self.btn_DangNhap.setText(_translate("MainWindow", "Đăng Nhập"))
        self.label.setText(_translate("MainWindow", "Tên Đăng Nhập:"))
        self.label_2.setText(_translate("MainWindow", "Mật Khẩu:"))
