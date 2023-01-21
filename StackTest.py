from PyQt5 import QtCore, QtGui, QtWidgets
import os
import datetime
import xml.etree.ElementTree as ET
import re
from dataclasses import dataclass
import Dialogs

@dataclass
class DataPassage:
    date_start: datetime.datetime
    date_end: datetime.datetime
    points_max: int
    points_right: int
    points_wrong: int
    points_skip: int
    dict_result: dict

class PushButtonNavigation(QtWidgets.QPushButton):
    push_button_current = None
    push_button_clicked = QtCore.pyqtSignal(int)
    def __init__(self, number: int, data_theme: dict):
        super().__init__()

        self.number = number
        self.data_theme = data_theme

        self.init_variables()

        self.setObjectName("push_button_navigation")
        self.setText(f"{self.number + 1}")
        self.setFont(QtGui.QFont("Segoe UI", 12))
        self.setFixedSize(50, 50)
        self.clicked.connect(self.push_button_press)

        self.set_style_sheet()

    def init_variables(self):
        self.dict_state = {
            "answered": False,
            "current": False
        }

    def push_button_press(self):
        if self != PushButtonNavigation.push_button_current and PushButtonNavigation.push_button_current != None:
            PushButtonNavigation.push_button_current.set_not_current()

        if self != PushButtonNavigation.push_button_current:
            PushButtonNavigation.push_button_current = self
            self.set_current()

            self.push_button_clicked.emit(self.number)

    def set_current(self):
        self.dict_state["current"] = True

        self.set_style_sheet()

    def set_not_current(self):
        self.dict_state["current"] = False

        self.set_style_sheet()

    def set_answered(self):
        self.dict_state["answered"] = True

        self.set_style_sheet()

    def set_not_answered(self):
        self.dict_state["answered"] = False

        self.set_style_sheet()

    def set_style_sheet(self):
        if self.dict_state["current"]:
            temp_style_sheet = self.data_theme["current"]
        else:
            temp_style_sheet = self.data_theme["not_current"]
        
        if self.dict_state["answered"]:
            temp_style_sheet = temp_style_sheet["answered"]
        else:
            temp_style_sheet = temp_style_sheet["not_answered"]

        self.setStyleSheet("""
        #push_button_navigation {
            outline: 0;
            border: 3px solid;
            border-radius: 25px;
            background: %(background)s;
            border-color: %(color_border)s;
            color: %(color)s;
        } """ % temp_style_sheet)

class BarNavigation(QtWidgets.QWidget):
    def __init__(self, len_course: int, data_theme: dict, func: callable):
        super().__init__()

        self.len_course = len_course
        self.data_theme = data_theme
        self.func = func

        self.init_variables()

        # главный макет
        self.hbox_layout_main = QtWidgets.QHBoxLayout()
        self.hbox_layout_main.setSpacing(10)
        self.hbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.hbox_layout_main)

        for i in range(self.len_course):
            push_button = PushButtonNavigation(number = i, data_theme = self.data_theme)
            push_button.push_button_clicked.connect(self.func)
            self.list_answered[i][0] = push_button
            self.hbox_layout_main.addWidget(push_button)

    def change_answered(self, number: int):
        self.list_answered[number][1] = True
        self.list_answered[number][0].set_answered()

    def push_button_press(self, number: int):
        self.list_answered[number][0].push_button_press()

    def init_variables(self):
        self.list_answered = {i: [None, False] for i in range(self.len_course)}

