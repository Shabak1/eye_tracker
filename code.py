import tkinter as tk
from tkinter import messagebox
import cv2
import pickle
import os

filename = "C:/Users/Бобырев Роман/Desktop/data.conf"
# Функция для загрузки данных пользователей
def load_user_data(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)
    return {}

# Функция для сохранения данных пользователей
def save_user_data(filename, data):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

# Функция для проверки данных пользователя
def login(username, password, user_data):
    return username in user_data and user_data[username] == password

# Функция для создания нового пользователя
def create_user(username, password, user_data):
    user_data[username] = password
    save_user_data("C:/Users/Бобырев Роман/Desktop/data.conf", user_data)
    messagebox.showinfo("Регистрация", "Пользователь успешно создан")

# Функция для отображения видео с веб-камеры
def show_camera():
    cap = cv2.VideoCapture(1)
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Camera', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()

# Функция для авторизации пользователя
def attempt_login():
    user_data = load_user_data("C:/Users/Бобырев Роман/Desktop/data.conf")
    if login(entry_username.get(), entry_password.get(), user_data):
        messagebox.Message("Вход выполнен успешно")
        # show_camera()
    else:
        messagebox.showerror("Ошибка входа", "Неверное имя пользователя или пароль")


def open_create_user_window():
    user_data = load_user_data('C:/Users/Бобырев Роман/Desktop/data.conf')
    

    # Создание нового окна для регистрации пользователя
    register_window = tk.Toplevel(root)
    register_window.title("Регистрация пользователя")

    # Создание метки и поля ввода для имени пользователя
    label_new_username = tk.Label(register_window, text="Новое имя пользователя:")
    label_new_username.pack()
    entry_new_username = tk.Entry(register_window)
    entry_new_username.pack()

    # Создание метки и поля ввода для пароля
    label_new_password = tk.Label(register_window, text="Новый пароль:")
    label_new_password.pack()
    entry_new_password = tk.Entry(register_window, show="*")
    entry_new_password.pack()

    # Создание кнопки для подтверждения регистрации
    button_confirm_registration = tk.Button(register_window, text="Зарегистрироваться", command=lambda: create_user(entry_new_username.get(), entry_new_password.get(), user_data))
    button_confirm_registration.pack()
    

# Создание основного окна
root = tk.Tk()
root.title("Окно авторизации")
root.geometry("600x450")  # Установка размеров окна

# Создание метки и поля ввода для имени пользователя
label_username = tk.Label(root, text="Имя пользователя:")
label_username.pack()
entry_username = tk.Entry(root)
entry_username.pack()

# Создание метки и поля ввода для пароля
label_password = tk.Label(root, text="Пароль:")
label_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

# Создание кнопки для входа
button_login = tk.Button(root, text="Войти", command=attempt_login)
button_login.pack()

# Создание кнопки, которая откроет окно создания нового пользователя
button_open_create_user_window = tk.Button(root, text="Создать нового пользователя", command=open_create_user_window)
button_open_create_user_window.pack()

root.mainloop()
