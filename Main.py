from PyQt5 import QtCore, QtGui, QtWidgets
import StackLogin
import StackLesson
import StackTest
import StackResult
import StackTableResults
import Window
import Dialogs
import version
import os
import sys
import json
import sqlite3  
import datetime    
from dataclasses import dataclass
import xml.etree.ElementTree as ET

@dataclass
class DataResult:
    points_max: int
    points_right: int
    points_wrong: int
    points_skip: int
    dict_result: dict

@dataclass
class DataSave:
    date_start: datetime.datetime
    date_end: datetime.datetime
    name: str
    surname: str
    class_name: str
    course: str
    points_max: int
    points_right: int
    points_wrong: int
    points_skip: int

@dataclass
class DataLoggin:
    name: str
    surname: str
    class_name: str
    path_course: str   

class Main(Window.Window):
    def __init__(self):
        self.init_variables()

        super().__init__(data_theme = self.data_theme["window"])

        self.setWindowTitle("IT Master")
        self.setWindowIcon(QtGui.QIcon(self.path_image_logo))

        self.set_title("IT Master")
        self.set_icon(QtGui.QPixmap(self.path_image_logo))

        self.open_info.connect(self.open_dialog_info)

        # создание страницы входа
        self.current_stack = StackLogin.StackLogin(
            path_theme = self.path_theme,
            path_courses = self.path_courses, 
            path_images = self.path_images, 
            data_theme = self.data_theme["stack_login"], 
            func_start = self.start, 
            func_table_results = self.open_table_result, 
            surname = self.data_loggin.surname, 
            name = self.data_loggin.name,
            class_name = self.data_loggin.class_name
        )

        # виджет стеков для страниц
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.stacked_widget.setObjectName("stacked_widget")

        self.add_widget(self.stacked_widget)

        # добавление страницы входа в виджет стеков
        self.stacked_widget.addWidget(self.current_stack)
        self.stacked_widget.setCurrentWidget(self.current_stack)

    def init_variables(self):
        self.text_info = """IT Master - это школьный предметный тренажёр по информатике, позволяющий изучить материал урока и закрепить полученные знания, выполнив тест\n
Ведущий разрабочик - Смирнов Н. А., 9 класс, ГБОУ школа №1370\n
Приложение написано на языке программирования Python"""

        self.path_settings = r"settings.json"

        self.test_started = False

        # получение настроек
        with open(self.path_settings, "r", encoding = "utf-8") as file:
            self.data = json.load(file)

        self.path_theme = self.data["path_theme"]

        # получение настроек цветовой темы
        with open(self.path_theme, "r", encoding = "utf-8") as file:
            self.data_theme = json.load(file)

        self.path_courses = self.data["path_courses"]
        self.path_images = self.data["path_images"]
        self.path_database = self.data["path_database"]
        self.path_image_logo = os.path.join(self.path_images, r"logo.png")

        self.data_loggin = DataLoggin(
            name = None,
            surname = None,
            class_name = None,
            path_course = None
        )

        # создание БД если её нет
        with sqlite3.connect(self.path_database) as db:
            cursor = db.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                date_start VARCHAR,
                date_end VARCHAR,
                name VARCHAR,
                surname VARCHAR,
                class_name VARCHAR,
                course VARCHAR,
                points_max INTEGER,
                points_right INTEGER,
                points_wrong INTEGER,
                points_skip INTEGER,
                result INTEGER
            ) """)

    def delete_old_record(self):
        # оставить в БД <= 100 записей
        with sqlite3.connect(self.path_database) as db:
            cursor = db.cursor()

            cursor.execute("""SELECT date_end FROM users""")
            amount_rows = i if (i := len(cursor.fetchall()) - 100) > 0 else 0

            cursor.execute("""DELETE FROM users WHERE date_end IN (SELECT date_end FROM users ORDER BY date_end ASC LIMIT ?)""", (amount_rows, ))

    def create_record(self, data: DataSave):
        # запись данных о прохождении в БД
        with sqlite3.connect(self.path_database) as db:
            cursor = db.cursor()

            values = (
                data.date_start.strftime(r"%Y.%m.%d %H:%M"),
                data.date_end.strftime(r"%Y.%m.%d %H:%M"),
                data.name,
                data.surname,
                data.class_name,
                data.course,
                data.points_max,
                data.points_right,
                data.points_wrong,
                data.points_skip,
                round(data.points_right / data.points_max * 100),
            )

            cursor.execute("""
            INSERT INTO users(
                date_start,
                date_end,
                name,
                surname,
                class_name,
                course,
                points_max,
                points_right,
                points_wrong,
                points_skip,
                result) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """, values)

        self.delete_old_record()

    def finish_test(self, data: StackTest.DataPassage):
        self.test_started = False

        # получение данных о прохождении
        data_save = DataSave(
            name = self.data_loggin.name,
            surname = self.data_loggin.surname,
            class_name = self.data_loggin.class_name,
            course = os.path.splitext(os.path.basename(self.data_loggin.path_course))[0],
            date_start = data.date_start,
            date_end = data.date_end,
            points_max = data.points_max,
            points_right = data.points_right,
            points_wrong = data.points_wrong,
            points_skip = data.points_skip
        )

        data_result = DataResult(
            points_max = data.points_max,
            points_right = data.points_right,
            points_wrong = data.points_wrong,
            points_skip = data.points_skip,
            dict_result = data.dict_result
        )

        self.create_record(data_save)

        # удаление старого окна
        self.stacked_widget.removeWidget(self.current_stack)

        # создание и упаковка окна результата выполнения
        self.current_stack = StackResult.StackResult(data_result = data_result, data_theme = self.data_theme["stack_result"], func = self.to_main)

        self.stacked_widget.addWidget(self.current_stack)
        self.stacked_widget.setCurrentWidget(self.current_stack)

    def start_test(self):
        self.test_started = True

        # удаление старого окна
        self.stacked_widget.removeWidget(self.current_stack)

        # создание и упаковка окна с тестом
        self.current_stack = StackTest.StackTest(
            icon_dialogs = QtGui.QPixmap(self.path_image_logo),
            parent = self, func = self.finish_test, 
            path_images = self.path_images, 
            data_theme = self.data_theme["stack_test"], 
            path_course = self.data_loggin.path_course
        )

        self.stacked_widget.addWidget(self.current_stack)
        self.stacked_widget.setCurrentWidget(self.current_stack)

    def open_table_result(self, data: StackLogin.DataPassage):
        # проверить пустая ли таблица
        with sqlite3.connect(self.path_database) as db:
            cursor = db.cursor()

            cursor.execute("""SELECT date_end FROM users""")
            amount = len(cursor.fetchall())

        if amount != 0:
            self.data_loggin = DataLoggin(
                name = data.name,
                surname = data.surname,
                class_name = data.class_name,
                path_course = data.path_course
            )

            # удаление старого окна
            self.stacked_widget.removeWidget(self.current_stack)

            # создание и упаковка окна с таблицей результатов
            self.current_stack = StackTableResults.StackTableResults(path_database = self.path_database, func = self.to_main, data_theme = self.data_theme["stack_table_result"])

            self.stacked_widget.addWidget(self.current_stack)
            self.stacked_widget.setCurrentWidget(self.current_stack)

        else:
            self.open_dialog_table_results_empty()

    def start(self, data: StackLogin.DataPassage):
        self.data_loggin = DataLoggin(
            name = data.name,
            surname = data.surname,
            class_name = data.class_name,
            path_course = data.path_course
        )

        # определение есть ли урок
        tree = ET.parse(self.data_loggin.path_course)
        root = tree.getroot()

        if root.find("lesson") != None:
            self.open_lesson()
        else:
            self.start_test()

    def open_lesson(self):
        # удаление старого окна
        self.stacked_widget.removeWidget(self.current_stack)

        tree = ET.parse(self.data_loggin.path_course)
        root = tree.getroot()
        path_lesson = os.path.join(os.path.split(self.data_loggin.path_course)[0], root.find("lesson").text).replace("\\", "/")

        # создание и упаковка окна урока
        self.current_stack = StackLesson.StackLesson(path_lesson = path_lesson, data_theme = self.data_theme["stack_lesson"], func = self.start_test)

        self.stacked_widget.addWidget(self.current_stack)
        self.stacked_widget.setCurrentWidget(self.current_stack)

        # показать урок
        self.current_stack.load_lesson()
        
    def to_main(self):
        # удаление старого окна
        self.stacked_widget.removeWidget(self.current_stack)

        # создание и упаковка окна входа
        self.current_stack = StackLogin.StackLogin(
            path_theme = self.path_theme,
            path_courses = self.path_courses, 
            path_images = self.path_images, 
            data_theme = self.data_theme["stack_login"], 
            func_start = self.start, 
            func_table_results = self.open_table_result, 
            surname = self.data_loggin.surname, 
            name = self.data_loggin.name,
            class_name = self.data_loggin.class_name
        )

        self.stacked_widget.addWidget(self.current_stack)
        self.stacked_widget.setCurrentWidget(self.current_stack)

    def open_dialog_info(self):
        dialog = Dialogs.DialogInfo(
            data_theme = self.data_theme["dialog_info"],
            version = f"Версия {version.__version__}",
            name = "IT Master",
            text_info = self.text_info,
            path_logo = self.path_image_logo,
            parent = self
        )

    def open_dialog_table_results_empty(self):
        dialog = Dialogs.DialogTableResultsEmpty(
            data_theme = self.data_theme["dialog_table_results_empty"], 
            parent = self
        )

    def exit_test(self):
        self.test_started = False

        self.to_main()

    def close_window(self):
        if self.test_started:
            dialog = Dialogs.DialogExit(data_theme = self.data_theme["dialog_exit_test"], parent = self)
            dialog.push_button_clicked_exit.connect(self.exit_test)
        else:
            super().close_window()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window_main = Main()
    window_main.show_window()

    sys.exit(app.exec_())