class RadiobuttonAnswers(QtWidgets.QWidget):
    radio_button_checked = QtCore.pyqtSignal()
    def __init__(self, text: str, path_images: str, data_theme: dict):
        self.__text = text
        self.data_theme = data_theme
        self.path_images = path_images

        self.init_variables()

        super().__init__()

        # главный макет
        self.hbox_layout_main = QtWidgets.QHBoxLayout()
        self.hbox_layout_main.setSpacing(0)
        self.hbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.hbox_layout_main)

        # кнопка с флажком
        self.push_button_flag = QtWidgets.QPushButton()
        self.push_button_flag.setObjectName("push_button_flag")
        self.push_button_flag.clicked.connect(self.radio_button_clicked)
        self.push_button_flag.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.push_button_flag.setMinimumHeight(25)

        self.hbox_layout_main.addWidget(self.push_button_flag)
        self.hbox_layout_main.addSpacing(5)

        # кнопка с текстом
        self.push_button_text = QtWidgets.QPushButton ()
        self.push_button_text.setObjectName("push_button_text")
        self.push_button_text.clicked.connect(self.radio_button_clicked)
        self.push_button_text.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

        self.hbox_layout_main.addWidget(self.push_button_text)

        # макет внутки кнопки
        self.push_button_text.layout_label_text = QtWidgets.QHBoxLayout()
        self.push_button_text.layout_label_text.setSpacing(0)
        self.push_button_text.layout_label_text.setContentsMargins(0, 0, 0, 0)

        self.push_button_text.setLayout(self.push_button_text.layout_label_text)

        # метка внутри кнопки
        self.label_text = QtWidgets.QLabel()
        self.label_text.setObjectName("label_text")
        self.label_text.setText(self.__text)
        self.label_text.setWordWrap(True)
        self.label_text.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.label_text.setFont(QtGui.QFont("Segoe UI", 14))
        self.label_text.setMinimumHeight(25)

        self.push_button_text.layout().addWidget(self.label_text)

        self.set_style_sheet()

        self.set_checked(checked = False)

    def text(self) -> str:
        return self.__text

    def is_checked(self) -> bool:
        return self.__checked

    def init_variables(self):
        self.path_img_checked = os.path.join(self.path_images, "radio_button_checked.png").replace("\\", "/")
        self.path_img_unchecked = os.path.join(self.path_images, "radio_button_unchecked.png").replace("\\", "/")

        self.image_flag_checked = QtGui.QIcon(self.path_img_checked)
        self.image_flag_unchecked = QtGui.QIcon(self.path_img_unchecked)

    def radio_button_clicked(self):
        if self.__checked == False:
            self.set_checked(checked = True)

    def set_checked(self, checked: bool):
        if checked == True:
            self.__checked = True

            self.push_button_flag.setIcon(self.image_flag_checked)
            self.push_button_flag.setIconSize(QtCore.QSize(22, 22))

            self.radio_button_checked.emit()

        elif checked == False:
            self.__checked = False

            self.push_button_flag.setIcon(self.image_flag_unchecked)
            self.push_button_flag.setIconSize(QtCore.QSize(22, 22))

    def set_style_sheet(self):
        # кнопка с флажком
        self.push_button_flag.setStyleSheet("""
        #push_button_flag {
            outline: 0;
            border: none;
            background: %(background)s;
        } """ % self.data_theme)

        # кнопка с текстом
        self.push_button_text.setStyleSheet("""
        #push_button_text {
            text-align: left;
            outline: 0;
            border: none;
            background: %(background)s;
        } """ % self.data_theme)

        # метка внутри кнопки
        self.label_text.setStyleSheet("""
        #label_text {
            background: %(background)s;
            color: %(color)s;
        } """ % self.data_theme)

class GroupRadiobuttons(QtCore.QObject):
    radio_button_checked = QtCore.pyqtSignal(RadiobuttonAnswers)
    def __init__(self):
        super().__init__()

        self.__list_radio_buttons = []
        self.__checked_radio_button = None

    def change_radio_button(self, radio_button: RadiobuttonAnswers):
        if self.__checked_radio_button != radio_button:
            if self.__checked_radio_button !=  None:
                self.__checked_radio_button.set_checked(checked = False)
            self.__checked_radio_button = radio_button

            self.radio_button_checked.emit(self.__checked_radio_button)

    def add_radio_button(self, radio_button: RadiobuttonAnswers):
        radio_button.radio_button_checked.connect(lambda: self.change_radio_button(radio_button))
        self.__list_radio_buttons.append(radio_button)

