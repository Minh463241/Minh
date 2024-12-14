from PyQt6.QtWidgets import QApplication
from QLKS.models.DangNhap import DangNhapApp

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = DangNhapApp()
    window.show()
    sys.exit(app.exec())