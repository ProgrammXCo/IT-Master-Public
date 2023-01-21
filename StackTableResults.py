from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import datetime 
import re

class StackTableResults(QtWidgets.QWidget):
    def __init__(self, path_database: str, func: callable, data_theme: dict):
        super().__init__()

        self.path_database = path_database
        self.func = func
        self.data_theme = data_theme
        
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

        # внутренний макет
        self.vbox_layout_internal = QtWidgets.QVBoxLayout()
        self.vbox_layout_internal.setSpacing(0)
        self.vbox_layout_internal.setContentsMargins(0, 0, 0, 0)

        self.frame_main.setLayout(self.vbox_layout_internal)

        # рамка заголовка
        self.frame_header = QtWidgets.QFrame()
        self.frame_header.setObjectName("frame_header")

        self.vbox_layout_internal.addWidget(self.frame_header)

        # макет заголовка
        self.hbox_layout_header = QtWidgets.QHBoxLayout()
        self.hbox_layout_header.setSpacing(0)
        self.hbox_layout_header.setContentsMargins(20, 10, 20, 10)

        self.frame_header.setLayout(self.hbox_layout_header)

        self.hbox_layout_header.addStretch(1)

        # метка заголовка
        self.label_header = QtWidgets.QLabel()
        self.label_header.setFont(QtGui.QFont("Segoe UI", 17, weight = QtGui.QFont.Bold))
        self.label_header.setObjectName("label_header")
        self.label_header.setText("Таблица результатов")
        self.label_header.setAlignment(QtCore.Qt.AlignCenter)

        self.hbox_layout_header.addWidget(self.label_header)
        self.hbox_layout_header.addStretch(1)

        # таблица результатов
        self.table_results = QtWidgets.QTableWidget()
        self.table_results.setObjectName("table_results")
        self.table_results.setColumnCount(10)
        self.table_results.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_results.setFont(QtGui.QFont("Segoe UI", 12))
        self.table_results.horizontalHeader().setFont(QtGui.QFont("Segoe UI", 12))
        self.table_results.verticalHeader().setFont(QtGui.QFont("Segoe UI", 12))
        self.table_results.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table_results.verticalHeader().setVisible(False)

        self.vbox_layout_internal.addWidget(self.table_results)

        # рамка панели инстументов
        self.frame_tools = QtWidgets.QFrame()
        self.frame_tools.setObjectName("frame_tools")
        
        self.vbox_layout_internal.addWidget(self.frame_tools)

        # макет панели инструментов
        self.hbox_layout_tools = QtWidgets.QHBoxLayout()
        self.hbox_layout_tools.setSpacing(0)
        self.hbox_layout_tools.setContentsMargins(20, 10, 20, 10)

        self.frame_tools.setLayout(self.hbox_layout_tools)

        self.hbox_layout_tools.addStretch(1)

        # кнопка на главную
        self.push_button_to_main = QtWidgets.QPushButton()
        self.push_button_to_main.setObjectName("push_button_to_main")
        self.push_button_to_main.clicked.connect(self.func)
        self.push_button_to_main.setFont(QtGui.QFont("Segoe UI", 14))
        self.push_button_to_main.setMinimumHeight(42)
        self.push_button_to_main.setText("На главную")

        self.hbox_layout_tools.addWidget(self.push_button_to_main)
        self.hbox_layout_tools.addStretch(1)

        # заполнение таблицы
        self.create_table_results()

        self.set_style_sheet()

    def init_variables(self):
        pattern = re.compile(r"^\s*rgb\s*\(\s*|\s*,\s*|\s*\)\s*$")

        self.background_even_item_table = QtGui.QColor(*[int(i) for i in pattern.split(self.data_theme["frame_main"]["table_results"]["even_item"]["background"])[1:-1]])
        self.color_even_item_table = QtGui.QColor(*[int(i) for i in pattern.split(self.data_theme["frame_main"]["table_results"]["even_item"]["color"])[1:-1]])

        self.background_odd_item_table = QtGui.QColor(*[int(i) for i in pattern.split(self.data_theme["frame_main"]["table_results"]["odd_item"]["background"])[1:-1]])
        self.color_odd_item_table = QtGui.QColor(*[int(i) for i in pattern.split(self.data_theme["frame_main"]["table_results"]["odd_item"]["color"])[1:-1]])

    def create_table_results(self):
        self.table_results.setHorizontalHeaderLabels([
            "Время начала",
            "Время прохождения",
            "Имя",
            "Фамилия",
            "Класс",
            "Урок",
            "Результат",
            "Верных",
            "Неверных",
            "Пропущенных"
        ])

        with sqlite3.connect(self.path_database) as db:
            cursor = db.cursor()

            cursor.execute("""SELECT * FROM users""")

            list_users = cursor.fetchall()
            list_users.sort(key = lambda x: x[0], reverse = True) 

            self.table_results.setRowCount(len(list_users))

            for row in range(len(list_users)):
                data = list_users[row]
                list_table_items = []

                # время начала
                list_table_items.append(datetime.datetime.strptime(data[0], r"%Y.%m.%d %H:%M").strftime(r"%d.%m.%Y %H:%M"))

                # время прохождения
                date_start = datetime.datetime.strptime(data[0], r"%Y.%m.%d %H:%M")
                date_end = datetime.datetime.strptime(data[1], r"%Y.%m.%d %H:%M")

                time_delta = date_end - date_start
                time_duration = int(time_delta.total_seconds() // 60)

                list_table_items.append(f"{time_duration} минут")

                # фамилия
                list_table_items.append(data[2])

                # имя
                list_table_items.append(data[3])

                # класс
                list_table_items.append(data[4])

                # урок
                list_table_items.append(data[5])

                # результат
                list_table_items.append(f"{data[10]} %")

                # верных
                list_table_items.append(str(data[7]))

                # неверных
                list_table_items.append(str(data[8]))

                # пропущенных
                list_table_items.append(str(data[9]))

                # чередование цветов строк
                if row % 2 == 0:
                    background = self.background_even_item_table
                    color = self.color_even_item_table
                else:
                    background = self.background_odd_item_table
                    color = self.color_odd_item_table

                for i in range(10):
                    table_item = QtWidgets.QTableWidgetItem(list_table_items[i])
                    self.table_results.setItem(row, i, table_item)

                    table_item.setBackground(background)
                    table_item.setForeground(color)

        self.table_results.resizeColumnsToContents()

    def set_style_sheet(self):
        # главная рамка
        self.frame_main.setStyleSheet("""
        #frame_main {
            background: %(background)s;
        } """ % self.data_theme["frame_main"])

        # рамка заголовка
        self.frame_header.setStyleSheet("""
        #frame_header {
            border-bottom-right-radius: 40px;
            background: %(background)s;
        } """ % self.data_theme["frame_main"]["frame_header"])

        # метка заголовка
        self.label_header.setStyleSheet("""
        #label_header {
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["frame_header"]["label_header"])

        # рамка панели инстументов
        self.frame_tools.setStyleSheet("""
        #frame_tools {
            border-top-left-radius: 40px;
            border-top-right-radius: 40px;
            background: %(background)s;
        } """ % self.data_theme["frame_main"]["frame_tools"])

        # кнопка на главную
        self.push_button_to_main.setStyleSheet("""
        #push_button_to_main {
            outline: 0;
            border-radius: 7px; 
            padding-left: 10px;
            padding-right: 10px;
            background: %(background)s; 
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["frame_tools"]["push_button_to_main"])

        # таблица результатов        
        self.table_results.horizontalHeader().setStyleSheet("""
        ::section:horizontal {
            background: %(background)s;
            color: %(color)s;
            border: none;
        } """ % self.data_theme["frame_main"]["table_results"]["header"])

        self.table_results.verticalHeader().setStyleSheet("""
        ::section:vertical {
            background:  %(background)s;
            color: %(color)s;
            border: none;
        } """ % self.data_theme["frame_main"]["table_results"]["header"])

        self.data_theme["frame_main"]["table_results"]["background_selected"] = self.data_theme["frame_main"]["table_results"]["selected_item"]["background"]
        self.data_theme["frame_main"]["table_results"]["color_selected"] = self.data_theme["frame_main"]["table_results"]["selected_item"]["color"]

        self.table_results.setStyleSheet("""
        QHeaderView {
            background: %(background)s;
        }      
        #table_results {
            background: %(background)s;
            gridline-color: %(color_gridline)s;
            border: none;
        }
        #table_results::item::selected {
            background: %(background_selected)s;
            color: %(color_selected)s;
        } """ % self.data_theme["frame_main"]["table_results"])

        # полоса прокрутки
        self.data_theme["frame_main"]["table_results"]["scrollbar"]["background_handle"] = self.data_theme["frame_main"]["table_results"]["scrollbar"]["handle"]["background"]

        self.setStyleSheet("""
        QScrollBar:vertical {
            background: %(background)s;
            width: 20px;
            margin: 0px 0px 0px 0px;
            border: none;
        }
        QScrollBar::handle:vertical {
            background: %(background_handle)s;         
            min-height: 20px;
            border-radius: 10px;
        }
        QScrollBar::sub-line:vertical {
            border: none;
            background: none;
        }
        QScrollBar::add-line:vertical {
            border: none;
            background: none;
        }
        QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {
            border: none;
            background: none;
        }
        QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {
            border: none;
            background: none;
        }
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
        
        QScrollBar:horizontal {
            background: %(background)s;
            height: 20px;
            margin: 0px 0px 0px 0px;
            border: none;
        }
        QScrollBar::handle:horizontal {
            background: %(background_handle)s;         
            min-width: 20px;
            border-radius: 10px;
        }
        QScrollBar::sub-line:horizontal {
            border: none;
            background: none;
        }
        QScrollBar::add-line:horizontal {
            border: none;
            background: none;
        }
        QScrollBar::sub-line:horizontal:hover,QScrollBar::sub-line:horizontal:on {
            border: none;
            background: none;
        }
        QScrollBar::add-line:horizontal:hover, QScrollBar::add-line:horizontal:on {
            border: none;
            background: none;
        }
        QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:horizontal {
            background: none;
        }
        """ % self.data_theme["frame_main"]["table_results"]["scrollbar"])
