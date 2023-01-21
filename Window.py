from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Window(QtWidgets.QMainWindow):
    window_close = QtCore.pyqtSignal()
    window_minimize = QtCore.pyqtSignal()
    open_info = QtCore.pyqtSignal()
    def __init__(self, data_theme: dict):
        super().__init__()
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        self.__data_theme = data_theme

        # главная рамка
        self.frame_main = QtWidgets.QFrame()
        self.frame_main.setObjectName("frame_main")

        self.setCentralWidget(self.frame_main)

        # внутренний макет
        self.vbox_layout_internal = QtWidgets.QVBoxLayout()
        self.vbox_layout_internal.setContentsMargins(0, 0, 0, 0)
        self.vbox_layout_internal.setSpacing(0)

        self.frame_main.setLayout(self.vbox_layout_internal)

        # рамка заголовка
        self.frame_title = QtWidgets.QFrame()
        self.frame_title.setObjectName("frame_title")
        self.frame_title.setFixedHeight(36)

        self.vbox_layout_internal.addWidget(self.frame_title)

        # макет рамки заголовка
        self.hbox_layout_title = QtWidgets.QHBoxLayout()
        self.hbox_layout_title.setContentsMargins(5, 0, 0, 0)
        self.hbox_layout_title.setSpacing(0)

        self.frame_title.setLayout(self.hbox_layout_title)

        # метка иконки
        self.label_icon = QtWidgets.QLabel()
        self.label_icon.setObjectName("label_icon")
        self.label_icon.setAlignment(QtCore.Qt.AlignCenter)
        self.label_icon.setFixedSize(25, 25)

        self.hbox_layout_title.addWidget(self.label_icon)
        self.hbox_layout_title.addSpacing(5)

        # метка титла
        self.label_title = QtWidgets.QLabel()
        self.label_title.setObjectName("label_title")
        self.label_title.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_title.setFont(QtGui.QFont("Trebuchet MS", 10, weight = QtGui.QFont.Bold))

        self.hbox_layout_title.addWidget(self.label_title)
        self.hbox_layout_title.addStretch(1)

        # кнопка о программе
        self.push_button_info = QtWidgets.QPushButton()
        self.push_button_info.setObjectName("push_button_info")
        self.push_button_info.clicked.connect(self.clicked_push_button_info)
        self.push_button_info.setFont(QtGui.QFont("Webdings", 9))
        self.push_button_info.setText("s")
        self.push_button_info.setFixedSize(58, 36)
        self.push_button_info.setFocusPolicy(QtCore.Qt.NoFocus)

        self.hbox_layout_title.addWidget(self.push_button_info)

        # кнопка свернуть
        self.push_button_minimize = QtWidgets.QPushButton()
        self.push_button_minimize.setObjectName("push_button_minimize")
        self.push_button_minimize.clicked.connect(self.clicked_push_button_minimize)
        self.push_button_minimize.setFont(QtGui.QFont("Webdings", 9))
        self.push_button_minimize.setText("0")
        self.push_button_minimize.setFixedSize(58, 36)
        self.push_button_minimize.setFocusPolicy(QtCore.Qt.NoFocus)

        self.hbox_layout_title.addWidget(self.push_button_minimize)

        # кнопка закрыть программу
        self.push_button_close = QtWidgets.QPushButton()
        self.push_button_close.setObjectName("push_button_close")
        self.push_button_close.clicked.connect(self.clicked_push_button_exit)
        self.push_button_close.setFont(QtGui.QFont("Webdings", 9))
        self.push_button_close.setText("r")
        self.push_button_close.setFixedSize(58, 36)
        self.push_button_close.setFocusPolicy(QtCore.Qt.NoFocus)

        self.hbox_layout_title.addWidget(self.push_button_close)

        # рамка для виджетов
        self.frame_widgets = QtWidgets.QFrame()
        self.frame_widgets.setObjectName("frame_widgets")

        self.vbox_layout_internal.addWidget(self.frame_widgets)

        # макет для виджетов
        self.hbox_layout_widget = QtWidgets.QHBoxLayout()
        self.hbox_layout_widget.setContentsMargins(0, 0, 0, 0)
        self.hbox_layout_widget.setSpacing(0)

        self.frame_widgets.setLayout(self.hbox_layout_widget)

        # присоединения слотов к сигналам
        self.window_close.connect(self.close_window)
        self.window_minimize.connect(self.minimize_window)

        self.set_style_sheet()
    
    def clicked_push_button_minimize(self):
        self.window_minimize.emit()

    def clicked_push_button_info(self):
        self.open_info.emit()

    def clicked_push_button_exit(self):
        self.window_close.emit()

    def close_window(self):
        sys.exit()

    def minimize_window(self):
        super().showMinimized()

    def show_window(self):
        super().showMaximized()

    def set_icon(self, icon: QtGui.QPixmap):
        icon = icon.scaled(25, 25, transformMode = QtCore.Qt.SmoothTransformation)
        self.label_icon.setPixmap(icon)

    def set_title(self, title: str):
        self.label_title.setText(title)

    def add_widget(self, widget: QtWidgets.QWidget):
        self.hbox_layout_widget.addWidget(widget)

    def set_style_sheet(self):
        # рамка заголовка
        self.frame_title.setStyleSheet("""
        #frame_title {
            background: %(background)s;
        } """ % self.__data_theme["frame_title"])

        # метка титла
        self.label_title.setStyleSheet("""
        #label_title {
            color: %(color)s;
        } """ % self.__data_theme["frame_title"]["label_title"])
        
        # кнопка о программе
        temp_data_theme = {
            "background_normal": self.__data_theme["frame_title"]["push_button_info"]["normal"]["background"],
            "color_normal": self.__data_theme["frame_title"]["push_button_info"]["normal"]["color"], 
            "background_hover": self.__data_theme["frame_title"]["push_button_info"]["hover"]["background"], 
            "color_hover": self.__data_theme["frame_title"]["push_button_info"]["hover"]["color"],
            "background_press": self.__data_theme["frame_title"]["push_button_info"]["press"]["background"], 
            "color_press": self.__data_theme["frame_title"]["push_button_info"]["press"]["color"]
        }

        self.push_button_info.setStyleSheet("""
        #push_button_info {
            outline: 0;
            border: none;
            background: %(background_normal)s; 
            color: %(color_normal)s;
        }
        #push_button_info::hover {
            background: %(background_hover)s; 
            color: %(color_hover)s;
        }
        #push_button_info::pressed {
            background: %(background_press)s; 
            color: %(color_press)s; 
        } """ % temp_data_theme)

        # кнопка свернуть
        temp_data_theme = {
            "background_normal": self.__data_theme["frame_title"]["push_button_minimize"]["normal"]["background"],
            "color_normal": self.__data_theme["frame_title"]["push_button_minimize"]["normal"]["color"], 
            "background_hover": self.__data_theme["frame_title"]["push_button_minimize"]["hover"]["background"], 
            "color_hover": self.__data_theme["frame_title"]["push_button_minimize"]["hover"]["color"],
            "background_press": self.__data_theme["frame_title"]["push_button_minimize"]["press"]["background"], 
            "color_press": self.__data_theme["frame_title"]["push_button_minimize"]["press"]["color"]
        }

        self.push_button_minimize.setStyleSheet("""
        #push_button_minimize {
            outline: 0;
            border: none;
            background: %(background_normal)s; 
            color: %(color_normal)s;
        }
        #push_button_minimize::hover {
            background: %(background_hover)s; 
            color: %(color_hover)s;
        }
        #push_button_minimize::pressed {
            background: %(background_press)s; 
            color: %(color_press)s; 
        } """ % temp_data_theme)

        # кнопка закрыть программу
        temp_data_theme = {
            "background_normal": self.__data_theme["frame_title"]["push_button_close"]["normal"]["background"],
            "color_normal": self.__data_theme["frame_title"]["push_button_close"]["normal"]["color"], 
            "background_hover": self.__data_theme["frame_title"]["push_button_close"]["hover"]["background"], 
            "color_hover": self.__data_theme["frame_title"]["push_button_close"]["hover"]["color"],
            "background_press": self.__data_theme["frame_title"]["push_button_close"]["press"]["background"], 
            "color_press": self.__data_theme["frame_title"]["push_button_close"]["press"]["color"]
        }

        self.push_button_close.setStyleSheet("""
        #push_button_close {
            outline: 0;
            border: none;
            background: %(background_normal)s; 
            color: %(color_normal)s;
        }
        #push_button_close::hover {
            background: %(background_hover)s; 
            color: %(color_hover)s;
        }
        #push_button_close::pressed {
            background: %(background_press)s; 
            color: %(color_press)s; 
        } """ % temp_data_theme)

        # макет для виджетов
        self.frame_widgets.setStyleSheet("""
        #frame_widgets {
            background: %(background)s;
        } """ % self.__data_theme["frame_widgets"])