class CheckboxAnswers(QtWidgets.QWidget):
    checkbox_checked = QtCore.pyqtSignal()
    def __init__(self, text: str, path_images: str, data_theme: dict):
        self.__text = text
        self.data_theme = data_theme
        self.path_images = path_images
        self.__checked = False

        self.init_variables()

        super().__init__()

        # главный макет
        self.hbox_layout_main = QtWidgets.QHBoxLayout()
        self.hbox_layout_main.setSpacing(0)
        self.hbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.hbox_layout_main)

        # кнопка с флажком
        self.push_button_flag = QtWidgets.QPushButton()
        self.push_button_flag.setObjectName("push_button_flag")
        self.push_button_flag.clicked.connect(self.checkbox_clicked)
        self.push_button_flag.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.push_button_flag.setMinimumHeight(25)

        self.hbox_layout_main.addWidget(self.push_button_flag)
        self.hbox_layout_main.addSpacing(5)

        # кнопка с текстом
        self.push_button_text = QtWidgets.QPushButton()
        self.push_button_text.setObjectName("push_button_text")
        self.push_button_text.clicked.connect(self.checkbox_clicked)
        self.push_button_text.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

        self.hbox_layout_main.addWidget(self.push_button_text)

        # макет внутки кнопки
        self.push_button_text.layout_label_text = QtWidgets.QHBoxLayout()
        self.push_button_text.layout_label_text.setSpacing(0)
        self.push_button_text.layout_label_text.setContentsMargins(0, 0, 0, 0)

        self.push_button_text.setLayout(self.push_button_text.layout_label_text)

        # метка внутри кнопки
        self.label_text = QtWidgets.QLabel()
        self.label_text.setObjectName("label_text")
        self.label_text.setText(self.__text)
        self.label_text.setWordWrap(True)
        self.label_text.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.label_text.setFont(QtGui.QFont("Segoe UI", 14))
        self.label_text.setMinimumHeight(25)

        self.push_button_text.layout().addWidget(self.label_text)

        self.set_style_sheet()

        self.set_checked(checked = False)

    def is_checked(self) -> bool:
        return self.__checked

    def text(self) -> str:
        return self.__text

    def init_variables(self):
        self.path_img_checked = os.path.join(self.path_images, "checkbox_checked.png").replace("\\", "/")
        self.path_img_unchecked = os.path.join(self.path_images, "checkbox_unchecked.png").replace("\\", "/")

        self.image_flag_checked = QtGui.QIcon(self.path_img_checked)
        self.image_flag_unchecked = QtGui.QIcon(self.path_img_unchecked)

    def checkbox_clicked(self):
        if self.__checked == True:
            self.set_checked(checked = False)
        else:
            self.set_checked(checked = True)

        self.checkbox_checked.emit()

    def set_checked(self, checked: bool):
        if checked == True:
            self.__checked = True

            self.push_button_flag.setIcon(self.image_flag_checked)
            self.push_button_flag.setIconSize(QtCore.QSize(22, 22))

        elif checked == False:
            self.__checked = False

            self.push_button_flag.setIcon(self.image_flag_unchecked)
            self.push_button_flag.setIconSize(QtCore.QSize(22, 22))

    def set_style_sheet(self):
        # кнопка с флажком
        self.push_button_flag.setStyleSheet("""
        #push_button_flag {
            outline: 0;
            border: none;
            background: %(background)s;
        } """ % self.data_theme)

        # кнопка с текстом
        self.push_button_text.setStyleSheet("""
        #push_button_text {
            text-align: left;
            outline: 0;
            border: none;
            background: %(background)s;
        } """ % self.data_theme)

        # метка внутри кнопки
        self.label_text.setStyleSheet("""
        #label_text {
            background: %(background)s;
            color: %(color)s;
        } """ % self.data_theme)

