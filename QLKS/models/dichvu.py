import sys
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.uic.properties import QtWidgets

from QLKS.View.dichvu_View import DichVuApp
from QLKS.DAO.dbManager import dbMng


class DichVu(QMainWindow, DichVuApp):
    def __init__(self):
        super().__init__()
        self.db = dbMng()
        self.setupUi(self)
        self.load_khach_hang()
        self.load_dich_vu()
        self.load_dich_vu_table()

        # Gắn sự kiện cho các nút
        self.btn_Them_DV.clicked.connect(self.them_dich_vu)
        self.btn_Sua_DV.clicked.connect(self.sua_dich_vu)
        self.btn_Xoa_DV.clicked.connect(self.xoa_dich_vu)
        self.btn_Huy.clicked.connect(self.huy_thao_tac)
        self.btn_dongy.clicked.connect(self.dong_y_dich_vu)

    # Tải danh sách khách hàng
    def load_khach_hang(self):
        try:
            query = "SELECT maKhachHang, tenKhachHang FROM KhachHang"
            cursor = self.db.conn.cursor()
            cursor.execute(query)
            khach_hang = cursor.fetchall()
            self.combb_tenkh_dv.clear()
            for kh in khach_hang:
                self.combb_tenkh_dv.addItem(f"{kh[1]} ({kh[0]})", kh[0])
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải khách hàng: {e}")

    # Tải danh sách dịch vụ
    def load_dich_vu(self):
        try:
            query = "SELECT maDichVu, tenDichVu FROM DichVu"
            cursor = self.db.conn.cursor()
            cursor.execute(query)
            dich_vu = cursor.fetchall()
            self.combb_madv.clear()
            for dv in dich_vu:
                self.combb_madv.addItem(f"{dv[1]} ({dv[0]})", dv[0])
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải dịch vụ: {e}")

    # Tải dữ liệu dịch vụ vào bảng
    def load_dich_vu_table(self):
        try:
            query = """
                SELECT tenDichVu, soLuong
                FROM SuDungDichVu
                JOIN DichVu ON SuDungDichVu.maDichVu = DichVu.maDichVu
            """
            cursor = self.db.conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            self.tableWidget_DV.setRowCount(0)
            for row_number, row_data in enumerate(data):
                self.tableWidget_DV.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget_DV.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải bảng dịch vụ: {e}")

    # Thêm dịch vụ (do lễ tân thực hiện)
    def them_dich_vu(self):
        tenDV = self.textEdit_tendv.text().strip()  # Đảm bảo sử dụng textEdit_tendv
        giaDV = self.textEdit_gia.text().strip()
        soLuong = self.textEdit_SOL.text().strip()

        if not tenDV or not giaDV or not soLuong:
            QtWidgets.QMessageBox.warning(self, "Cảnh Báo", "Vui lòng điền đầy đủ thông tin!")
            return

        if not giaDV.isdigit() or int(giaDV) <= 0:
            QMessageBox.warning(self, "Lỗi", "Giá dịch vụ phải là số nguyên dương!")
            return

        try:
            query = "INSERT INTO DichVu (tenDichVu, gia) VALUES (%s, %s)"
            cursor = self.db.conn.cursor()
            cursor.execute(query, (tenDV, giaDV))
            self.db.conn.commit()
            QMessageBox.information(self, "Thành công", "Thêm dịch vụ thành công!")
            self.load_dich_vu()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi thêm dịch vụ: {e}")

    # Sửa dịch vụ (do lễ tân thực hiện)
    def sua_dich_vu(self):
        maDV = self.combb_madv.currentData()
        tenDV = self.textEdit_tendv.text().strip()
        giaDV = self.textEdit_gia.text().strip()

        if not maDV or not tenDV or not giaDV:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin dịch vụ!")
            return

        if not giaDV.isdigit() or int(giaDV) <= 0:
            QMessageBox.warning(self, "Lỗi", "Giá dịch vụ phải là số nguyên dương!")
            return

        try:
            query = "UPDATE DichVu SET tenDichVu = %s, gia = %s WHERE maDichVu = %s"
            cursor = self.db.conn.cursor()
            cursor.execute(query, (tenDV, giaDV, maDV))
            self.db.conn.commit()
            QMessageBox.information(self, "Thành công", "Cập nhật dịch vụ thành công!")
            self.load_dich_vu()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi cập nhật dịch vụ: {e}")

    # Xóa dịch vụ (do lễ tân thực hiện)
    def xoa_dich_vu(self):
        maDV = self.combb_madv.currentData()

        try:
            query = "DELETE FROM DichVu WHERE maDichVu = %s"
            cursor = self.db.conn.cursor()
            cursor.execute(query, (maDV,))
            self.db.conn.commit()
            QMessageBox.information(self, "Thành công", "Xóa dịch vụ thành công!")
            self.load_dich_vu()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi xóa dịch vụ: {e}")

    # Đồng ý dịch vụ (đặt dịch vụ cho khách hàng)
    def dong_y_dich_vu(self):
        maKH = self.combb_tenkh_dv.currentData()
        maDV = self.combb_madv.currentData()

        if not maKH or not maDV:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn đầy đủ khách hàng và dịch vụ!")
            return

        soLuong = self.textEdit_SOL.text().strip()

        if not soLuong:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập số lượng dịch vụ!")
            return

        if not soLuong.isdigit() or int(soLuong) <= 0:
            QMessageBox.warning(self, "Lỗi", "Số lượng phải là một số nguyên dương!")
            return

        confirm = QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn đồng ý với dịch vụ này?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                       QMessageBox.StandardButton.No)

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                query = "INSERT INTO SuDungDichVu (maKhachHang, maDichVu, soLuong) VALUES (%s, %s, %s)"
                cursor = self.db.conn.cursor()
                cursor.execute(query, (maKH, maDV, soLuong))  # Sử dụng số lượng đã nhập
                self.db.conn.commit()
                QMessageBox.information(self, "Thành công", "Đồng ý dịch vụ thành công!")
                self.load_dich_vu_table()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi khi đồng ý dịch vụ: {e}")
        else:
            QMessageBox.information(self, "Hủy", "Bạn đã hủy thao tác đồng ý dịch vụ.")

    # Hủy thao tác
    def huy_thao_tac(self):
        self.combb_tenkh_dv.setCurrentIndex(0)
        self.combb_madv.setCurrentIndex(0)
        self.textEdit_SOL.setText("")
        self.textEdit_TenDV.setText("")
        self.textEdit_GiaDV.setText("")
        QMessageBox.information(self, "Thông báo", "Hủy thao tác thành công!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DichVu()
    window.show()
    sys.exit(app.exec())
