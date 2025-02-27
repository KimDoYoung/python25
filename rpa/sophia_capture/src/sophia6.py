import sys
import os
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QFileDialog, 
                             QScrollArea, QVBoxLayout, QWidget, QToolBar, QPushButton, 
                             QTextEdit, QAction, QStatusBar, QHBoxLayout, QSplitter, QRubberBand, QSizePolicy, QMessageBox)
from PyQt5.QtGui import QPixmap, QImage, QFont, QIcon
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtCore import QSize


class CustomLabel(QLabel):
    """ (요구사항 3) Rubber Band (점선 사각형) 구현 """
    def __init__(self, parent=None):
        print("SophiaCapture Initialized")  # 프로그램이 실행되었는지 확인
        super().__init__(parent)
        self.setMouseTracking(True)  # (요구사항 1) 마우스 이동 감지
        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)  
        self.rubber_band.setStyleSheet("border: 2px dashed red; background: rgba(255, 0, 0, 50);")  # ✅ 반투명 효과 추가
        self.start_pos = None
        self.parent_window = parent  

        # ✅ 디버깅 추가 (parent_window가 SophiaCapture인지 확인)
        if not hasattr(self.parent_window, "original_image"):
            print("Error: parent_window does not have 'original_image'")

    def mouseMoveEvent(self, event):
        """ 마우스 이동 시 Rubber Band 크기 조정 (Zoom Factor 반영) """
        if self.parent_window.original_image is None:
            return

        label_x = event.x()
        label_y = event.y()

        # ✅ QLabel 내부에서만 마우스 좌표 제한 (초과 방지)
        label_rect = self.rect()
        label_x = max(0, min(label_x, label_rect.width() - 1))
        label_y = max(0, min(label_y, label_rect.height() - 1))

        image_x = int(label_x / self.parent_window.scale_factor)
        image_y = int(label_y / self.parent_window.scale_factor)

        if 0 <= image_x < self.parent_window.original_image.shape[1] and 0 <= image_y < self.parent_window.original_image.shape[0]:
            self.parent_window.update_mouse_position(image_x, image_y)

        # ✅ Rubber Band 크기 조정
        if self.rubber_band.isVisible():
            self.rubber_band.setGeometry(QRect(self.start_pos, QPoint(label_x, label_y)).normalized())

    def mousePressEvent(self, event):
        """ Rectangle Capture / Image Capture 시 마우스 클릭 시작 (Rubber Band 위치 보정) """
        if event.button() == Qt.LeftButton and (self.parent_window.rect_capture_mode or self.parent_window.image_capture_mode):
            self.start_pos = event.pos()

            # ✅ QLabel 내부에서 Rubber Band가 생성되도록 위치 보정
            label_rect = self.rect()  # QLabel의 크기 가져오기
            self.start_pos.setX(max(0, min(self.start_pos.x(), label_rect.width() - 1)))
            self.start_pos.setY(max(0, min(self.start_pos.y(), label_rect.height() - 1)))

            self.rubber_band.setGeometry(QRect(self.start_pos, QSize(1, 1)))  # ✅ 초기 크기 설정
            self.rubber_band.show()
            self.rubber_band.update()  # ✅ 즉시 갱신

    def mouseReleaseEvent(self, event):
        """ 마우스 드래그 후 선택된 영역 처리 (Rubber Band 위치 보정) """
        if event.button() == Qt.LeftButton and self.start_pos and (self.parent_window.rect_capture_mode or self.parent_window.image_capture_mode):
            end_pos = event.pos()

            # ✅ QLabel 내부에서만 마우스 좌표 제한 (초과 방지)
            label_rect = self.rect()
            end_pos.setX(max(0, min(end_pos.x(), label_rect.width() - 1)))
            end_pos.setY(max(0, min(end_pos.y(), label_rect.height() - 1)))

            selected_rect = QRect(self.start_pos, end_pos).normalized()
            self.parent_window.process_selection(selected_rect)

            self.rubber_band.hide()
            self.rubber_band.update()  # ✅ 즉시 갱신