class PushButtonImage(QtWidgets.QPushButton):
    push_button_clicked = QtCore.pyqtSignal()
    def __init__(self, path_image: str,  data_theme: dict):
        super().__init__()

        self.path_image = path_image
        self.data_theme = data_theme

        self.init_variables()

        self.setObjectName("push_button_image")
        self.setFixedSize(300, 200)
        self.clicked.connect(self.push_button_press)

        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.set_style_sheet()

    def init_variables(self):
        self.pixmap = QtGui.QPixmap(self.path_image)

        zoom = max(300 / self.pixmap.width(), 200 / self.pixmap.height())
        self.pixmap = self.pixmap.scaled(round(self.pixmap.width() * zoom), round(self.pixmap.height() * zoom), transformMode = QtCore.Qt.SmoothTransformation)
        
        delta_x = (self.pixmap.width() - 300) // 2
        delta_y = (self.pixmap.height() - 200) // 2
        self.pixmap = self.pixmap.copy(delta_x + 10, delta_y + 10, 300 - 10, 200 - 10)
        self.image = QtGui.QIcon(self.pixmap)

    def push_button_press(self):
        self.push_button_clicked.emit()

    def set_style_sheet(self):
        self.setStyleSheet("""
        #push_button_image {
            outline: 0;
            border-radius: 7px; 
            background: %(background)s; 
        } """ % self.data_theme)
        
        self.setIcon(self.image)
        self.setIconSize(QtCore.QSize(300, 200))

