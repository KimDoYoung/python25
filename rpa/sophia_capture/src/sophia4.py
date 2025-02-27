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
    """ (요구사항 3) Rubber Band (점선 사각형) 구현 """
    def __init__(self, parent=None):
        print("SophiaCapture Initialized")  # 프로그램이 실행되었는지 확인
        super().__init__(parent)
        self.setMouseTracking(True)  # (요구사항 1) 마우스 이동 감지
        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)  
        self.start_pos = None
        self.parent_window = parent  
        self.setWindowTitle("SophiaCapture")
        self.is_first_show = True        


    def mouseMoveEvent(self, event):
        """ (요구사항 1) 이미지가 로드된 경우에만 마우스 위치 업데이트 """
        if self.parent_window.image is None:
            return  # 이미지가 없으면 업데이트 안 함

        # 마우스 좌표를 이미지 내부 좌표로 변환
        x = event.x()
        y = event.y()

        # 이미지 영역 내에 있을 때만 부모 윈도우에 좌표 전달
        if 0 <= x < self.pixmap().width() and 0 <= y < self.pixmap().height():
            self.parent_window.update_mouse_position(x, y)
        if self.rubber_band.isVisible():
            self.rubber_band.setGeometry(QRect(self.start_pos, event.pos()).normalized())

    def mousePressEvent(self, event):
        """ (요구사항 3) Rectangle Capture / Image Capture 시 마우스 클릭 시작 """
        if event.button() == Qt.LeftButton and (self.parent_window.rect_capture_mode or self.parent_window.image_capture_mode):
            self.start_pos = event.pos()
            self.rubber_band.setGeometry(QRect(self.start_pos, self.start_pos))  
            self.rubber_band.show()

    def mouseReleaseEvent(self, event):
        """ (요구사항 3, 4) 마우스 드래그 후 선택된 영역 처리 """
        if event.button() == Qt.LeftButton and self.start_pos and (self.parent_window.rect_capture_mode or self.parent_window.image_capture_mode):
            end_pos = event.pos()
            selected_rect = QRect(self.start_pos, end_pos).normalized()
            self.parent_window.process_selection(selected_rect)  
            self.rubber_band.hide()


