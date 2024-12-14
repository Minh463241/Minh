from PyQt6 import QtWidgets
from QLKS.View.ChagnePass_view import doipass  # Import lớp giao diện
from QLKS.models.admin import Admin  # Import lớp Admin

class changePass(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = doipass()  # Khởi tạo giao diện
        self.ui.setupUi(self)  # Thiết lập giao diện trên cửa sổ hiện tại
        self.ui.btn_XN.clicked.connect(self.change_password)  # Kết nối sự kiện
        self.ui.btn_Thoat_chagne.clicked.connect(self.close)

    def change_password(self):
        tendn = self.ui.lineEdit_Username_chagne.text()
        passcu = self.ui.lineEdit_pass_chagne.text()
        tendnmoi = self.ui.lineEdit_Username_new.text()
        passmoi = self.ui.lineEdit_pass_new.text()
        xacnhan = self.ui.lineEdit_confirm_pass.text()

        if not tendn or not passcu or not tendnmoi or not passmoi or not xacnhan:
            QtWidgets.QMessageBox.critical(None, 'Lỗi', 'Vui lòng điền đầy đủ thông tin!')
            return

        admin = Admin(tendn, passcu)
        if not admin.login():
            QtWidgets.QMessageBox.critical(None, 'Lỗi', 'Mật khẩu cũ không đúng!')
            return

        if passmoi != xacnhan:
            QtWidgets.QMessageBox.critical(None, 'Lỗi', 'Mật khẩu mới không khớp! Vui lòng thử lại.')
            return

        if admin.change_password(passmoi, tendnmoi):
            QtWidgets.QMessageBox.information(None, 'Thông báo', 'Đổi mật khẩu thành công!')
            self.close()
        else:
            QtWidgets.QMessageBox.critical(None, 'Lỗi', 'Đổi mật khẩu thất bại!')
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = changePass()
    window.show()
    sys.exit(app.exec())
