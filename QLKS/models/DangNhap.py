from PyQt6 import QtWidgets
from QLKS.View.DangNhap_View import DangNhap
from QLKS.models.admin import Admin

class DangNhapApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = DangNhap()
        self.ui.setupUi(self)

        # Kết nối tín hiệu
        self.ui.btn_DangNhap.clicked.connect(self.login_admin)
        self.ui.btn_Thoat.clicked.connect(QtWidgets.QApplication.instance().quit)

        # Biến lưu quyền của người dùng sau khi đăng nhập
        self.role = None

    def login_admin(self):
        username = self.ui.lineEdit_Username.text()
        password = self.ui.lineEdit_pass.text()

        if not username or not password:
            QtWidgets.QMessageBox.critical(self, 'Lỗi', 'Vui lòng nhập tên đăng nhập và mật khẩu!')
            return

        admin = Admin(username, password)
        if admin.login():
            QtWidgets.QMessageBox.information(self, 'Thành Công', 'Đăng nhập thành công!')
            self.check_role(admin)  # Kiểm tra quyền của admin
            self.open_main_screen()
            self.close()  # Đóng cửa sổ đăng nhập
        else:
            QtWidgets.QMessageBox.critical(self, 'Thất Bại', 'Đăng nhập thất bại!')

    def check_role(self, admin):
        role = admin.get_role()  # Lấy quyền của admin
        # Kiểm tra quyền của admin
        self.role = role  # Lưu quyền vào biến role

        if role == 'LeTan':
            QtWidgets.QMessageBox.information(self, 'Quyền LeTan', 'Bạn đang đăng nhập với quyền Lễ Tân.')
        elif role == 'QuanLy':
            QtWidgets.QMessageBox.information(self, 'Quyền QuanLy', 'Bạn đang đăng nhập với quyền Quản Lý.')

    def open_main_screen(self):
        from QLKS.models.qlks import qlks  # Import khi cần
        self.main_window = qlks(self.role)  # Truyền quyền vào cửa sổ chính
        self.main_window.show()  # Hiển thị cửa sổ chính


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = DangNhapApp()
    window.show()  # Hiển thị cửa sổ đăng nhập
    sys.exit(app.exec())
