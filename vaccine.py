import re
import sys
import os
import pandas as pd
import traceback
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QMessageBox, QDesktopWidget, QLineEdit, QTableWidget, QTableWidgetItem, QComboBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtCore, QtGui, QtWidgets
from path import *
import datetime
from icon import vacina
from reqs import *


class RegisterVacWIndow(QWidget):
    registered_vac_signal = QtCore.pyqtSignal()

    def __init__(self, username, password, vac_df):
        super().__init__()
        self.activateWindow()
        loadUi(register_vac_path, self)
        self.vac_df = vac_df
        self.username = username
        self.password = password
        self.connect_buttons()
        self.configure_ui()

    def update_user_vac_table(self):
        self.registered_vac_signal.emit()

    def configure_ui(self):
        self.setWindowTitle("Registrar vacina")
        self.setWindowIcon(QtGui.QIcon("icon/vacina.png"))
        self.combo_vac.addItems(self.vac_df['name'].to_list())
        # self.combo_vac.addItems(vac_df[])

    def connect_buttons(self):
        self.button_register_vac.clicked.connect(self.register_vac)

    def register_vac(self):
        vac_name = self.combo_vac.currentText()
        vac_id = self.vac_df.query(f"name == '{vac_name}'")['vac_id'].item()
        date = self.line_vac_date.text()
        successful_register = register_vac(user_info=(self.username, self.password), vac_info={"vac_id": vac_id, "date_taken": date}).status_code
        if successful_register == 200:
            self.registered_vac_signal.emit()
        else:
            notification_message("Registro de vacina", "Não foi possível registrar vacina, tente novamente")

    def display_info(self):
        try:
            self.setWindowModality(Qt.ApplicationModal)
            self.setFocus()
            self.show()

        except:
            print(traceback.format_exc())


class ChangePasswordWindow(QWidget):
    teste_signal = QtCore.pyqtSignal(str)

    def __init__(self, username, password):
        super().__init__()
        self.activateWindow()
        loadUi(change_password_window_path, self)
        self.username = username
        self.password = password
        self.connect_buttons()
        self.line_current_password.setText("")
        self.line_current_password.focusWidget()
        self.line_current_password.setFocus()
        self.configure_ui()

    def emit_updated_password(self):
        self.teste_signal.emit(self.password)

    def configure_ui(self):
        self.setWindowTitle("Alterar senha")
        self.setWindowIcon(QtGui.QIcon("icon/vacina.png"))
        self.line_current_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.line_new_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.line_confirm_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.line_current_password.setFocus()

    def check_password(self):
        current_password = self.line_current_password.text()
        new_password = self.line_new_password.text()
        confirm_password = self.line_confirm_password.text()

        if current_password != self.password:
            error_message("senha", "Senha atual inválida")
            return False

        elif current_password == new_password:
            error_message("senha", "Senha atual igual a nova senha")
            return False

        elif " " in new_password or new_password == "":
            error_message("senha", "Senha inválida")
            return False

        elif new_password != confirm_password:
            error_message("senha", "Nova senha diferente da confirmação")
            return False

        return True

    def change_password(self):
        new_password = self.line_new_password.text()
        valid_password = self.check_password()

        if valid_password is True:
            update_response = update_password(self.username,self.password,new_password)
            if update_response.ok:
                notification_message("alteração", "Senha alterada com sucesso")
                self.password = new_password
                self.emit_updated_password()
            else:
                error_message("erro", "Não foi possível alterar a senha, tente novamente")

    def connect_buttons(self):
        self.button_cancel.clicked.connect(self.close)
        self.button_change.clicked.connect(self.change_password)

    def display_info(self):
        try:
            self.setWindowModality(Qt.ApplicationModal)
            self.setFocus()
            self.show()

        except:
            print(traceback.format_exc())


