import sys
import os
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QFileDialog, 
                             QScrollArea, QVBoxLayout, QWidget, QToolBar, QPushButton, 
                             QTextEdit, QAction, QStatusBar, QHBoxLayout, QSplitter, QRubberBand)
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtCore import Qt, QRect, QPoint


class CustomLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)  # 마우스 이동 감지 활성화
        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)  # 점선 사각형
        self.start_pos = None
        self.parent_window = parent  # 부모 윈도우(MainWindow)

    def mouseMoveEvent(self, event):
        x, y = event.x(), event.y()
        if self.parent_window:
            self.parent_window.update_mouse_position(x, y)  # 마우스 좌표 업데이트

        if self.rubber_band.isVisible():
            self.rubber_band.setGeometry(QRect(self.start_pos, event.pos()).normalized())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and (self.parent_window.rect_capture_mode or self.parent_window.image_capture_mode):
            self.start_pos = event.pos()
            self.rubber_band.setGeometry(QRect(self.start_pos, self.start_pos))  # 초기 크기 설정
            self.rubber_band.show()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.start_pos and (self.parent_window.rect_capture_mode or self.parent_window.image_capture_mode):
            end_pos = event.pos()
            selected_rect = QRect(self.start_pos, end_pos).normalized()
            self.parent_window.process_selection(selected_rect)  # 선택 영역 처리
            self.rubber_band.hide()


class SophiaCapture(QMainWindow):
    def __init__(self):
        super().__init__()

        # **✅ 초기 실행 시 최대화**
        self.setWindowTitle("SophiaCapture")
        self.showMaximized()

        # 메뉴바 추가
        self.menu = self.menuBar()
        file_menu = self.menu.addMenu("File")
        
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_image)
        file_menu.addAction(open_action)

        quit_action = QAction("Quit", self)
        quit_action.setShortcut("Alt+F4")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # 툴바 추가
        self.toolbar = QToolBar("Toolbar")
        self.addToolBar(self.toolbar)

        self.zoom_in_btn = QPushButton("Zoom In")
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        self.toolbar.addWidget(self.zoom_in_btn)

        self.reset_zoom_btn = QPushButton("1:1")
        self.reset_zoom_btn.clicked.connect(self.reset_zoom)
        self.toolbar.addWidget(self.reset_zoom_btn)

        self.rect_capture_btn = QPushButton("Rectangle Capture")
        self.rect_capture_btn.setCheckable(True)
        self.rect_capture_btn.clicked.connect(self.toggle_rectangle_capture)
        self.toolbar.addWidget(self.rect_capture_btn)

        self.image_capture_btn = QPushButton("Image Capture")
        self.image_capture_btn.setCheckable(True)
        self.image_capture_btn.clicked.connect(self.toggle_image_capture)
        self.toolbar.addWidget(self.image_capture_btn)

        # 중앙 레이아웃 설정
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout(self.central_widget)  # 좌우 배치

        # **이미지 뷰어 영역 (7)**
        self.image_label = CustomLabel(self)  # CustomLabel 사용
        self.image_label.setAlignment(Qt.AlignCenter)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setWidgetResizable(True)

        # **정보 표시 영역 (2배 증가)**
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setFixedWidth(600)  # 기존보다 2배 증가
        self.info_text.setFont(QFont("Arial", 14))  # ✅ **정보 영역 글꼴 크기 증가**

        # **Splitter를 이용해 가변적인 7:3 비율 유지**
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.scroll_area)
        self.splitter.addWidget(self.info_text)
        self.splitter.setSizes([840, 600])  # 7:3 비율로 초기 크기 설정

        main_layout.addWidget(self.splitter)

        # **Status Bar (3분할)**
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.mouse_pos_label = QLabel("X: 0, Y: 0")
        self.status_label = QLabel("")
        self.message_label = QLabel("Ready")

        self.status_bar.addWidget(self.mouse_pos_label, 1)
        self.status_bar.addWidget(self.status_label, 1)
        self.status_bar.addWidget(self.message_label, 3)

        # 이미지 관련 변수
        self.image = None
        self.pixmap = None
        self.scale_factor = 1.0
        self.rect_capture_mode = False
        self.image_capture_mode = False
        self.captured_images_count = 0

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp)")
        if file_name:
            self.image = cv2.imread(file_name)
            self.display_image()

    def display_image(self):
        if self.image is not None:
            h, w, ch = self.image.shape
            bytes_per_line = ch * w
            qt_image = QImage(self.image.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
            self.pixmap = QPixmap.fromImage(qt_image)
            self.image_label.setPixmap(self.pixmap.scaled(self.pixmap.size() * self.scale_factor, Qt.KeepAspectRatio))

    def zoom_in(self):
        self.scale_factor *= 1.2
        self.display_image()

    def reset_zoom(self):
        self.scale_factor = 1.0
        self.display_image()

    def toggle_rectangle_capture(self):
        self.rect_capture_mode = not self.rect_capture_mode
        if self.rect_capture_mode:
            self.image_capture_mode = False
        self.status_label.setText("Rectangle Capture ON" if self.rect_capture_mode else "")

    def toggle_image_capture(self):
        self.image_capture_mode = not self.image_capture_mode
        if self.image_capture_mode:
            self.rect_capture_mode = False
        self.status_label.setText("Image Capture ON" if self.image_capture_mode else "")

    def update_mouse_position(self, x, y):
        self.mouse_pos_label.setText(f"X: {x}, Y: {y}")

    def process_selection(self, rect):
        if self.image is None:
            return

        if self.image_capture_mode:
            cropped_image = self.image[rect.top():rect.bottom(), rect.left():rect.right()]
            save_path = f"image_{self.captured_images_count}.png"
            cv2.imwrite(save_path, cropped_image)
            self.captured_images_count += 1
            self.info_text.append(f"{save_path} saved")  # ✅ 저장된 이미지 정보 표시

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = SophiaCapture()
    editor.show()
    sys.exit(app.exec_())
