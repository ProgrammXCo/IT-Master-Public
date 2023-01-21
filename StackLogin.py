from PyQt5 import QtCore, QtGui, QtWidgets
import os
from dataclasses import dataclass

@dataclass
class DataPassage:
    name: str
    surname: str
    class_name: str
    path_course: str

class PushButtonCourse(QtWidgets.QWidget):
    push_button_clicked_choose_course = QtCore.pyqtSignal()
    def __init__(self, path_images: str, data_theme: dict):
        super().__init__()

        self.path_images = path_images
        self.data_theme = data_theme

        self.init_variables()

        # главный макет
        self.hbox_layout_main = QtWidgets.QHBoxLayout(self)
        self.hbox_layout_main.setSpacing(0)
        self.hbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.hbox_layout_main)

        # кнопка с название курса
        self.push_button_title = QtWidgets.QPushButton()
        self.push_button_title.setObjectName("push_button_title")
        self.push_button_title.clicked.connect(self.press_choose_course)
        self.push_button_title.setText("Выбрать урок")
        self.push_button_title.setFont(QtGui.QFont("Segoe UI", 12))
        self.push_button_title.setFixedHeight(42)
        self.push_button_title.setFocusPolicy(QtCore.Qt.NoFocus)

        self.hbox_layout_main.addWidget(self.push_button_title)

        # кнопка со значком выбора курса
        self.push_button_download = QtWidgets.QPushButton()
        self.push_button_download.setObjectName("push_button_download")
        self.push_button_download.clicked.connect(self.press_choose_course)
        self.push_button_download.setFont(QtGui.QFont("Segoe UI", 12))
        self.push_button_download.setFixedSize(42, 42)
        self.push_button_download.setFocusPolicy(QtCore.Qt.NoFocus)

        self.hbox_layout_main.addWidget(self.push_button_download)

        self.set_style_sheet()

    def change_title(self, text: str):
        self.push_button_title.setText(text)

    def press_choose_course(self):
        self.push_button_clicked_choose_course.emit()

    def init_variables(self):
        self.img_download = QtGui.QIcon(os.path.join(self.path_images, "download.png"))

    def set_style_sheet(self):
        # кнопка с название курса
        self.push_button_title.setStyleSheet("""
        #push_button_title { 
            outline: 0;
            border-top-left-radius: 7px; 
            border-bottom-left-radius: 7px;
            padding-left: 42px;
            background: %(background)s;
            color: %(color)s;
        } """ % self.data_theme)

        # кнопка со значком выбора курса
        self.push_button_download.setStyleSheet("""
        #push_button_download {
            outline: 0;
            border-top-right-radius: 7px; 
            border-bottom-right-radius: 7px; 
            background: %(background)s; 
            color: %(color)s;
        } """ % self.data_theme)
        
        self.push_button_download.setIcon(self.img_download)
        self.push_button_download.setIconSize(QtCore.QSize(42 - 14, 42 - 14))

