import mysql.connector
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QApplication, QMessageBox
from QLKS.DAO.dbManager import dbMng
from QLKS.models import ChangePass, DangNhap, dichvu
from QLKS.View.QuanLyKS_view import Main  # Lớp giao diện chính
from QLKS.models.thanhtoan import thanhToan

import sys
class qlks(Main):
       def __init__(self, role):
          super().__init__()  # Khởi tạo QMainWindow trước
          self.ui = Main()  # Khởi tạo giao diện từ lớp Main
          self.ui.setupUi(self)  # Thiết lập giao diện
          self.role = role
          # Sau đó kết nối các tín hiệu với slot (sự kiện)
          # Truy cập các nút thông qua self.ui
          self.ui.btn_TKKH.clicked.connect(self.tk)
          self.ui.btn_timkiem_P.clicked.connect(self.tkPhong)
          self.ui.them_P.clicked.connect(self.themphong)
          self.ui.sua_P.clicked.connect(self.suaphong)
          self.ui.xoa_P.clicked.connect(self.xoaphong)
          self.ui.sua_TTKH.clicked.connect(self.suakhachhang)
          self.ui.xoa_KH.clicked.connect(self.xoakhachhang)
          self.ui.btn_Logout.clicked.connect(self.dangxuat)
          self.ui.btn_Logout.clicked.connect(QtWidgets.QApplication.instance().quit)
          self.ui.btn_DP.clicked.connect(self.datphong)
          self.ui.comboBox_DP.currentIndexChanged.connect(self.on_combobox_changed)
          self.ui.btn_ChangePass.clicked.connect(self.doimk)
          self.ui.btn_DV_DP.clicked.connect(self.dichvu)
          self.ui.btn_inHD.clicked.connect(self.thanhtoan)
          self.ui.btn_TK_DP.clicked.connect(self.tkdatphong)
          self.ui.btn_SDDV.clicked.connect(self.sddv)
          self.ui.btn_themtk.clicked.connect(self.themtk)

          self.loadDSPComboBox()
          self.loadDSP()
          self.loadDSKH()
          self.loadDSDP()

          self.ui.btn_taoHD.clicked.connect(self.themHoaDon)
          self.ui.btn_suaHD.clicked.connect(self.suaHoaDon)

          self.ui.comboBox_MDP_HD.currentIndexChanged.connect(self.cobb_HD)

          # Tải danh sách mã đặt phòng và loại thanh toán
          self.load_maDatPhong()
          self.load_loaiThanhToan()
          self.hienthiHD()

          self.ui.btn_thongke.clicked.connect(self.load_data)

       def doimk(self):
           from QLKS.models.ChangePass import changePass
           self.main_window = changePass()  # Khởi tạo cửa sổ chính từ lớp qlks
           self.main_window.show()

       def themtk(self):
           if self.role == 'QuanLy':  # Kiểm tra quyền trước khi mở giao diện thêm tài khoản
               self.open_add_account_window()
           else:
               QtWidgets.QMessageBox.warning(self, 'Lỗi quyền', 'Quyền này chỉ Quản Lý mới được sử dụng.')

       def open_add_account_window(self):
           from QLKS.models.ThemTK import AddAccountApp
           self.window = AddAccountApp()  # Khởi tạo đối tượng AddAccountApp
           self.window.show()

       def sddv(self):
           from QLKS.models.dichvu import DichVu
           self.main_window = DichVu()  # Khởi tạo cửa sổ chính từ lớp qlks
           self.main_window.show()

       def load_data(self):
           # Lấy tháng từ ComboBox
           thang = self.ui.comboBox.currentIndex() + 1  # ComboBox trả về index từ 0, nên cần cộng thêm 1 để lấy tháng thực tế

           # Tạo kết nối tới cơ sở dữ liệu
           db = dbMng()
           db.open_connect()

           # Truy vấn dữ liệu theo tháng
           db.cur.execute("""
               SELECT COUNT(dp.maDatPhong) AS SoLuongDatPhong, 
                      SUM(hd.tongTien) AS TongTien,
                      p.loaiPhong AS LoaiPhong, 
                      dp.ngayNhanPhong AS ThoiGianDatPhong
               FROM HoaDon hd
               JOIN DatPhong dp ON hd.maDatPhong = dp.maDatPhong
               JOIN Phong p ON dp.maPhong = p.maPhong
               WHERE MONTH(dp.ngayNhanPhong) = %s
               GROUP BY p.loaiPhong, dp.ngayNhanPhong
               ORDER BY COUNT(dp.maDatPhong) DESC
               LIMIT 1  -- Lấy loại phòng được đặt nhiều nhất
           """, (thang,))  # Truyền thang như tham số cho câu lệnh SQL

           # Lấy kết quả của truy vấn
           data = db.cur.fetchall()

           # Hiển thị dữ liệu trong tableView
           model = QtGui.QStandardItemModel()
           model.setHorizontalHeaderLabels(
               ['Số lượng đặt phòng', 'Tổng tiền', 'Loại phòng phổ biến', 'Thời gian đặt phòng'])

           for row in data:
               items = [QtGui.QStandardItem(str(field)) for field in row]  # Tạo các phần tử trong từng hàng
               model.appendRow(items)

           # Đặt mô hình dữ liệu vào tableView
           self.ui.tableView_TK.setModel(model)

           # Đóng kết nối cơ sở dữ liệu
           db.close_connect()

       def tkdatphong(self):
           ngay_den = self.ui.NgayDen_DP.date().toString("yyyy-MM-dd")
           ngay_di = self.ui.NgayDi_DP.date().toString("yyyy-MM-dd")

           try:
               db = dbMng()
               db.open_connect()

               # Truy vấn dữ liệu từ cơ sở dữ liệu
               query = """
                   SELECT P.soPhong, K.tenKhachHang, 
                          CASE WHEN DP.ngayNhanPhong IS NOT NULL THEN 'Đã Đặt' ELSE 'Trống' END AS trangThai,
                          P.kieuPhong, P.loaiPhong, DP.ngayNhanPhong, DP.ngayTraPhong
                   FROM Phong P
                   LEFT JOIN DatPhong DP ON P.maPhong = DP.maPhong AND (
                       (%s BETWEEN DP.ngayNhanPhong AND DP.ngayTraPhong OR
                        %s BETWEEN DP.ngayNhanPhong AND DP.ngayTraPhong)
                       OR
                       (%s <= DP.ngayNhanPhong AND %s >= DP.ngayTraPhong)
                   )
                   LEFT JOIN KhachHang K ON DP.maKhachHang = K.maKhachHang
               """
               db.cur.execute(query, (ngay_den, ngay_di, ngay_den, ngay_di))

               results = db.cur.fetchall()

               # Hiển thị dữ liệu trên bảng
               self.ui.tableWidget_DSDP.setRowCount(0)
               for row_number, row_data in enumerate(results):
                   self.ui.tableWidget_DSDP.insertRow(row_number)
                   for column_number, data in enumerate(row_data):
                       self.ui.tableWidget_DSDP.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

               db.cur.close()
           except mysql.connector.Error as err:
               print(f"Error: {err}")
           except Exception as e:
               print(f"Error: {e}")
           finally:
               db.close_connect()

       def load_maDatPhong(self):
           db = dbMng()
           db.open_connect()
           db.cur.execute("SELECT maDatPhong FROM DatPhong")
           row = db.cur.fetchall()
           for maDatPhong in row:
               self.ui.comboBox_MDP_HD.addItem(str(maDatPhong[0]))
           db.close_connect()

       def cobb_HD(self, index):
           try:
               db = dbMng()
               db.open_connect()
               madatPhong = self.ui.comboBox_MDP_HD.currentText()  # Lấy mã phòng được chọn từ combobox

               db.cur.execute("SELECT maPhong, maKhachHang FROM datphong WHERE maDatPhong = %s", (madatPhong,))
               row = db.cur.fetchone()

               if row:
                   self.ui.textEdit_MP_HD.setText(str(row[0]))  # Hiển thị
                   self.ui.textEdit_KH_HD.setText(str(row[1]))  # Hiển thị
               else:
                   self.ui.textEdit_MP_HD.setText("")  # Xóa nội dung nếu không tìm thấy thông tin
                   self.ui.textEdit_KH_HD.setText("")

               db.cur.close()

           except mysql.connector.Error as err:
               print(f"Error: {err}")

       def closeEvent(self, event):
           event.accept()

       def load_loaiThanhToan(self):
           loaiThanhToans = ["Tiền mặt", "Thẻ tín dụng", "Chuyển khoản"]
           self.ui.comboBox_LoaiTT.addItems(loaiThanhToans)

       def themHoaDon(self):
           maDatPhong = self.ui.comboBox_MDP_HD.currentText()
           loaiThanhToan = self.ui.comboBox_LoaiTT.currentText()
           maphong = self.ui.textEdit_MP_HD.toPlainText()

           # Kiểm tra xem các trường thông tin có bị bỏ trống không
           if not maDatPhong or not loaiThanhToan or not maphong:
               QtWidgets.QMessageBox.warning(self.ui.centralwidget, "Thông Báo", "Vui lòng điền đầy đủ thông tin.")
               return

           # Kết nối tới cơ sở dữ liệu
           db = dbMng()
           db.open_connect()

           try:
               # Kiểm tra xem đã tồn tại hóa đơn cho mã phòng và khách hàng này chưa
               db.cur.execute("SELECT COUNT(*) FROM HoaDon WHERE maDatPhong = %s", (maDatPhong,))
               count = db.cur.fetchone()[0]

               if count > 0:
                   QtWidgets.QMessageBox.warning(self.ui.centralwidget, "Lỗi", "Đã tồn tại hóa đơn cho mã phòng này")
                   return

               # Lấy chi phí phòng
               db.cur.execute(
                   "SELECT p.gia, dp.maKhachHang FROM Phong p JOIN DatPhong dp ON p.maPhong = dp.maPhong WHERE dp.maDatPhong = %s",
                   (maDatPhong,))
               datPhong = db.cur.fetchone()
               if datPhong:
                   giaPhong = datPhong[0]
                   maKhachHang = datPhong[1]
               else:
                   giaPhong = 0
                   maKhachHang = None

               # Tạo hóa đơn và lưu mã khách hàng
               db.cur.execute(
                   "INSERT INTO HoaDon (maDatPhong, tongTien, maPhong, LoaiThanhToan, maKhachHang) VALUES (%s, %s, %s, %s, %s)",
                   (maDatPhong, giaPhong, maphong, loaiThanhToan, maKhachHang))
               db.conn.commit()

               QtWidgets.QMessageBox.information(self.ui.centralwidget, "Thông Báo", "Hóa Đơn Đã Được Tạo")
               self.hienthiHD()  # Giả sử phương thức này tồn tại để làm mới danh sách hóa đơn

           except mysql.connector.Error as err:
               QtWidgets.QMessageBox.warning(self.ui.centralwidget, "Lỗi", f"Lỗi khi tạo hóa đơn: {err}")

           finally:
               db.close_connect()

       def suaHoaDon(self):
           try:
               maHoaDon = self.ui.textEdit_MaHD.toPlainText()
               loaiThanhToan = self.ui.comboBox_LoaiTT.currentText()

               db = dbMng()
               db.open_connect()
               db.cur.execute("UPDATE HoaDon SET LoaiThanhToan = %s WHERE maHoaDon = %s",
                              (loaiThanhToan, maHoaDon))
               db.conn.commit()

               QtWidgets.QMessageBox.information(None, "Thông Báo", "Hóa Đơn Đã Được Sửa")
               self.hienthiHD()

           except mysql.connector.Error as err:
               QMessageBox.warning(None, "thong bao", "loi")
           finally:
               db.close_connect()

       def hienthiHD(self):
           db = dbMng()
           db.open_connect()
           db.cur.execute("SELECT maHoaDon, maDatPhong,maKhachHang, maPhong, tongTien, LoaiThanhToan, status FROM HoaDon")
           invoices = db.cur.fetchall()
           db.close_connect()
           self.ui.tableWidget_HD.setRowCount(0)
           for row_number, row_data in enumerate(invoices):
               self.ui.tableWidget_HD.insertRow(row_number)
               for column_number, data in enumerate(row_data):
                   self.ui.tableWidget_HD.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

       def dichvu(self):
           from QLKS.models.dichvu import DichVu
           self.main_window = DichVu()  # Khởi tạo cửa sổ chính từ lớp qlks
           self.main_window.show()

       def thanhtoan(self):
           self.another_from = QtWidgets.QMainWindow()
           self.ui = thanhToan()
           self.ui.setupUi(self.another_from)
           self.another_from.show()

       def datphong(self):
           db = dbMng()
           db.open_connect()

           # Lấy dữ liệu từ giao diện
           ten = self.ui.ten_DP.toPlainText().strip()
           qt = self.ui.QT_DP.currentText()
           cccd = self.ui.CCCDKH_DP.toPlainText().strip()
           sdt = self.ui.SDTKH_DP.toPlainText().strip()
           ngayden = self.ui.NgayDen_DP.date().toString("yyyy-MM-dd")
           ngaydi = self.ui.NgayDi_DP.date().toString("yyyy-MM-dd")
           maphong = self.ui.comboBox_DP.currentText()

           # Lấy giới tính
           gt = ""
           if self.ui.nam_DP.isChecked():
               gt = self.ui.nam_DP.text()
           elif self.ui.nu_DP.isChecked():
               gt = self.ui.nu_DP.text()
           elif self.ui.khac_DP.isChecked():
               gt = self.ui.khac_DP.text()

           # Kiểm tra trường trống
           if not ten or not sdt or not cccd or not ngayden or not ngaydi or not maphong or not gt:
               QtWidgets.QMessageBox.warning(None, "Thông Báo", "Vui lòng điền đầy đủ thông tin.")
               return

           # Kiểm tra định dạng số điện thoại và CCCD
           if not sdt.isdigit() or not cccd.isdigit():
               QtWidgets.QMessageBox.warning(None, "Thông Báo", "Số điện thoại và CCCD phải là số.")
               return

           # Kiểm tra ngày đến và ngày đi
           from datetime import datetime, date
           today = date.today().strftime("%Y-%m-%d")  # Lấy ngày hiện tại
           if ngayden < today:
               QtWidgets.QMessageBox.warning(None, "Thông Báo",
                                             "Ngày đến phải lớn hơn hoặc bằng ngày hiện tại.")
               return
           if ngaydi < ngayden:
               QtWidgets.QMessageBox.warning(None, "Thông Báo",
                                             "Ngày đi phải lớn hơn hoặc bằng ngày đến.")
               return

           try:
               # Kiểm tra trùng lặp số điện thoại và CCCD trong cơ sở dữ liệu
               db.cur.execute("SELECT COUNT(*) FROM KhachHang WHERE soDienThoai = %s OR CCCD = %s", (sdt, cccd))
               if db.cur.fetchone()[0] > 0:
                   QtWidgets.QMessageBox.warning(None, "Thông Báo",
                                                 "Số điện thoại hoặc CCCD đã tồn tại.")
                   return

               # Thêm thông tin khách hàng mới vào bảng KhachHang
               db.cur.execute(
                   "INSERT INTO KhachHang (tenKhachHang, soDienThoai, CCCD, quocTich, gioiTinh) VALUES (%s, %s, %s, %s, %s)",
                   (ten, sdt, cccd, qt, gt)
               )
               makh = db.cur.lastrowid  # Lấy mã khách hàng vừa thêm vào

               if makh == 0:
                   print(None, "Thông Báo",
                                                 "Lỗi khi thêm khách hàng vào cơ sở dữ liệu.")
                   return

               # Thêm thông tin đặt phòng mới vào bảng DatPhong
               db.cur.execute(
                   "INSERT INTO DatPhong (maPhong, maKhachHang, ngayNhanPhong, ngayTraPhong) VALUES (%s, %s, %s, %s)",
                   (maphong, makh, ngayden, ngaydi)
               )

               # Cập nhật trạng thái phòng
               db.cur.execute("UPDATE Phong SET trangThai = True WHERE maPhong = %s", (maphong,))

               db.conn.commit()

               QtWidgets.QMessageBox.information(None, "Thông Báo", "Đặt phòng thành công!")
               self.loadDSDP()
               self.loadDSKH()
               self.hienthiHD()
               self.load_maDatPhong()
               self.loadDSP()

           except Exception as e:
               QtWidgets.QMessageBox.warning(None, "Thông Báo", f"Lỗi khi thực hiện: {str(e)}")

       def dangxuat(self):
           self.another_from = QtWidgets.QMainWindow()
           self.ui = DangNhap.DangNhap()
           self.ui.setupUi(self.another_from)
           self.another_from.show()

       def xoakhachhang(self):
           maKhachHang = self.comboBox_MaKH.currentText()

           if not maKhachHang:
               QtWidgets.QMessageBox.warning(self.centralwidget, "Thông Báo", "Vui lòng chọn khách hàng để xóa.")
               return

           reply = QtWidgets.QMessageBox.question(
               self.centralwidget, 'Xác Nhận', 'Bạn có chắc chắn muốn xóa khách hàng này?',
               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No
           )

           if reply == QtWidgets.QMessageBox.Yes:
               try:
                   # Xóa khách hàng khỏi cơ sở dữ liệu
                   db = dbMng()
                   db.open_connect()
                   db.cur.execute("DELETE FROM KhachHang WHERE maKhachHang = %s", (maKhachHang,))
                   db.conn.commit()

                   QtWidgets.QMessageBox.information(self.centralwidget, "Thông Báo", "Khách Hàng Đã Được Xóa.")
                   self.loadDSKH()  # Giả sử phương thức này làm mới danh sách khách hàng
               except mysql.connector.Error as err:
                   QtWidgets.QMessageBox.warning(self.centralwidget, "Lỗi", f"Lỗi khi xóa khách hàng: {err}")
               finally:
                   db.close_connect()

       def suakhachhang(self):
           db = dbMng()
           db.open_connect()
           mkh = self.ui.MKH_tbKH.toPlainText()
           ten = self.ui.NameKH_tbKH.toPlainText()
           qt = self.ui.comboBox_tbKH.currentText()
           cccd = self.ui.CCCDKH_tbKH.toPlainText()
           sdt = self.ui.SDTKH_tbKH.toPlainText()
           gt = ""
           if self.ui.nam.isChecked():
               gt = self.ui.nam.text()
           elif self.ui.nu.isChecked():
               gt = self.ui.nu.text()
           else:
               gt = self.ui.khac.text()
           try:
               db.cur.execute(
                   "UPDATE khachhang SET tenKhachHang = %s, soDienThoai = %s, CCCD = %s, quocTich = %s, GioiTinh = %s WHERE maKhachHang = %s",
                   (ten, cccd, sdt, qt, gt, mkh))
               db.conn.commit()
               QMessageBox.information(None, "Thành công", "Sửa Khách Hàng Thành Công!")
               self.loadDSKH()
           except mysql.connector.Error as err:
               QMessageBox.critical(None, "Lỗi", f"Đã xảy ra lỗi: {err}")
           finally:
               db.close_connect()

       def xoaphong(self):
           db = dbMng()
           db.open_connect()
           sophong = self.ui.TP_P.toPlainText()

           try:
               db.cur.execute("DELETE FROM phong WHERE soPhong=%s", (sophong,))
               db.conn.commit()
               QMessageBox.information(None, "Thành công", "Xóa phòng thành công!")
               self.loadDSP()

           except mysql.connector.Error as err:
               QMessageBox.critical(None, "Lỗi", f"Đã xảy ra lỗi: {err}")
           finally:
               db.close_connect()

       def suaphong(self):
           db = dbMng()
           db.open_connect()
           map = self.ui.MP_P.toPlainText()
           kieuphong = self.ui.KP_P.currentText()
           sophong = self.ui.TP_P.toPlainText()
           loaiphong = self.ui.LP_P.currentText()
           giaphong = self.ui.GiaP_P.toPlainText()
           if not map:
               QtWidgets.QMessageBox.warning(None, "Thông Báo", "Vui lòng điền mã phòng cần sửa!")
               return
           try:
               db.cur.execute("UPDATE phong SET soPhong=%s,loaiPhong = %s, kieuPhong=%s, gia=%s WHERE maPhong=%s",
                              (sophong, kieuphong, loaiphong, giaphong, map))
               db.conn.commit()
               QMessageBox.information(None, "Thành công", "Sửa phòng thành công!")
               self.loadDSP()
           except mysql.connector.Error as err:
               QMessageBox.critical(None, "Lỗi", f"Đã xảy ra lỗi: {err}")
           finally:
               db.close_connect()

       def themphong(self):
           db = dbMng()
           db.open_connect()
           kieuphong = self.ui.KP_P.currentText()
           tenphong = self.ui.TP_P.toPlainText()
           loaiphong = self.ui.LP_P.currentText()
           giaphong = self.ui.GiaP_P.toPlainText()

           try:
               db.cur.execute(
                   "INSERT INTO phong (soPhong, loaiPhong, kieuPhong,gia,trangThai) VALUES (%s, %s, %s, %s, 0)",
                   (tenphong, kieuphong, loaiphong, giaphong))
               db.conn.commit()
               QMessageBox.information(None, "Thành công", "Thêm phòng thành công!")
               self.loadDSPComboBox()
               self.loadDSP()
           except mysql.connector.Error as err:
               QMessageBox.critical(None, "Lỗi", f"Đã xảy ra lỗi: {err}")
           finally:
               db.close_connect()

       def loadDSPComboBox(self):
           try:
               db = dbMng()
               db.open_connect()
               db.cur.execute("SELECT maPhong FROM Phong")
               rows = db.cur.fetchall()
               for row in rows:
                   self.ui.comboBox_DP.addItem(str(row[0]))  # Thêm mã phòng vào combobox
               db.close_connect()
           except mysql.connector.Error as err:
               print(f"Error: {err}")

       def on_combobox_changed(self, index):
           try:
               db = dbMng()
               db.open_connect()
               maPhong = self.ui.comboBox_DP.currentText()  # Lấy mã phòng được chọn từ combobox

               db.cur.execute("SELECT loaiPhong, kieuPhong, trangThai FROM Phong WHERE maPhong = %s", (maPhong,))
               row = db.cur.fetchone()

               if row:
                   self.ui.KP_DP.setText(row[0])  # Hiển thị loại phòng
                   self.ui.KP_DP_2.setText("Đã đặt" if row[2] else "Còn trống")  # Hiển thị tình trạng phòng
                   self.ui.KP_DP_3.setText(row[1])  # Hiển thị kiểu phòng
               else:
                   self.ui.KP_DP.setText("")  # Xóa nội dung nếu không tìm thấy thông tin
                   self.ui.KP_DP_2.setText("")
                   self.ui.KP_DP_3.setText("")

               db.close_connect()
           except mysql.connector.Error as err:
               print(f"Error: {err}")

       def tkPhong(self):
           db = dbMng()
           db.open_connect()
           try:
               ten = self.ui.tk_P.toPlainText()
               if ten == "":
                   return self.loadDSP()
               else:
                   db.cur.execute("SELECT * FROM phong WHERE soPhong LIKE %s", (ten,))
                   kq = db.cur.fetchall()
                   self.ui.tableWidget_DSP.setRowCount(len(kq))
                   for x1, y1 in enumerate(kq):
                       for x2, y2 in enumerate(y1):
                           self.ui.tableWidget_DSP.setItem(x1, x2, QtWidgets.QTableWidgetItem(str(y2)))

           except mysql.connector.Error as err:
               QMessageBox.information(None, "Thong Báo", f"{err}")
           finally:
               db.close_connect()

       def tk(self):
           db = dbMng()
           db.open_connect()
           cccd = self.ui.tkKH.toPlainText()
           if cccd == "":
               return self.loadDSKH()
           else:
               db.cur.execute("SELECT * FROM khachhang WHERE CCCD LIKE %s", ('%' + cccd + '%',))

               kq = db.cur.fetchall()
               self.ui.tableWidget_DSKH.setRowCount(len(kq))
               for x1, y1 in enumerate(kq):
                   for x2, y2 in enumerate(y1):
                       self.ui.tableWidget_DSKH.setItem(x1, x2, QtWidgets.QTableWidgetItem(str(y2)))
               db.close_connect()

       def loadDSDP(self):
           db = dbMng()
           db.open_connect()
           db.cur.execute("""
                                                      SELECT 
                                                          phong.soPhong AS 'Tên phòng',
                                                          khachhang.tenKhachHang AS 'Tên Khách hàng',
                                                          phong.trangThai AS 'Trạng thái',
                                                          phong.kieuPhong AS 'Kiểu phòng',
                                                          phong.loaiPhong AS 'Loại phòng',
                                                          datphong.ngayNhanPhong AS 'Ngày đến',
                                                          datphong.ngayTraPhong AS 'Ngày đi'
                                                      FROM 
                                                          datphong
                                                      INNER JOIN 
                                                          khachhang ON datphong.maKhachHang = khachhang.maKhachHang
                                                      INNER JOIN 
                                                          phong ON datphong.maPhong = phong.maPhong
                                                  """)

           kq = db.cur.fetchall()
           self.ui.tableWidget_DSDP.setRowCount(len(kq))

           for row_index, row_data in enumerate(kq):
               for col_index, col_data in enumerate(row_data):
                   item = QtWidgets.QTableWidgetItem(str(col_data))
                   self.ui.tableWidget_DSDP.setItem(row_index, col_index, item)
           db.close_connect()

       def loadDSKH(self):
           db = dbMng()
           db.open_connect()
           db.cur.execute("SELECT * FROM khachhang")
           kq = db.cur.fetchall()
           self.ui.tableWidget_DSKH.setRowCount(len(kq))
           for x1, y1 in enumerate(kq):
               for x2, y2 in enumerate(y1):
                   self.ui.tableWidget_DSKH.setItem(x1, x2, QtWidgets.QTableWidgetItem(str(y2)))
           db.close_connect()

       def loadDSP(self):
           db = dbMng()
           db.open_connect()
           db.cur.execute("SELECT * FROM phong")
           kq = db.cur.fetchall()
           self.ui.tableWidget_DSP.setRowCount(len(kq))
           for x1, y1 in enumerate(kq):
               for x2, y2 in enumerate(y1):
                   self.ui.tableWidget_DSP.setItem(x1, x2, QtWidgets.QTableWidgetItem(str(y2)))
           db.close_connect()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Truyền tham số role vào khi tạo đối tượng qlks
    role = 'QuanLy'  # Hoặc lấy giá trị role từ nơi khác như đăng nhập
    window = qlks(role)  # Tạo cửa sổ chính và truyền tham số role vào
    window.show()  # Hiển thị cửa sổ

    sys.exit(app.exec())  # Bắt đầu vòng lặp sự kiện