class RegisterForm(QWidget):
    def __init__(self):
        super().__init__()
        loadUi(register_form_path, self)
        self.connect_buttons()
        self.setWindowTitle("Cadastrar usuário")
        self.setWindowIcon(QtGui.QIcon("icon/vacina.png"))
        self.line_register_password.setEchoMode(QtWidgets.QLineEdit.Password)

    def connect_buttons(self):
        self.button_cancel.clicked.connect(self.close)
        self.button_register.clicked.connect(self.register_user)

    def display_info(self):
        self.setWindowModality(Qt.ApplicationModal)
        self.setFocus()
        self.show()

    def check_user(self):
        username = self.line_register_username.text().lower()
        if username == "" or not username.isalnum():
            return False
        self.username = username
        return True

    def check_name(self):
        name = self.line_register_name.text()
        if name == "" or not name.replace(" ", "").isalpha():
            return False
        formatted_name = [name.capitalize() for name in name.split()]
        formatted_name = " ".join(formatted_name)
        self.name = formatted_name
        return True

    def check_birth(self):
        birth = self.line_register_birth.text()
        try:
            datetime.datetime.strptime(birth, '%Y-%m-%d')
        except ValueError:
            return False
        self.birth = birth
        return True

    def check_email(self):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email = self.line_register_email.text()
        if not re.fullmatch(regex, email):
            return False
        self.email = email
        return True

    def check_password(self):
        password = self.line_register_password.text()
        if " " in password or password == "":
            return False
        self.password = password
        return True

    def check_entries(self):
        user = self.check_user()
        name = self.check_name()
        birth = self.check_birth()
        email = self.check_email()
        password = self.check_password()

        if user is False:
            error_message("usuário", "Usuário inválido")
            return

        elif name is False:
            error_message("nome", "Nome inválido")
            return

        elif birth is False:
            error_message("nascimento", "Data de nascimento inválida")
            return

        elif email is False:
            error_message("email", "Email inválido")
            return

        elif password is False:
            error_message("senha", "Senha inválida")
            return

        else:
            return True

    def register_user(self):
        try:
            valid_input = self.check_entries()
            if valid_input is True:
                user_info ={
                    "username": self.username,
                    "name": self.name,
                    "birth": self.birth,
                    "email": self.email,
                    "password": self.password
                }
                register_response = register_user(user_info).text
                self.check_register(register_response)

        except:
            print(traceback.format_exc())

    def check_register(self, registered):
        try:
            email_error = "constraint failed: UNIQUE constraint failed: users.email"
            user_error = "constraint failed: UNIQUE constraint failed: users.username"

            if email_error in registered:
                error_message("email", "Email já existe")
                return

            if user_error in registered:
                error_message("user", "Usuário já existe")
                return

            confirmation = notification_message("Cadastro", "Usuario cadastrado com sucesso")
            if confirmation == QMessageBox.Ok:
                del self.username
                del self.name
                del self.email
                del self.birth
                del self.password
                self.close()

        except:
            print(traceback.format_exc())


class LoginForm(QWidget):
    def __init__(self):
        global user
        try:
            super().__init__()
            loadUi(login_form_path, self)

            user = user if user != "None" else ""
            self.setWindowTitle("Login")
            self.setWindowIcon(QtGui.QIcon("icon/vacina.png"))
            self.button_login.clicked.connect(self.validate_login_info)
            self.line_password.setEchoMode(QtWidgets.QLineEdit.Password)
            self.line_user.setText(user)
            self.line_user.focusWidget()
            self.line_password.focusWidget()

            if remember == "0":
                self.check_box_user.setChecked(False)
            else:
                self.check_box_user.setChecked(True)
            self.button_register.clicked.connect(self.register_user)
            # QtWidgets.QLineEdit.focusWidget()

        except:
            print(traceback.format_exc())

    def register_user(self):
        self.main_window = RegisterForm()
        self.main_window.display_info()

    def display_info(self):
        try:
            self.setWindowModality(Qt.ApplicationModal)
            self.setFocus()
            self.show()

        except:
            print(traceback.format_exc())

    def check_remember_user(self):
        checked = self.check_box_user.isChecked()
        user = self.line_user.text()
        if checked:
            config_parser['remember_user']['user'] = user
            config_parser['remember_user']['remember'] = "1"

        else:
            config_parser['remember_user']['user'] = ""
            config_parser['remember_user']['remember'] = "0"
        ini_file = open(config_file_path, "w")
        config_parser.write(ini_file)

    def validate_login_info(self):
        try:
            input_user = self.line_user.text()
            input_password = self.line_password.text()
            login_response = get_user_info(input_user, input_password)

            if input_user == "":
                error_message("Usuário", "Usuário vazio")
                self.line_user.setFocus()
                return

            if input_password == "":
                error_message("Senha", "Senha vazia")
                self.line_password.setFocus()
                return

            if not login_response.ok:
                error_message("Login inválido", "Nome de usuário ou senha inválidos")
                self.line_password.setFocus()
                self.line_password.selectAll()
                return

            self.check_remember_user()
            self.main_window = MainWindow(input_user, input_password)
            self.main_window.show()
            self.close()

        except:
            print(traceback.format_exc())

    def clear_password(self):
        self.line_password.clear()
        self.line_user.setFocus()
        self.line_user.selectAll()