class SophiaCapture(QMainWindow):
    def __init__(self):
        super().__init__()

        # 이미지 관련 변수
        self.original_image = None  # 원본 이미지
        self.displayed_image = None  # 확대/축소용 이미지
        self.scale_factor = 1.0


        self.setWindowTitle("Sophia Capture")

        base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일(sophia.py)의 절대 경로
        icon_path = os.path.join(base_dir, "sophia_capture.ico")  # 절대 경로로 변경        
        
        # ✅ 아이콘 파일이 존재하는지 확인
        if not os.path.exists(icon_path):
            print(f"Error: Icon file not found: {icon_path}")
        else:
            print(f"Icon Loaded: {icon_path}")        
        self.setWindowIcon(QIcon(icon_path))  # 같은 폴더에 있는 ico 파일 사용

        # (요구사항 1) 프로그램 실행 시 최대화 (showEvent에서 처리)
        self.is_first_show = True

        
        # ✅ 메뉴바 설정
        self.menu = self.menuBar()
        file_menu = self.menu.addMenu("File")
        
        # ✅ Open 메뉴 (Ctrl+O 핫키 추가)
        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")  # ✅ Ctrl+O 단축키 추가
        open_action.triggered.connect(self.open_image)
        file_menu.addAction(open_action)

        # ✅ About 메뉴 추가
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_popup)
        file_menu.addAction(about_action)

        # ✅ Separator(구분선) 추가
        file_menu.addSeparator()

        # ✅ Quit 메뉴 추가 (Alt+F4 그대로 유지)
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
        # self.image_label = CustomLabel(self)  
        # self.image_label.setAlignment(Qt.AlignCenter)
        # self.scroll_area = QScrollArea()
        # self.scroll_area.setWidget(self.image_label)
        # self.scroll_area.setWidgetResizable(True)

        self.image_label = CustomLabel(self)
        self.image_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)  # ✅ 좌측 상단 고정
        self.image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # ✅ 크기 자동 변경 방지

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.image_label)
        self.scroll_area.setWidgetResizable(False)  # ✅ QLabel 크기가 자동 변경되지 않도록 설정



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
        """ 선택된 영역을 원본 이미지 좌표로 변환 후 저장 """
        if self.original_image is None:
            print("Error: original_image is None")  # 디버깅 추가
            return  

        # 화면 좌표 → 원본 좌표 변환
        x = int(rect.left() / self.scale_factor)
        y = int(rect.top() / self.scale_factor)
        w = int(rect.width() / self.scale_factor)
        h = int(rect.height() / self.scale_factor)

        # 원본 이미지 기준으로 좌표 확인
        h_img, w_img, _ = self.original_image.shape
        if x < 0 or y < 0 or x + w > w_img or y + h > h_img:
            print("Error: Selection out of bounds")  # 선택 영역이 이미지 범위를 초과하는 경우
            return

        if self.image_capture_mode:
            save_path = os.path.join(self.save_folder, f"image_{self.captured_images_count}.png")
            cropped = self.original_image[y:y+h, x:x+w]  # ✅ 원본 이미지에서 정확한 영역 잘라내기
            cv2.imwrite(save_path, cropped)
            self.captured_images_count += 1
            self.info_text.append("-----> ")
            self.info_text.append(f"{save_path} saved")
        elif self.rect_capture_mode:
            self.info_text.append("-----> ")
            self.info_text.append(f"rect: ({rect.left()}, {rect.top()}) - ({rect.right()}, {rect.bottom()})")
            self.info_text.append(f"region: ({x}, {y}, {w}, {h})")

    def open_image(self):
        """ 이미지 파일 열기 (원본 보관 & 복제본 생성) """
        """ 파일 열기 대화상자 (기본 폴더: $HOME\사진) """
        home_path = os.path.expanduser("~")  # ✅ 사용자 홈 디렉터리
        default_folder = os.path.join(home_path, "사진")  # ✅ $HOME\사진 폴더 설정        
        # ✅ 만약 "사진" 폴더가 없으면 "Pictures" 폴더 사용
        if not os.path.exists(default_folder):
            default_folder = os.path.join(home_path, "Pictures")

        base_folder = os.path.join(default_folder, "SophiaCapture")  # ✅ 기본 폴더 설정
        os.makedirs(base_folder, exist_ok=True)  # ✅ 기본 폴더 생성 (없으면 생성)
        # 파일 열기 대화상자 실행 (기본 폴더 설정)
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", default_folder, "Images (*.png *.jpg *.bmp)")    
    
        if not file_name:
            print("Warning: No file selected")  # 파일 선택 안 한 경우
            return
        image_array = np.fromfile(file_name, dtype=np.uint8)
        self.original_image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        # self.original_image = cv2.imread(file_name)
        if self.original_image is None:
            print(f"Error: Failed to load image {file_name}")  # 이미지 로드 실패 확인
            return

        print(f"Image loaded: {file_name}, Size: {self.original_image.shape[1]}x{self.original_image.shape[0]}")  # 정상 로드 확인
        self.displayed_image = self.original_image.copy()  # 화면 표시용 복제본 생성
        self.scale_factor = 1.0  # 화면 표시용 이미지 크기 비율 초기화
        self.display_image()

        # ✅ 창 제목 업데이트 (Full Path 표시)
        self.setWindowTitle(f"Sophia Capture - {file_name}")

        # ✅ 이미지 파일명 추출 후 폴더 생성
        image_basename = os.path.basename(file_name)  # 파일명 (abc.png)
        image_name, _ = os.path.splitext(image_basename)  # 확장자 제거 (abc)
        self.save_folder = os.path.join(base_folder, image_name)  # 저장 폴더 경로
        os.makedirs(self.save_folder, exist_ok=True)  # ✅ 폴더 생성 (있으면 skip)

        # ✅ 캡처 이미지 번호 초기화 (0번부터 시작)
        self.captured_images_count = 0

        # ✅ 상태바(StatusBar) 마지막 레이블을 저장 폴더로 업데이트
        self.message_label.setText(self.save_folder)

        self.display_image()


    def reset_zoom(self):
        """ 이미지 원래 크기로 복원 """
        if self.original_image is None:
            return
        self.scale_factor = 1.0
        self.display_image()

    def zoom_in(self):
        """ 이미지 확대 (QLabel 크기 업데이트 포함) """
        if self.original_image is None:
            print("Error: zoom_in() called but original_image is None")
            return

        self.scale_factor *= 1.2
        print(f"Zoom In: New Scale Factor = {self.scale_factor}")

        self.display_image()

        # ✅ QPixmap이 존재할 때만 QLabel 크기 조정
        if not self.pixmap.isNull():
            new_size = self.pixmap.size()
            self.image_label.resize(new_size)
            print(f"Zoom In: QLabel New Size = {new_size.width()}x{new_size.height()}")

        self.scroll_area.setWidgetResizable(False)
        self.scroll_area.update()


    def display_image(self):
        """ 확대/축소 적용하여 이미지 표시 (QPixmap 변환 오류 수정) """
        if self.original_image is None:
            print("Error: display_image() called but original_image is None")
            return

        h, w, ch = self.original_image.shape
        new_w = int(w * self.scale_factor)
        new_h = int(h * self.scale_factor)

        # ✅ 새로운 크기가 0이 되지 않도록 보정
        if new_w < 1:
            new_w = 1
        if new_h < 1:
            new_h = 1

        print(f"Resizing Image to: {new_w}x{new_h}")

        # ✅ cv2.resize() 수행 (INTER_LANCZOS4 사용)
        resized = cv2.resize(self.original_image, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
        self.displayed_image = resized  # 화면 표시용 이미지 업데이트

        bytes_per_line = ch * new_w
        qt_image = QImage(resized.data, new_w, new_h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        self.pixmap = QPixmap.fromImage(qt_image)

        # ✅ QPixmap 변환이 실패한 경우 로그 출력
        if self.pixmap.isNull():
            print("Error: QPixmap conversion failed!")
            return  # 변환 실패 시 함수 종료

        print(f"Pixmap Created: {self.pixmap.width()}x{self.pixmap.height()}")

        self.image_label.setPixmap(self.pixmap)

        # ✅ QLabel 크기를 Pixmap 크기로 설정
        self.image_label.resize(self.pixmap.size())
        print(f"QLabel New Size: {self.image_label.width()}x{self.image_label.height()}")

        # ✅ QScrollArea 업데이트
        self.scroll_area.setWidgetResizable(False)
        self.scroll_area.update()



    def update_mouse_position(self, x, y):
        """ (요구사항 1) 마우스 좌표 + Zoom Factor 업데이트 """
        self.mouse_pos_label.setText(f"X: {x}, Y: {y} | Zoom: x{self.scale_factor:.1f}")


    def show_about_popup(self):
        """ About 창을 표시하는 함수 """
        msg = QMessageBox(self)
        msg.setWindowTitle("About SophiaCapture")
        msg.setText("SophiaCapture v1.0\n\n이미지 캡처 및 편집 도구\n\n© 2024 SophiaCapture Team")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)

        # ✅ 중앙 정렬
        msg.setStyleSheet("QLabel{ text-align: center; }")  
        msg.exec_()

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
