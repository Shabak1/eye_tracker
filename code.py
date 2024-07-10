import cv2
import numpy as np
import os
import json
import serial
from PyQt5 import QtWidgets, QtGui, QtCore

# Путь к файлу с настройками пользователей
SETTINGS_FILE = "Путь к файлу"

# Подключение к Arduino
ser = serial.Serial('COM3', 9600)  # Нужно убедиться, что COM-порт и скорость совпадают с подключением Arduino

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Управление электроколяской")
        self.setGeometry(100, 100, 800, 600)
        
        self.login_widget = LoginWidget(self)
        self.setCentralWidget(self.login_widget)

    def start_control(self, username):
        self.control_widget = ControlWidget(self, username)
        self.setCentralWidget(self.control_widget)

class LoginWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(LoginWidget, self).__init__(parent)
        self.parent = parent

        self.layout = QtWidgets.QVBoxLayout(self)

        self.username_label = QtWidgets.QLabel("Имя пользователя:")
        self.layout.addWidget(self.username_label)

        self.username_input = QtWidgets.QLineEdit()
        self.layout.addWidget(self.username_input)

        self.login_button = QtWidgets.QPushButton("Войти")
        self.login_button.clicked.connect(self.login)
        self.layout.addWidget(self.login_button)

        self.new_user_button = QtWidgets.QPushButton("Создать нового пользователя")
        self.new_user_button.clicked.connect(self.create_new_user)
        self.layout.addWidget(self.new_user_button)

    def login(self):
        username = self.username_input.text()
        if self.validate_user(username):
            self.parent.start_control(username)
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пользователь не найден")

    def create_new_user(self):
        username = self.username_input.text()
        if not self.validate_user(username):
            self.save_user(username)
            QtWidgets.QMessageBox.information(self, "Успех", "Пользователь создан")
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Пользователь уже существует")

    def validate_user(self, username):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                users = json.load(f)
            return username in users
        return False

    def save_user(self, username):
        users = {}
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                users = json.load(f)
        users[username] = {}
        with open(SETTINGS_FILE, "w") as f:
            json.dump(users, f)

class ControlWidget(QtWidgets.QWidget):
    def __init__(self, parent, username):
        super(ControlWidget, self).__init__(parent)
        self.parent = parent
        self.username = username

        self.layout = QtWidgets.QVBoxLayout(self)
        self.video_label = QtWidgets.QLabel()
        self.layout.addWidget(self.video_label)

        self.cap = cv2.VideoCapture(0)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = self.process_frame(frame)
            image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QtGui.QImage.Format_BGR888)
            self.video_label.setPixmap(QtGui.QPixmap.fromImage(image))

    def process_frame(self, frame):
        height, width, _ = frame.shape
        mid_h = height // 2
        mid_w = width // 2

        # Это место для интеграции айтрекера, который должен определить координаты взгляда (x, y)
        gaze_x, gaze_y = self.get_gaze_coordinates()

        if gaze_x < mid_w / 2:
            self.move_left()
        elif gaze_x > 3 * mid_w / 2:
            self.move_right()
        elif gaze_y < mid_h / 2:
            self.move_forward()
        elif gaze_y > 3 * mid_h / 2:
            self.move_backward()

        return frame

    def get_gaze_coordinates(self):
        # Возвращаем фиктивные координаты для примера
        return 400, 300

    def move_forward(self):
        # Команда для движения вперед
        ser.write(b'F')

    def move_backward(self):
        # Команда для движения назад
        ser.write(b'B')

    def move_left(self):
        # Команда для поворота налево
        ser.write(b'L')

    def move_right(self):
        # Команда для поворота направо
        ser.write(b'R')

    def stop_motors(self):
        # Команда для остановки моторов
        ser.write(b'S')

app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec_()
