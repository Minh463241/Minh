import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QPushButton
from PyQt5.QtGui import QImage, QPixmap
from ultralytics import YOLO
from form import Ui_MainWindow
from PyQt5.QtCore import QTimer

class YOLOTracker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Liên kết nút bấm
        self.ui.btnOpenVideo.clicked.connect(self.open_video)
        self.ui.btnStartTracking.clicked.connect(self.start_tracking)
        self.ui.btnStartCamera.clicked.connect(self.start_camera)
        self.ui.btnStopCamera.clicked.connect(self.stop_camera)
        self.ui.btnExit.clicked.connect(self.close)

        self.video_path = None
        self.model = YOLO('yolov8n.pt')  # Tải model YOLOv8 nhỏ
        self.cap = None  # Đối tượng VideoCapture cho camera hoặc video
        self.out = None  # Đối tượng VideoWriter để ghi video
        self.timer = QTimer(self)  # Để điều khiển việc hiển thị hình ảnh liên tục
        self.timer.timeout.connect(self.update_frame)

        # Khởi tạo các biến để tính toán độ chính xác
        self.true_positive = 0
        self.false_positive = 0
        self.false_negative = 0

    def open_video(self):
        # Mở file video
        options = QFileDialog.Options()
        self.video_path, _ = QFileDialog.getOpenFileName(self, "Chọn video", "",
                                                         "Video Files (*.mp4 *.avi);;All Files (*)", options=options)
        if self.video_path:
            self.ui.labelStatus.setText(f"Đã chọn video: {self.video_path}")
        else:
            self.ui.labelStatus.setText("Chưa chọn video!")

    def start_tracking(self):
        if not self.video_path and not self.cap:
            self.ui.labelStatus.setText("Vui lòng chọn video hoặc mở camera trước!")
            return

        # Nếu đang dùng video, tải video vào VideoCapture
        if self.video_path:
            self.cap = cv2.VideoCapture(self.video_path)

            # Lấy thông tin về video (độ phân giải, fps) để lưu video kết quả
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec video (có thể thay đổi)
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # Tạo đối tượng VideoWriter để ghi video kết quả
            self.out = cv2.VideoWriter('output/output_video.mp4', fourcc, fps, (width, height))

        self.timer.start(30)  # Bắt đầu hiển thị video hoặc camera

    def start_camera(self):
        # Mở camera laptop (ID 0 thường là camera mặc định)
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.ui.labelStatus.setText("Không thể mở camera!")
            return

        self.ui.labelStatus.setText("Đang sử dụng camera...")
        self.timer.start(30)  # Bắt đầu hiển thị hình ảnh từ camera

    def stop_camera(self):
        if self.cap:
            self.cap.release()  # Giải phóng camera hoặc video
            self.cap = None
            self.ui.labelStatus.setText("Đã dừng camera.")

        if self.out:
            self.out.release()  # Giải phóng đối tượng VideoWriter khi không cần ghi video nữa
            self.out = None

        self.timer.stop()  # Dừng việc cập nhật hình ảnh

    def update_frame(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if not ret:
                self.ui.labelStatus.setText("Đã kết thúc video hoặc không nhận được khung hình từ camera.")
                self.stop_camera()  # Dừng khi hết video hoặc không nhận được khung hình

            # Dự đoán đối tượng với YOLO
            results = self.model(frame)
            detections = results[0].boxes.data.numpy()  # Lấy kết quả từ YOLO

            for detection in detections:
                x1, y1, x2, y2, score, class_id = detection
                if score > 0.5:  # Ngưỡng tin cậy
                    # Vẽ khung và tên đối tượng
                    label = f"{self.model.names[int(class_id)]}: {score:.2f}"
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # Tính toán các chỉ số Precision, Recall
                    self.update_metrics(score)

            # Tính toán và in ra các chỉ số
            precision = self.calculate_precision()
            recall = self.calculate_recall()
            print(f"Precision: {precision:.2f}, Recall: {recall:.2f}")

            # Hiển thị khung hình trong giao diện
            self.display_frame(frame)

            # Lưu khung hình vào video kết quả nếu có
            if self.out:
                self.out.write(frame)

    def display_frame(self, frame):
        # Chuyển đổi hình ảnh sang định dạng QPixmap
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)

        # Hiển thị lên QLabel
        self.ui.labelVideo.setPixmap(pixmap)
        self.ui.labelVideo.setScaledContents(True)

    def update_metrics(self, score):
        # Giả định TP (True Positive) nếu điểm tin cậy > 0.5
        if score > 0.5:
            self.true_positive += 1
        else:
            self.false_positive += 1
            self.false_negative += 1

    def calculate_precision(self):
        # Tính Precision = TP / (TP + FP)
        if self.true_positive + self.false_positive == 0:
            return 0
        return self.true_positive / (self.true_positive + self.false_positive)

    def calculate_recall(self):
        # Tính Recall = TP / (TP + FN)
        if self.true_positive + self.false_negative == 0:
            return 0
        return self.true_positive / (self.true_positive + self.false_negative)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YOLOTracker()
    window.show()
    sys.exit(app.exec_())