class WidgetTest(QtWidgets.QWidget):
    def __init__(self, path_course: str, icon_dialogs: QtGui.QPixmap, question: str, path_images: str, started: bool, answer, data_theme: dict, number: int, len_course: int, func_changed: callable, parent = None):
        super().__init__()

        self.path_course = path_course
        self.started = started
        self.answer = answer
        self.question = question
        self.data_theme = data_theme
        self.path_images = path_images
        self.number = number
        self.len_course = len_course
        self.func_changed = func_changed
        self.parent = parent
        self.icon_dialogs = icon_dialogs

        # главный макет
        self.grid_layout_main = QtWidgets.QGridLayout()
        self.grid_layout_main.setSpacing(0)
        self.grid_layout_main.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_main.setColumnStretch(0, 0)
        self.grid_layout_main.setColumnStretch(1, 1)
        self.grid_layout_main.setColumnStretch(2, 0)
        self.grid_layout_main.setRowStretch(0, 0)
        self.grid_layout_main.setRowStretch(1, 1)
        self.grid_layout_main.setRowStretch(2, 0)

        self.setLayout(self.grid_layout_main)

        # главная рамка
        self.frame_main = QtWidgets.QFrame()
        self.frame_main.setObjectName("frame_main")

        self.grid_layout_main.addWidget(self.frame_main, 1, 1)

        # макет для виджетов теста
        self.vbox_layout_internal =  QtWidgets.QVBoxLayout()
        self.vbox_layout_internal.setSpacing(0)
        self.vbox_layout_internal.setContentsMargins(20, 20, 20, 20)

        self.frame_main.setLayout(self.vbox_layout_internal)

        # метка номера задания
        self.label_numder_question = QtWidgets.QLabel()
        self.label_numder_question.setObjectName("label_numder_question")
        self.label_numder_question.setFont(QtGui.QFont("Segoe UI", 12))
        self.label_numder_question.setText(f"Вопрос {self.number + 1}")

        self.vbox_layout_internal.addWidget(self.label_numder_question)

        # метка с вопросом
        self.label_question = QtWidgets.QLabel()
        self.label_question.setObjectName("label_question")
        self.label_question.setWordWrap(True)
        self.label_question.setFont(QtGui.QFont("Segoe UI", 14))
        self.label_question.setText(self.question.find("title").text)

        self.vbox_layout_internal.addWidget(self.label_question)

        # метка типа задания
        self.label_type_question = QtWidgets.QLabel()
        self.label_type_question.setObjectName("label_type_question")
        self.label_type_question.setFont(QtGui.QFont("Segoe UI", 12))

        self.vbox_layout_internal.addWidget(self.label_type_question)
        self.vbox_layout_internal.addSpacing(5)

        # добавление кнопки с изображением
        if (path_image := self.question.find("questions").find("image")) != None:
            self.path_image = os.path.join(os.path.split(self.path_course)[0], path_image.text).replace("\\", "/")

            self.push_button_image = PushButtonImage(path_image = self.path_image, data_theme = self.data_theme["frame_main"]["push_button_image"])
            self.push_button_image.push_button_clicked.connect(self.show_image)

            self.vbox_layout_internal.addWidget(self.push_button_image)
            self.vbox_layout_internal.addSpacing(5)

        # создание виджетов ответов
        if self.question.find("questions").find("type").text == "radio_button":
            self.label_type_question.setText("Укажите правильный вариант ответа:")

            self.create_radio_buttons(list_radio_buttons = self.question.find("questions").findall("question"))

        elif self.question.find("questions").find("type").text == "checkbox":
            self.label_type_question.setText("Укажите правильные варианты ответа:")

            self.create_checkboxes(list_checkboxes = self.question.find("questions").findall("question"))

        elif self.question.find("questions").find("type").text == "input":
            self.label_type_question.setText("Введите правильный ответ:")
            
            self.line_edit_answer = QtWidgets.QLineEdit()
            self.line_edit_answer.setObjectName("line_edit_answer")
            self.line_edit_answer.textChanged.connect(self.line_edit_text_changed)
            self.line_edit_answer.setFont(QtGui.QFont("Segoe UI", 14))
            self.line_edit_answer.setMinimumHeight(42)

            if self.started:
                self.line_edit_answer.insert(self.answer)

            self.vbox_layout_internal.addWidget(self.line_edit_answer)

            temp_data_theme = {
            "color_border_not_focus": self.data_theme["frame_main"]["line_edit"]["not_focus"]["color_border"],
            "background_not_focus": self.data_theme["frame_main"]["line_edit"]["not_focus"]["background"], 
            "color_not_focus": self.data_theme["frame_main"]["line_edit"]["not_focus"]["color"], 
            "color_border_focus": self.data_theme["frame_main"]["line_edit"]["focus"]["color_border"],
            "background_focus": self.data_theme["frame_main"]["line_edit"]["focus"]["background"], 
            "color_focus": self.data_theme["frame_main"]["line_edit"]["focus"]["color"]
            }

            self.line_edit_answer.setStyleSheet("""
            #line_edit_answer {
                border-radius: 7px; 
                border: 2px solid; 
                border-color: %(color_border_not_focus)s;
                background: %(background_not_focus)s; 
                color: %(color_not_focus)s;
            } 
            #line_edit_answer:focus {
                border-color: %(color_border_focus)s;
                background: %(background_focus)s; 
                color: %(color_focus)s;
            } """ % temp_data_theme)

        self.vbox_layout_internal.addStretch(1)
        
        self.set_style_sheet()

    def show_image(self):
        self.dialog_image = Dialogs.DialogImage(
            parent = self.parent, 
            path_image = self.path_image,
            data_theme = self.data_theme["frame_main"]["dialog_image"]
        )
        self.dialog_image.set_icon(icon = self.icon_dialogs)
        self.dialog_image.set_title(title = "Изображение")

        self.dialog_image.load_lesson()

    def radio_button_clicked(self, radio_button: RadiobuttonAnswers):
        self.answer = radio_button.text()

        self.func_changed(self.number)

    def ceckbox_clicked(self):
        if not self.sender().is_checked() and self.sender().text() in self.answer:
            self.answer.remove(self.sender().text())
        else:
            self.answer.append(self.sender().text())

        self.func_changed(self.number)

    def line_edit_text_changed(self):
        self.answer = self.line_edit_answer.text()

        self.func_changed(self.number)

    def create_radio_buttons(self, list_radio_buttons: list):
        # макет радиокнопок
        self.vbox_layout_radio_buttons = QtWidgets.QVBoxLayout()
        self.vbox_layout_radio_buttons.setSpacing(10)
        self.vbox_layout_radio_buttons.setContentsMargins(0, 0, 0, 0)

        self.vbox_layout_internal.addLayout(self.vbox_layout_radio_buttons)

        # группа радио кнопок
        self.group_radio_buttons = GroupRadiobuttons()

        # создание и упаковка радиокнопок
        for element in list_radio_buttons:
            radio_button = RadiobuttonAnswers(
                path_images = self.path_images,
                text = element.text,
                data_theme = self.data_theme["frame_main"]["radio_button"]
            )

            self.group_radio_buttons.add_radio_button(radio_button)

            if self.started and element.text == self.answer:
                radio_button.set_checked(checked = True)

            self.vbox_layout_radio_buttons.addWidget(radio_button)

        self.group_radio_buttons.radio_button_checked.connect(self.radio_button_clicked)
    
    def create_checkboxes(self, list_checkboxes: list):
        # макет переключателей
        self.vbox_layout_checkboxes = QtWidgets.QVBoxLayout()
        self.vbox_layout_checkboxes.setSpacing(10)
        self.vbox_layout_checkboxes.setContentsMargins(0, 0, 0, 0)

        self.vbox_layout_internal.addLayout(self.vbox_layout_checkboxes)

        # создание и упаковка радиокнопок
        for element in list_checkboxes:
            checkbox = CheckboxAnswers(
                path_images = self.path_images, 
                text = element.text, 
                data_theme = self.data_theme["frame_main"]["checkbox"]
            )

            if self.started and element.text in self.answer:
                checkbox.set_checked(checked = True)

            self.vbox_layout_checkboxes.addWidget(checkbox)
            
            checkbox.checkbox_checked.connect(self.ceckbox_clicked)

    def set_style_sheet(self):
        # главная рамка
        self.frame_main.setStyleSheet("""
        #frame_main {
            background: %(background)s;
        } """ % self.data_theme["frame_main"])

        # метка номера задания
        self.label_question.setStyleSheet("""
        #label_question {
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["label_question"])

        # метка вопроса
        self.label_numder_question.setStyleSheet("""
        #label_numder_question {
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["label_numder_question"])

        # метка типа задания
        self.label_type_question.setStyleSheet("""
        #label_type_question { 
            color: %(color)s;
        }""" % self.data_theme["frame_main"]["label_type_question"])