class SophiaCapture(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SophiaCapture")

        # (요구사항 1) 프로그램 실행 시 최대화 (showEvent에서 처리)
        self.is_first_show = True

        # (요구사항 2) 메뉴바 설정
        self.menu = self.menuBar()
        file_menu = self.menu.addMenu("File")
        
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_image)
        file_menu.addAction(open_action)

        quit_action = QAction("Quit", self)
        quit_action.setShortcut("Alt+F4")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # (요구사항 2) 툴바 설정
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

        # (요구사항 2) 중앙 레이아웃 설정
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout(self.central_widget)  # 좌우 배치

        # (요구사항 2) 이미지 뷰어
        self.image_label = CustomLabel(self)  
        self.image_label.setAlignment(Qt.AlignCenter)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setWidgetResizable(True)

        # (요구사항 6, 7) 정보 표시 영역 (사용자 입력 가능)
        self.info_text = QTextEdit()
        self.info_text.setFixedWidth(600)  
        self.info_text.setFont(QFont("Arial", 16))  

        # (요구사항 2) 가변적인 7:3 비율 유지
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.scroll_area)
        self.splitter.addWidget(self.info_text)
        self.splitter.setSizes([840, 600])  

        main_layout.addWidget(self.splitter)

        # (요구사항 1, 2) Status Bar 설정 (Zoom Factor 추가)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.mouse_pos_label = QLabel("X: 0, Y: 0 | Zoom: x1.0")
        self.mouse_pos_label.setAlignment(Qt.AlignCenter)
        self.status_label = QLabel("")
        self.message_label = QLabel("Ready")

        self.status_bar.addWidget(self.mouse_pos_label, 2)
        self.status_bar.addWidget(self.status_label, 1)
        self.status_bar.addWidget(self.message_label, 3)

        # 이미지 관련 변수
        self.image = None
        self.pixmap = None
        self.scale_factor = 1.0
        self.rect_capture_mode = False
        self.image_capture_mode = False
        self.captured_images_count = 0

    def showEvent(self, event):
        """ (요구사항 1) 프로그램 시작 시 최대화 """
        if self.is_first_show:
            self.showMaximized()
            self.is_first_show = False

    def toggle_rectangle_capture(self):
        """ Rectangle Capture 모드 ON/OFF (Image Capture가 켜져 있으면 끔) """
        self.rect_capture_mode = not self.rect_capture_mode
        if self.rect_capture_mode:
            self.image_capture_mode = False  # Image Capture OFF
            self.image_capture_btn.setChecked(False)  # 버튼 UI 동기화

        self.rect_capture_btn.setChecked(self.rect_capture_mode)  # 현재 상태 반영
        self.status_label.setText("Rectangle Capture ON" if self.rect_capture_mode else "")

    def toggle_image_capture(self):
        """ Image Capture 모드 ON/OFF (Rectangle Capture가 켜져 있으면 끔) """
        self.image_capture_mode = not self.image_capture_mode
        if self.image_capture_mode:
            self.rect_capture_mode = False  # Rectangle Capture OFF
            self.rect_capture_btn.setChecked(False)  # 버튼 UI 동기화

        self.image_capture_btn.setChecked(self.image_capture_mode)  # 현재 상태 반영
        self.status_label.setText("Image Capture ON" if self.image_capture_mode else "")


    def process_selection(self, rect):
        """ (요구사항 2) 선택된 영역을 2가지 방식으로 표현 """
        x, y, w, h = rect.left(), rect.top(), rect.width(), rect.height()

        if self.image_capture_mode:
            save_path = f"image_{self.captured_images_count}.png"
            cv2.imwrite(save_path, self.image[y:y+h, x:x+w])
            self.captured_images_count += 1
            self.info_text.append("-----> ")
            self.info_text.append(f"{save_path} saved")
        elif self.rect_capture_mode:
            self.info_text.append("-----> ")
            self.info_text.append(f"rect: ({rect.left()}, {rect.top()}) - ({rect.right()}, {rect.bottom()})")
            self.info_text.append(f"region: ({x}, {y}, {w}, {h})")

    def open_image(self):
        """ (요구사항 2) 이미지 파일 열기 """
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Images (*.png *.jpg *.bmp)")
        if file_name:
            self.image = cv2.imread(file_name)
            self.display_image()

    def zoom_in(self):
        """ (요구사항 2) 이미지 확대 """
        self.scale_factor *= 1.2
        self.display_image()

    def reset_zoom(self):
        """ (요구사항 2) 이미지 원래 크기로 복원 """
        self.scale_factor = 1.0
        self.display_image()

    def display_image(self):
        """ (요구사항 2) 이미지 표시 (이미지가 없을 경우 실행 안 함) """
        if self.image is None:
            return  # 이미지가 없으면 실행하지 않음
        
        h, w, ch = self.image.shape
        bytes_per_line = ch * w
        qt_image = QImage(self.image.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        self.pixmap = QPixmap.fromImage(qt_image)
        self.image_label.setPixmap(self.pixmap.scaled(self.pixmap.size() * self.scale_factor, Qt.KeepAspectRatio))

    def update_mouse_position(self, x, y):
        """ (요구사항 1) 마우스 좌표 + Zoom Factor 업데이트 """
        self.mouse_pos_label.setText(f"X: {x}, Y: {y} | Zoom: x{self.scale_factor:.1f}")


if __name__ == "__main__":
    print("Starting SophiaCapture...")  # 프로그램 시작 확인

    app = QApplication(sys.argv)
    print("QApplication initialized.")  # QApplication 생성 확인

    try:
        editor = SophiaCapture()
        print("SophiaCapture instance created.")  # SophiaCapture 인스턴스 생성 확인

        editor.show()
        print("SophiaCapture window shown.")  # SophiaCapture UI 표시 확인

        sys.exit(app.exec_())  # 이벤트 루프 실행
    except Exception as e:
        print(f"Error: {e}")  # 예외 발생 시 출력