class MainWindow(QMainWindow):
    def __init__(self, username, password):
        super().__init__()
        loadUi(main_window_path, self)
        self.setWindowIcon(QtGui.QIcon("icon/vacina.png"))
        self.username = username
        self.password = password
        self.change_password_window = ChangePasswordWindow(username, password)
        self.change_password_window.teste_signal.connect(self.update_main_window_password)
        self.load_available_vacs()
        self.register_vac_window = RegisterVacWIndow(username, password, self.vac_df)
        self.register_vac_window.registered_vac_signal.connect(self.update_user_vac_table)
        self.table_all_vacs.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.table_all_vacs.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.table_user_vacs.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.table_user_vacs.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.connect_buttons()

    def update_user_vac_table(self):
        self.table_user_vacs.setRowCount(0)
        self.load_user_vacs()

    def update_main_window_password(self, val):
        self.password = val

    def connect_buttons(self):
        self.menu_change_user.triggered.connect(self.change_user)
        self.sep_change_password.triggered.connect(self.change_password_window.display_info)
        self.sep_delete_user.triggered.connect(self.delete_user)
        self.button_register_vac.clicked.connect(self.register_vac_window.display_info)

    def change_user(self):
        confirmation = notification_message("troca de usuário", "Realmente deseja trocar de usuário?")
        if confirmation == QMessageBox.Ok:
            self.close()
            main_window.clear_password()
            main_window.show()

    def delete_user(self):
        confirm_deletion = notification_message("usuário", "Realmente deseja excluir o usuário?")
        if confirm_deletion == QMessageBox.Ok:
            remove_user(self.username, self.password)
            self.close()
            main_window.show()
            del self

    def load_available_vacs(self):
        vac_list = get_all_vaccines().text
        vac_list = json.loads(vac_list)
        self.vac_df = pd.DataFrame(vac_list)
        self.table_all_vacs.setRowCount(len(vac_list))
        for index, row in enumerate(vac_list):
            vac_id = str(row['vac_id'])
            name = str(row['name'])
            obs = str(row['obs'])
            num_doses = str(row['num_doses'])
            self.table_all_vacs.setItem(index, 0, QTableWidgetItem(name))
            self.table_all_vacs.setItem(index, 1, QTableWidgetItem(num_doses))
            self.table_all_vacs.setItem(index, 2, QTableWidgetItem(obs))
        self.load_user_vacs()

    def load_user_vacs(self):
        user_vacs = get_user_vaccines(self.username, self.password).text
        user_vacs = json.loads(user_vacs)

        self.table_user_vacs.setRowCount(len(user_vacs))
        for index, vac_row in enumerate(user_vacs):
            vac_id = vac_row['vac_id']
            df_row = self.vac_df.query(f"vac_id == {vac_id}")
            vac_name = df_row['name'].item()
            date = vac_row['date_taken']
            vac_item = QTableWidgetItem(vac_name)
            vac_item.setTextAlignment(Qt.AlignCenter)
            date_item = QTableWidgetItem(date)
            date_item.setTextAlignment(Qt.AlignCenter)

            self.table_user_vacs.setItem(index, 0, vac_item)
            self.table_user_vacs.setItem(index, 1, date_item)


def set_focus_startup(window):
    if window.line_user.text() != "":
        window.line_password.setFocus()
    else:
        window.line_user.setFocus()


def error_message(message_title, message_text):
    message = QtWidgets.QMessageBox()
    message.setWindowTitle(message_title)
    message.setText(message_text)
    message.setIcon(QtWidgets.QMessageBox.Warning)
    message.exec_()


def notification_message(message_title, message_text):
    message = QtWidgets.QMessageBox()
    message.setWindowTitle(message_title)
    message.setText(message_text)
    message.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
    message.setIcon(QtWidgets.QMessageBox.Information)
    confirmation = message.exec_()
    return confirmation


def move_screen(window):
    screen_width = QDesktopWidget().availableGeometry().width()
    screen_height = QDesktopWidget().availableGeometry().height()
    window_width = window.size().width()
    window_height = window.size().height()
    middle_x = int(screen_width/2 - window_width/2)
    middle_y = int(screen_height/2 - window_height/2)
    window.move(middle_x, middle_y)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = LoginForm()
    move_screen(main_window)
    main_window.show()
    set_focus_startup(main_window)
    sys.exit(app.exec_())
