from PyQt6 import QtCore, QtGui, QtWidgets
import mysql.connector
from PyQt6.QtWidgets import QMessageBox

from QLKS.DAO.dbManager import dbMng


class thanhToan(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 700)
        MainWindow.setWindowTitle("Quản lý thanh toán hóa đơn")

        # Central Widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Layout chính
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # GroupBox: Chọn hóa đơn
        self.group_invoice = QtWidgets.QGroupBox("Chọn hóa đơn")
        self.group_invoice_layout = QtWidgets.QHBoxLayout(self.group_invoice)
        self.comboBox_TT = QtWidgets.QComboBox(self.group_invoice)
        self.btn_xemHD = QtWidgets.QPushButton("Xem hóa đơn", self.group_invoice)
        self.btn_xemHD.setIcon(QtGui.QIcon("icons/view.png"))  # Thêm biểu tượng (nếu có)
        self.group_invoice_layout.addWidget(QtWidgets.QLabel("Mã hóa đơn:"))
        self.group_invoice_layout.addWidget(self.comboBox_TT)
        self.group_invoice_layout.addWidget(self.btn_xemHD)
        self.main_layout.addWidget(self.group_invoice)

        # GroupBox: Hiển thị hóa đơn
        self.group_display = QtWidgets.QGroupBox("Thông tin hóa đơn")
        self.group_display_layout = QtWidgets.QVBoxLayout(self.group_display)
        self.textBrowser = QtWidgets.QTextBrowser(self.group_display)
        self.group_display_layout.addWidget(self.textBrowser)
        self.main_layout.addWidget(self.group_display)

        # GroupBox: Chức năng thanh toán
        self.group_actions = QtWidgets.QGroupBox("Chức năng")
        self.group_actions_layout = QtWidgets.QHBoxLayout(self.group_actions)
        self.btn_huy = QtWidgets.QPushButton("Hủy", self.group_actions)
        self.btn_huy.setIcon(QtGui.QIcon("icons/cancel.png"))  # Thêm biểu tượng (nếu có)
        self.btn_thanhToan = QtWidgets.QPushButton("Thanh toán", self.group_actions)
        self.btn_thanhToan.setFont(QtGui.QFont("Arial", 14))
        self.btn_thanhToan.setIcon(QtGui.QIcon("icons/pay.png"))  # Thêm biểu tượng (nếu có)
        self.group_actions_layout.addWidget(self.btn_huy)
        self.group_actions_layout.addWidget(self.btn_thanhToan)
        self.main_layout.addWidget(self.group_actions)

        # Set central widget
        MainWindow.setCentralWidget(self.centralwidget)

        # Status bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        # Kết nối chức năng
        self.btn_xemHD.clicked.connect(self.xemHoaDon)
        self.btn_thanhToan.clicked.connect(self.thanhToanHoaDon)

        # Load danh sách mã hóa đơn
        self.taiMaHoaDon()

    def taiMaHoaDon(self):
        db = dbMng()
        db.open_connect()
        db.cur.execute("SELECT maHoaDon FROM HoaDon WHERE status = 'ctt'")
        invoice_ids = db.cur.fetchall()
        for invoice_id in invoice_ids:
            self.comboBox_TT.addItem(str(invoice_id[0]))
        db.close_connect()

    def xemHoaDon(self):
        maHoaDon = self.comboBox_TT.currentText()
        db = dbMng()
        db.open_connect()
        db.cur.execute("""
                        SELECT hd.maHoaDon, hd.maPhong, hd.tongTien, hd.LoaiThanhToan,
                               dp.ngayNhanPhong, dp.ngayTraPhong, p.soPhong, kh.tenKhachHang,
                               dv.tenDichVu, sdv.soLuong, dv.gia, (sdv.soLuong * dv.gia) AS thanhTien
                        FROM HoaDon hd
                        JOIN DatPhong dp ON hd.maDatPhong = dp.maDatPhong
                        JOIN Phong p ON hd.maPhong = p.maPhong
                        JOIN KhachHang kh ON dp.maKhachHang = kh.maKhachHang
                        LEFT JOIN SuDungDichVu sdv ON kh.maKhachHang = sdv.maKhachHang
                        LEFT JOIN DichVu dv ON sdv.maDichVu = dv.maDichVu
                        WHERE hd.maHoaDon = %s AND hd.status = 'ctt'
                    """, (maHoaDon,))
        invoice_details = db.cur.fetchall()
        if invoice_details:
            content = f"<h2>HÓA ĐƠN THANH TOÁN</h2>"
            content += f"<p>Mã hóa đơn: {invoice_details[0][0]}</p>"
            content += f"<p>Phòng: {invoice_details[0][6]}</p>"
            content += f"<p>Khách hàng: {invoice_details[0][7]}</p>"
            content += f"<p>Ngày nhận phòng: {invoice_details[0][4]}</p>"
            content += f"<p>Ngày trả phòng: {invoice_details[0][5]}</p>"
            content += f"<table border='1'><tr><th>Dịch vụ</th><th>Số lượng</th><th>Đơn giá</th><th>Thành tiền</th></tr>"
            total_service_amount = 0
            for detail in invoice_details:
                if detail[8]:
                    content += f"<tr><td>{detail[8]}</td><td>{detail[9]}</td><td>{detail[10]}</td><td>{detail[11]}</td></tr>"
                    total_service_amount += detail[11]
            content += f"</table><p>Tổng dịch vụ: {total_service_amount}</p>"
            content += f"<p>Tiền phòng: {invoice_details[0][2]}</p>"
            content += f"<p><b>Tổng cộng: {invoice_details[0][2] + total_service_amount}</b></p>"
            self.textBrowser.setHtml(content)
        else:
            self.textBrowser.setHtml("<p>Không tìm thấy hóa đơn.</p>")
        db.close_connect()

    def thanhToanHoaDon(self):
        from QLKS.models.qlks import qlks
        maHoaDon = self.comboBox_TT.currentText()  # Giả sử mã hóa đơn được chọn từ comboBox
        db = dbMng()
        db.open_connect()

        try:
            # Cập nhật trạng thái của hóa đơn thành 'Đã Thanh Toán'
            db.cur.execute("UPDATE HoaDon SET status = 'Đã Thanh Toán' WHERE maHoaDon = %s", (maHoaDon,))
            db.conn.commit()

            # Lấy mã đặt phòng từ hóa đơn
            db.cur.execute("SELECT maDatPhong FROM HoaDon WHERE maHoaDon = %s", (maHoaDon,))
            maDatPhong = db.cur.fetchone()[0]

            # Cập nhật trạng thái phòng thành 'Trống' (trangThai = 0) trong bảng Phong
            db.cur.execute(
                "UPDATE Phong SET trangThai = 0 WHERE maPhong = (SELECT maPhong FROM DatPhong WHERE maDatPhong = %s)",
                (maDatPhong,)
            )
            db.conn.commit()

            # Thông báo thành công
            QMessageBox.information(self, "Thanh toán thành công", "Hóa đơn đã được thanh toán thành công!")

        except Exception as e:
            db.conn.rollback()  # Rollback nếu có lỗi
            QMessageBox.warning(self, "Lỗi", f"Đã xảy ra lỗi: {str(e)}")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = thanhToan()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
