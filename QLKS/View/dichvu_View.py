from PyQt6 import QtCore, QtGui, QtWidgets

class DichVuApp(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        MainWindow.setWindowTitle("Quản Lý Dịch Vụ")

        # Central widget
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Main Layout
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)

        # Group: Thông tin khách hàng
        self.group_khach_hang = QtWidgets.QGroupBox("Thông Tin Khách Hàng", parent=self.centralwidget)
        self.group_khach_hang.setFont(QtGui.QFont("Arial", 12))
        self.kh_layout = QtWidgets.QGridLayout(self.group_khach_hang)

        self.label_tenkh = QtWidgets.QLabel("Tên Khách Hàng:", parent=self.group_khach_hang)
        self.combb_tenkh_dv = QtWidgets.QComboBox(parent=self.group_khach_hang)
        self.label_makh = QtWidgets.QLabel("Mã Khách Hàng:", parent=self.group_khach_hang)
        self.MaKH_DV = QtWidgets.QLineEdit(parent=self.group_khach_hang)
        self.MaKH_DV.setFixedHeight(30)

        self.kh_layout.addWidget(self.label_tenkh, 0, 0)
        self.kh_layout.addWidget(self.combb_tenkh_dv, 0, 1)
        self.kh_layout.addWidget(self.label_makh, 1, 0)
        self.kh_layout.addWidget(self.MaKH_DV, 1, 1)

        # Group: Thông tin dịch vụ
        self.group_dich_vu = QtWidgets.QGroupBox("Thông Tin Dịch Vụ", parent=self.centralwidget)
        self.group_dich_vu.setFont(QtGui.QFont("Arial", 12))
        self.dv_layout = QtWidgets.QGridLayout(self.group_dich_vu)

        self.label_madv = QtWidgets.QLabel("Mã Dịch Vụ:", parent=self.group_dich_vu)
        self.combb_madv = QtWidgets.QComboBox(parent=self.group_dich_vu)
        self.label_gia = QtWidgets.QLabel("Giá:", parent=self.group_dich_vu)
        self.textEdit_gia = QtWidgets.QLineEdit(parent=self.group_dich_vu)
        self.textEdit_gia.setFixedHeight(30)
        self.label_soluong = QtWidgets.QLabel("Số Lượng:", parent=self.group_dich_vu)
        self.textEdit_SOL = QtWidgets.QLineEdit(parent=self.group_dich_vu)
        self.textEdit_SOL.setFixedHeight(30)

        # Add a new input field for the name of the new service
        self.label_tendv = QtWidgets.QLabel("Tên Dịch Vụ Mới:", parent=self.group_dich_vu)
        self.textEdit_tendv = QtWidgets.QLineEdit(parent=self.group_dich_vu)
        self.textEdit_tendv.setFixedHeight(30)

        self.dv_layout.addWidget(self.label_madv, 0, 0)
        self.dv_layout.addWidget(self.combb_madv, 0, 1)
        self.dv_layout.addWidget(self.label_gia, 1, 0)
        self.dv_layout.addWidget(self.textEdit_gia, 1, 1)
        self.dv_layout.addWidget(self.label_soluong, 2, 0)
        self.dv_layout.addWidget(self.textEdit_SOL, 2, 1)
        self.dv_layout.addWidget(self.label_tendv, 3, 0)
        self.dv_layout.addWidget(self.textEdit_tendv, 3, 1)

        # Table: Danh sách dịch vụ
        self.tableWidget_DV = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableWidget_DV.setColumnCount(2)
        self.tableWidget_DV.setHorizontalHeaderLabels(["Tên Dịch Vụ", "Số Lượng"])
        self.tableWidget_DV.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableWidget_DV.setFont(QtGui.QFont("Arial", 10))
        self.tableWidget_DV.setFixedHeight(200)

        # Group: Chức năng
        self.group_buttons = QtWidgets.QGroupBox("Chức Năng", parent=self.centralwidget)
        self.group_buttons.setFont(QtGui.QFont("Arial", 12))
        self.button_layout = QtWidgets.QHBoxLayout(self.group_buttons)

        self.btn_Them_DV = QtWidgets.QPushButton("Thêm", parent=self.group_buttons)
        self.btn_Sua_DV = QtWidgets.QPushButton("Sửa", parent=self.group_buttons)
        self.btn_Xoa_DV = QtWidgets.QPushButton("Xóa", parent=self.group_buttons)
        self.btn_Huy = QtWidgets.QPushButton("Hủy", parent=self.group_buttons)
        self.btn_dongy = QtWidgets.QPushButton("Đồng Ý", parent=self.group_buttons)

        self.button_layout.addWidget(self.btn_Them_DV)
        self.button_layout.addWidget(self.btn_Sua_DV)
        self.button_layout.addWidget(self.btn_Xoa_DV)
        self.button_layout.addWidget(self.btn_Huy)
        self.button_layout.addWidget(self.btn_dongy)

        # Add widgets to main layout
        self.main_layout.addWidget(self.group_khach_hang)
        self.main_layout.addWidget(self.group_dich_vu)
        self.main_layout.addWidget(self.tableWidget_DV)
        self.main_layout.addWidget(self.group_buttons)

        MainWindow.setCentralWidget(self.centralwidget)

# Main Application
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = DichVuApp()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