class StackLogin(QtWidgets.QWidget):
    def __init__(self, path_theme: str, path_courses: str, path_images: str, data_theme: dict, func_start: callable, func_table_results: callable, name: str = None, surname: str = None, class_name: str = None):
        super().__init__()

        self.path_courses = path_courses
        self.path_images = path_images
        self.data_theme = data_theme
        self.func_start = func_start
        self.func_table_results = func_table_results
        self.path_theme = path_theme

        self.name = name
        self.surname = surname
        self.class_name = class_name

        self.init_variables()

        # главная сетка
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

        # внутренняя сетка
        self.grid_layout_internal = QtWidgets.QGridLayout()
        self.grid_layout_internal.setSpacing(0)
        self.grid_layout_internal.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_internal.setColumnStretch(0, 1)
        self.grid_layout_internal.setColumnStretch(1, 0)
        self.grid_layout_internal.setColumnStretch(2, 1)
        self.grid_layout_internal.setRowStretch(0, 1)
        self.grid_layout_internal.setRowStretch(1, 0)
        self.grid_layout_internal.setRowStretch(2, 1)

        self.frame_main.setLayout(self.grid_layout_internal)

        # внутренняя рамка формы
        self.frame_internal = QtWidgets.QFrame()
        self.frame_internal.setObjectName("frame_internal")
        self.frame_internal.setFixedWidth(360)

        self.grid_layout_internal.addWidget(self.frame_internal, 1, 1)

        # макет внутри внутренней рамки
        self.vbox_layout_internal = QtWidgets.QVBoxLayout()
        self.vbox_layout_internal.setSpacing(0)
        self.vbox_layout_internal.setContentsMargins(0, 0, 0, 0)

        self.frame_internal.setLayout(self.vbox_layout_internal)

        # макет для полей ввода и кнопок
        self.vbox_layout_data = QtWidgets.QVBoxLayout()
        self.vbox_layout_data.setSpacing(0)
        self.vbox_layout_data.setContentsMargins(20, 20, 20, 0)

        self.vbox_layout_internal.addLayout(self.vbox_layout_data)

        # метка заголовка
        self.label_header = QtWidgets.QLabel()
        self.label_header.setFont(QtGui.QFont("Segoe UI", 20, weight = QtGui.QFont.Bold))
        self.label_header.setObjectName("label_header")
        self.label_header.setText("Вход")
        self.label_header.setAlignment(QtCore.Qt.AlignCenter)

        self.vbox_layout_data.addWidget(self.label_header)
        self.vbox_layout_data.addSpacing(10)

        # строка ввода фамилии
        self.line_edit_surname = QtWidgets.QLineEdit()
        self.line_edit_surname.setObjectName("line_edit_surname")
        self.line_edit_surname.setFont(QtGui.QFont("Segoe UI", 12))
        self.line_edit_surname.setPlaceholderText("Фамилия")
        self.line_edit_surname.setFixedHeight(42)

        if self.surname != None:
            self.line_edit_surname.insert(self.surname)

        self.vbox_layout_data.addWidget(self.line_edit_surname)
        self.vbox_layout_data.addSpacing(5)

        # строка ввода имени
        self.line_edit_name = QtWidgets.QLineEdit()
        self.line_edit_name.setObjectName("line_edit_name")
        self.line_edit_name.setFont(QtGui.QFont("Segoe UI", 12))
        self.line_edit_name.setPlaceholderText("Имя")
        self.line_edit_name.setFixedHeight(42)

        if self.name != None:
            self.line_edit_name.insert(self.name)

        self.vbox_layout_data.addWidget(self.line_edit_name)
        self.vbox_layout_data.addSpacing(5)

        # строка ввода класса
        self.line_edit_class = QtWidgets.QLineEdit()
        self.line_edit_class.setObjectName("line_edit_class")
        self.line_edit_class.setFont(QtGui.QFont("Segoe UI", 12))
        self.line_edit_class.setPlaceholderText("Класс")
        self.line_edit_class.setFixedHeight(42)

        if self.class_name != None:
            self.line_edit_class.insert(self.class_name)

        self.vbox_layout_data.addWidget(self.line_edit_class)
        self.vbox_layout_data.addSpacing(5)

        # кнопка выбора курса
        self.push_button_course = PushButtonCourse(path_images = self.path_images, data_theme = self.data_theme["frame_main"]["frame_internal"]["push_button_cource"])
        self.push_button_course.push_button_clicked_choose_course.connect(self.choose_course)

        self.vbox_layout_data.addWidget(self.push_button_course)
        self.vbox_layout_data.addSpacing(5)

        # кнопка входа
        self.push_button_enter = QtWidgets.QPushButton()
        self.push_button_enter.setObjectName("push_button_enter")
        self.push_button_enter.setEnabled(False)
        self.push_button_enter.clicked.connect(self.start_test)
        self.push_button_enter.setFont(QtGui.QFont("Segoe UI", 12))
        self.push_button_enter.setText("Войти")
        self.push_button_enter.setFixedHeight(42)
        self.push_button_enter.setFocusPolicy(QtCore.Qt.NoFocus)

        self.vbox_layout_data.addWidget(self.push_button_enter)

        self.vbox_layout_internal.addSpacing(10)

        # кнопка посмотреть таблицу результатов
        self.push_button_table_results = QtWidgets.QPushButton()
        self.push_button_table_results.setObjectName("push_button_table_results")
        self.push_button_table_results.clicked.connect(self.open_table_result)
        self.push_button_table_results.setFont(QtGui.QFont("Segoe UI", 12))
        self.push_button_table_results.setText("Таблица результатов")
        self.push_button_table_results.setFixedHeight(42)
        self.push_button_table_results.setFocusPolicy(QtCore.Qt.NoFocus)

        self.vbox_layout_internal.addWidget(self.push_button_table_results)

        # проверка ввода данных
        self.line_edit_surname.textChanged.connect(self.check_data)
        self.line_edit_name.textChanged.connect(self.check_data)
        self.line_edit_class.textChanged.connect(self.check_data)

        self.set_style_sheet()

    def init_variables(self):
        self.max_len_title_course = 19
        self.path_course = None

    def start_test(self):
        data_passage = DataPassage(
            name = self.line_edit_name.text(),
            surname = self.line_edit_surname.text(),
            class_name = self.line_edit_class.text(),
            path_course = self.path_course
        )

        self.func_start(data = data_passage)

    def open_table_result(self):
        data_passage = DataPassage(
            name = text if (text := self.line_edit_name.text()) != 0 else None,
            surname = text if (text := self.line_edit_surname.text()) != 0 else None,
            class_name = text if (text := self.line_edit_class.text()) != 0 else None,
            path_course = self.path_course
        )

        self.func_table_results(data_passage)

    def choose_course(self):
        # диалог выбора файла с курсом
        path_file_course = QtWidgets.QFileDialog.getOpenFileName(self, "Выбор курса", self.path_courses, "XML Файл (*.xml)")[0]

        if os.path.isfile(path_file_course):
            self.path_course = path_file_course

            self.check_data()
            
            name_course = os.path.splitext(os.path.basename(self.path_course))[0]
            name_course = (name_course[:self.max_len_title_course] + "…") if len(name_course) > self.max_len_title_course else name_course

            self.push_button_course.change_title(name_course)
            self.push_button_course.choosed = True

    def check_data(self):
        # проверка данных
        if self.line_edit_name.text() != "" and self.line_edit_surname.text() != "" and self.line_edit_class.text() != "" and self.path_course != None:
            if os.path.isfile(self.path_course):
                self.push_button_enter.setEnabled(True)
        else:
            self.push_button_enter.setEnabled(False)

    def set_style_sheet(self):
        self.data_theme["frame_main"]["path_background_image"] = os.path.join(os.path.split(self.path_theme)[0], self.data_theme["frame_main"]["background_image"]).replace("\\", "/")

        # главная рамка
        self.frame_main.setStyleSheet("""
        #frame_main {
            background: %(background)s;
            border-image: url(%(path_background_image)s);
            background-repeat: no-repeat; 
            background-position: center;
        } """ % self.data_theme["frame_main"])

        # внутренняя рамка формы
        self.frame_internal.setStyleSheet("""
        #frame_internal {
            border-radius: 14px;
            background: %(background)s;
        } """ % self.data_theme["frame_main"]["frame_internal"])

        # метка заголовка
        self.label_header.setStyleSheet("""
        #label_header {
            background: %(background)s; 
            color: %(color)s
        } """ % self.data_theme["frame_main"]["frame_internal"]["label_header"])
        
        # строка ввода фамилии
        temp_data_theme = {
            "color_border_not_focus": self.data_theme["frame_main"]["frame_internal"]["line_edit_surname"]["not_focus"]["color_border"],
            "background_not_focus": self.data_theme["frame_main"]["frame_internal"]["line_edit_surname"]["not_focus"]["background"], 
            "color_not_focus": self.data_theme["frame_main"]["frame_internal"]["line_edit_surname"]["not_focus"]["color"], 
            "color_border_focus": self.data_theme["frame_main"]["frame_internal"]["line_edit_surname"]["focus"]["color_border"],
            "background_focus": self.data_theme["frame_main"]["frame_internal"]["line_edit_surname"]["focus"]["background"], 
            "color_focus": self.data_theme["frame_main"]["frame_internal"]["line_edit_surname"]["focus"]["color"]
        }

        self.line_edit_surname.setStyleSheet("""
        #line_edit_surname {
            border-radius: 7px; 
            border: 2px solid %(color_border_not_focus)s; 
            background: %(background_not_focus)s; 
            color: %(color_not_focus)s;
        } 
        #line_edit_surname:focus {
            border: 2px solid %(color_border_focus)s; 
            background: %(background_focus)s; 
            color: %(color_focus)s;
        } """ % temp_data_theme)

        # строка ввода имени
        temp_data_theme = {
            "color_border_not_focus": self.data_theme["frame_main"]["frame_internal"]["line_edit_name"]["not_focus"]["color_border"],
            "background_not_focus": self.data_theme["frame_main"]["frame_internal"]["line_edit_name"]["not_focus"]["background"], 
            "color_not_focus": self.data_theme["frame_main"]["frame_internal"]["line_edit_name"]["not_focus"]["color"], 
            "color_border_focus": self.data_theme["frame_main"]["frame_internal"]["line_edit_name"]["focus"]["color_border"],
            "background_focus": self.data_theme["frame_main"]["frame_internal"]["line_edit_name"]["focus"]["background"], 
            "color_focus": self.data_theme["frame_main"]["frame_internal"]["line_edit_name"]["focus"]["color"]
        }

        self.line_edit_name.setStyleSheet("""
        #line_edit_name {
            border-radius: 7px; 
            border: 2px solid %(color_border_not_focus)s; 
            background: %(background_not_focus)s; 
            color: %(color_not_focus)s;
        } 
        #line_edit_name:focus {
            border: 2px solid %(color_border_focus)s; 
            background: %(background_focus)s; 
            color: %(color_focus)s;
        } """ % temp_data_theme)
        
        # строка ввода класса
        temp_data_theme = {
            "color_border_not_focus": self.data_theme["frame_main"]["frame_internal"]["line_edit_class"]["not_focus"]["color_border"],
            "background_not_focus": self.data_theme["frame_main"]["frame_internal"]["line_edit_class"]["not_focus"]["background"], 
            "color_not_focus": self.data_theme["frame_main"]["frame_internal"]["line_edit_class"]["not_focus"]["color"], 
            "color_border_focus": self.data_theme["frame_main"]["frame_internal"]["line_edit_class"]["focus"]["color_border"],
            "background_focus": self.data_theme["frame_main"]["frame_internal"]["line_edit_class"]["focus"]["background"], 
            "color_focus": self.data_theme["frame_main"]["frame_internal"]["line_edit_class"]["focus"]["color"]
        }

        self.line_edit_class.setStyleSheet("""
        #line_edit_class {
            border-radius: 7px;
            border: 2px solid %(color_border_not_focus)s; 
            background: %(background_not_focus)s; 
            color: %(color_not_focus)s;
        } 
        #line_edit_class:focus {
            border: 2px solid %(color_border_focus)s; 
            background: %(background_focus)s; 
            color: %(color_focus)s;
        } """ % temp_data_theme)
        
        # кнопка входа
        self.push_button_enter.setStyleSheet("""
        #push_button_enter {
            outline: 0;
            border-radius: 7px; 
            background: %(background)s; 
            color: %(color)s;
        } 
        #push_button_enter::pressed {
            background: %(background_pressed)s; 
            color: %(color)s;
        }
        #push_button_enter::disabled {
            background: %(background_disabled)s;
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["frame_internal"]["push_button_enter"])

        # кнопка посмотреть таблицу результатов
        self.push_button_table_results.setStyleSheet("""
        #push_button_table_results {
            outline: 0;
            border-bottom-left-radius: 14px; 
            border-bottom-right-radius: 14px; 
            background: %(background)s; 
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["push_button_table_results"])
