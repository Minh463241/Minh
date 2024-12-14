import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
)
import mysql.connector


class AddAccountApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.connect_db()

    def initUI(self):
        self.setWindowTitle("Thêm tài khoản")
        self.setGeometry(200, 200, 400, 300)

        # Layout
        layout = QVBoxLayout()

        # Title
        title = QLabel("Thêm Tài Khoản Mới")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: blue;")
        layout.addWidget(title)

        # Username
        self.username_label = QLabel("Tên đăng nhập:")
        layout.addWidget(self.username_label)
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        # Password
        self.password_label = QLabel("Mật khẩu:")
        layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Role
        self.role_label = QLabel("Phân quyền:")
        layout.addWidget(self.role_label)
        self.role_combo = QComboBox()
        self.role_combo.addItems(["LeTan", "QuanLy"])
        layout.addWidget(self.role_combo)

        # Add Button
        self.add_button = QPushButton("Thêm tài khoản")
        self.add_button.clicked.connect(self.add_account)
        layout.addWidget(self.add_button)

        # Set layout
        self.setLayout(layout)

    def connect_db(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",  # Đổi thành user của bạn
                password="",  # Đổi thành password của bạn
                database="qlks",
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Lỗi kết nối", f"Lỗi: {err}")
            sys.exit()

    from PyQt6.QtWidgets import QMessageBox

    def add_account(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_combo.currentText().strip()  # Lấy quyền hạn từ combobox

        if not username or not password or not role:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin!")
            return

        try:
            # Kiểm tra xem tên đăng nhập đã tồn tại chưa
            check_query = "SELECT * FROM admin WHERE tenDangNhap = %s"
            self.cursor.execute(check_query, (username,))
            if self.cursor.fetchone():
                QMessageBox.warning(self, "Lỗi", "Tên đăng nhập đã tồn tại!")
                return

            # Thêm tài khoản mới với quyền hạn
            query = "INSERT INTO admin (tenDangNhap, matKhau, quyenHan) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (username, password, role))
            self.conn.commit()

            QMessageBox.information(self, "Thành công", "Thêm tài khoản thành công!")
            self.username_input.clear()
            self.password_input.clear()
            self.role_combo.setCurrentIndex(0)  # Đặt lại combobox về trạng thái mặc định
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Lỗi", f"Không thể thêm tài khoản: {err}")


def main():
    app = QApplication(sys.argv)
    window = AddAccountApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