class StackTest(QtWidgets.QWidget):
    def __init__(self, data_theme: dict, icon_dialogs: QtGui.QPixmap, path_images: str, path_course: str, func: callable, parent = None):
        super().__init__()

        self.data_theme = data_theme
        self.path_images = path_images
        self.path_course = path_course
        self.func = func
        self.parent = parent
        self.icon_dialogs = icon_dialogs

        self.init_variables()

        # главная сетка
        self.grid_layout_main = QtWidgets.QGridLayout(self)
        self.grid_layout_main.setSpacing(0)
        self.grid_layout_main.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_main.setRowStretch(0, 0)
        self.grid_layout_main.setRowStretch(1, 1)
        self.grid_layout_main.setRowStretch(2, 0)
        self.grid_layout_main.setColumnStretch(0, 0)
        self.grid_layout_main.setColumnStretch(1, 1)
        self.grid_layout_main.setColumnStretch(2, 0)

        # главная рамка
        self.frame_main = QtWidgets.QFrame()
        self.frame_main.setObjectName("frame_main")

        self.grid_layout_main.addWidget(self.frame_main, 1, 1)

        # главный макет
        self.vbox_layout_main = QtWidgets.QVBoxLayout()
        self.vbox_layout_main.setSpacing(0)
        self.vbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.frame_main.setLayout(self.vbox_layout_main)

        # сетка тестов
        self.grid_layout_test = QtWidgets.QGridLayout()
        self.grid_layout_test.setSpacing(0)
        self.grid_layout_test.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_test.setRowStretch(0, 0)
        self.grid_layout_test.setRowStretch(1, 1)
        self.grid_layout_test.setRowStretch(2, 0)
        self.grid_layout_test.setColumnStretch(0, 0)
        self.grid_layout_test.setColumnStretch(1, 1)
        self.grid_layout_test.setColumnStretch(2, 0)

        self.vbox_layout_main.addLayout(self.grid_layout_test)

        # виджет стеков для страниц теста
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.stacked_widget.setObjectName("stacked_widget")

        self.grid_layout_test.addWidget(self.stacked_widget, 1, 1)

        # панель инструментов и навигации
        self.frame_tools = QtWidgets.QFrame()
        self.frame_tools.setObjectName("frame_tools")
        
        self.vbox_layout_main.addWidget(self.frame_tools)

        # макет панели инстументов
        self.hbox_layout_tools = QtWidgets.QHBoxLayout()
        self.hbox_layout_tools.setSpacing(0)
        self.hbox_layout_tools.setContentsMargins(20, 10, 20, 10)

        self.frame_tools.setLayout(self.hbox_layout_tools)

        self.hbox_layout_tools.addStretch(1)

        # панель навигации с кнопками
        self.bar_navigation = BarNavigation(
            len_course = self.len_course, 
            data_theme = self.data_theme["frame_main"]["frame_tools"]["push_button_navigation"], 
            func = self.switch_question
        )

        self.hbox_layout_tools.addWidget(self.bar_navigation)
        self.hbox_layout_tools.addStretch(1)

        # кнопка завершить тест
        self.push_button_finish = QtWidgets.QPushButton()
        self.push_button_finish.setObjectName("push_button_finish")
        self.push_button_finish.clicked.connect(self.finish_test)
        self.push_button_finish.setText("Завершить")
        self.push_button_finish.setFont(QtGui.QFont("Segoe UI", 12))
        self.push_button_finish.setFixedHeight(42)

        self.hbox_layout_tools.addWidget(self.push_button_finish)

        # создать страницу теста
        self.switch_question(self.current_question)
        self.bar_navigation.push_button_press(number = self.current_question)

        self.set_style_sheet()

    def init_variables(self):
        self.current_stack = None
        self.current_question = 0

        self.tree = ET.parse(self.path_course)
        self.root = self.tree.getroot()

        self.len_course = len(self.root.findall("exercise"))
        self.dict_answers = {}
        self.dict_started = {i: False for i in range(self.len_course)}
        for i in range(self.len_course):
            temp = self.root.findall("exercise")[i].find("questions").find("type").text
            if temp == "checkbox":
                self.dict_answers[i] = []
            elif temp == "radio_button":
                self.dict_answers[i] = None
            elif temp == "input":
                self.dict_answers[i] = None

        self.time_start = datetime.datetime.now()

    def finish_test(self):
        # получение ответа текущей страницы
        self.dict_answers[self.current_stack.number] = self.current_stack.answer

        # подсчёт количества верных, неверных и пропущенных ответ
        points_right = 0
        points_wrong = 0
        points_skip = 0

        dict_result = {}

        for i in range(self.len_course):
            user_answer = self.dict_answers[i]
            right_answer = list(i.text for i in self.root.findall("exercise")[i].find("answers").findall("answer"))
            type = self.root.findall("exercise")[i].find("questions").find("type").text

            if self.dict_started[i]:
                # если радиокнопка
                if type == "radio_button":
                    if user_answer == right_answer[0]:
                        points_right += 1
                        dict_result[i] = "right"
                    else:
                        points_wrong += 1
                        dict_result[i] = "wrong"

                # если переключатель
                elif type == "checkbox":
                    right_answer.sort()
                    user_answer.sort()

                    if user_answer == right_answer:
                        points_right += 1
                        dict_result[i] = "right"
                    else:
                        points_wrong += 1
                        dict_result[i] = "wrong"

                # если ввод ответа
                elif type == "input":
                    settings = None
                    right_answer = right_answer[0]

                    if (_setting := self.root.findall("exercise")[i].find("answers").find("settings")) != None:
                        settings = _setting.attrib
                    
                    if settings and user_answer != None:
                        # убирает пробелы
                        if "including_space" in settings:
                            if settings["including_space"] == "False":
                                pattern = re.compile(r"^\s*|\s*$")

                                right_answer = pattern.sub(r"", right_answer)
                                user_answer = pattern.sub(r"", user_answer)

                        if "type" in settings:
                            if settings["type"] == "number":
                                # заменаяет , на .
                                right_answer = right_answer.replace(",", ".")
                                user_answer = user_answer.replace(",", ".")

                                # проверка на число
                                pattern = re.compile("^-?\d+(\.d+)?$")

                                # если это число, то приводит к дробному типу
                                if (right_answer_ := pattern.match(right_answer)) and (user_answer_ := pattern.match(user_answer)):
                                    if right_answer_.group(0) and user_answer_.group(0):
                                        right_answer = str(float(right_answer))
                                        user_answer = str(float(user_answer))

                    if right_answer == user_answer:
                        points_right += 1
                        dict_result[i] = "right"
                    else:
                        points_wrong += 1
                        dict_result[i] = "wrong"

            else:
                points_skip += 1
                dict_result[i] = "skip"

        data_passage = DataPassage(
            date_start = self.time_start,
            date_end = datetime.datetime.now(),
            points_max = self.len_course,
            points_right = points_right,
            points_wrong = points_wrong,
            points_skip = points_skip,
            dict_result = dict_result
        )

        self.func(data_passage)

    def switch_question(self, number: int):
        current_question = self.root.findall("exercise")[number]

        if self.current_stack != None:
            # сохранение ответа
            self.dict_answers[self.current_stack.number] = self.current_stack.answer

            # удаление старой страницы
            self.stacked_widget.removeWidget(self.current_stack)

        # создание и упаковка новой страницы
        self.current_stack = WidgetTest(
            icon_dialogs = self.icon_dialogs,
            parent = self.parent,
            path_course = self.path_course,
            question = current_question,
            path_images = self.path_images, 
            started = self.dict_started[number],
            answer = self.dict_answers[number], 
            data_theme = self.data_theme["frame_main"]["test_tab"], 
            number = number, 
            len_course = self.len_course, 
            func_changed = self.func_changed
        )

        self.stacked_widget.addWidget(self.current_stack)
        self.stacked_widget.setCurrentWidget(self.current_stack)

    def func_changed(self, number: int):
        self.bar_navigation.change_answered(number)
        self.dict_started[number] = True

    def set_style_sheet(self):
        # панель инструментов и навигации
        self.frame_tools.setStyleSheet("""
        #frame_tools {
            border-top-left-radius: 40px;
            border-top-right-radius: 40px;
            background: %(background)s;
        } """ % self.data_theme["frame_main"]["frame_tools"])

        # главная рамка
        self.frame_main.setStyleSheet("""
        #frame_main {
            background: %(background)s;
        } """ % self.data_theme["frame_main"])

        # кнопка завершить тест
        self.push_button_finish.setStyleSheet("""
        #push_button_finish {
            outline: 0;
            border-top-left-radius: 7px;
            border-top-right-radius: 25px;
            border-bottom-left-radius: 7px;
            border-bottom-right-radius: 7px;
            padding-left: 10px;
            padding-right: 10px;
            color: %(color)s;
            background: %(background)s; 
        } """ % self.data_theme["frame_main"]["frame_tools"]["push_button_finish"])
