import mysql.connector
from QLKS.DAO.dbManager import dbMng


class Admin():
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.role = None  # Thêm một biến để lưu quyền của admin

    def login(self):
        db = dbMng()
        db.open_connect()
        try:
            # Truy vấn mật khẩu và phân quyền của người dùng
            db.cur.execute("SELECT matKhau, quyenHan FROM admin WHERE tenDangNhap = %s", (self.username,))
            admin_info = db.cur.fetchone()

            if admin_info:
                stored_password, role = admin_info
                # So sánh mật khẩu đã lưu trong cơ sở dữ liệu với mật khẩu người dùng nhập
                if stored_password == self.password:
                    self.role = role  # Lưu phân quyền vào đối tượng admin
                    return True
                else:
                    return False
            else:
                return False
        except mysql.connector.Error as e:
            print(f"Lỗi khi đăng nhập: {e}")
            return False
        finally:
            db.close_connect()

    def get_role(self):
        # Trả về phân quyền của admin
        return self.role

    def change_password(self, new_password, new_username):
        db = dbMng()
        db.open_connect()
        try:
            # Kiểm tra xem tên đăng nhập và mật khẩu mới có hợp lệ không
            if not new_password or not new_username:
                print("Tên đăng nhập hoặc mật khẩu mới không được để trống")
                return False

            # Cập nhật mật khẩu và tên đăng nhập mới
            db.cur.execute("UPDATE admin SET matKhau = %s, tenDangNhap = %s WHERE tenDangNhap = %s",
                           (new_password, new_username, self.username))
            db.conn.commit()
            print("Đổi mật khẩu thành công")
            return True
        except mysql.connector.Error as e:
            print(f"Lỗi khi đổi mật khẩu: {e}")
            return False
        finally:
            db.close_connect()
