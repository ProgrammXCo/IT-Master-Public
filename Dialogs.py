from PyQt5 import QtCore, QtGui, QtWidgets
import re

class ImageGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, path_image: str, data_theme: dict):
        super().__init__()

        self.data_theme = data_theme
        self.path_image = path_image

        self.init_variables()

        self.image = QtWidgets.QGraphicsPixmapItem()
        self.image.setTransformationMode(QtCore.Qt.SmoothTransformation) 

        self.graphics_scene = QtWidgets.QGraphicsScene()
        self.graphics_scene.addItem(self.image)

        self.setScene(self.graphics_scene)

        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.HighQualityAntialiasing)

        self.set_style_sheet()

    def init_variables(self):
        self.min_zoom = None
        self.max_zoom = None
        self.zoom = None

        pattern = re.compile(r"^\s*rgb\s*\(\s*|\s*,\s*|\s*\)\s*$")

        self.background = QtGui.QColor(*[int(i) for i in pattern.split(self.data_theme["background"])[1:-1]])

    def fit_in_view(self):
        rect = QtCore.QRectF(self.image.pixmap().rect())

        self.setSceneRect(rect)

        unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
        self.scale(1 / unity.width(), 1 / unity.height())
        view_rect = self.viewport().rect()
        scene_rect = self.transform().mapRect(rect)

        self.min_zoom = min(view_rect.width() / scene_rect.width(), view_rect.height() / scene_rect.height())
        self.max_zoom = max(view_rect.width() / scene_rect.width(), view_rect.height() / scene_rect.height())

        self.zoom = self.min_zoom

        self.scale(self.zoom, self.zoom)

    def set_image(self):
        self.image.setPixmap(QtGui.QPixmap(self.path_image))

        self.fit_in_view()

    def wheelEvent(self, event):
        current_zoom = self.zoom
        if event.angleDelta().y() > 0 and self.zoom < self.max_zoom:
            factor = 1.25
            self.zoom *= factor
            if self.zoom > self.max_zoom:
                self.zoom = self.max_zoom
                factor = self.zoom / current_zoom
            self.scale(factor, factor)
        elif  event.angleDelta().y() < 0 and self.zoom > self.min_zoom:
            factor = 0.8
            self.zoom *= factor
            if self.zoom < self.min_zoom:
                self.zoom = self.min_zoom
                factor = self.zoom / current_zoom
            self.scale(factor, factor)

    def set_style_sheet(self):
        # фоновый цвет холста
        self.setBackgroundBrush(self.background)

class DialogImage(QtWidgets.QDialog):
    window_close = QtCore.pyqtSignal()
    def __init__(self, path_image: str, data_theme: dict, parent = None):
        self.parent = parent
        self.data_theme = data_theme
        self.path_image = path_image

        super().__init__(self.parent)
        self.setContentsMargins(7, 7, 7, 7)
        
        self.setWindowTitle('Изображение')
        self.setModal(True)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

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
        self.frame_main.setFixedSize(700, 600)
        self.frame_main.setObjectName("frame_main")

        self.grid_layout_main.addWidget(self.frame_main, 1, 1)

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

        # кнопка закрыть
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

        # сетка для виджетов
        self.grid_layout_widget = QtWidgets.QGridLayout()
        self.grid_layout_widget.setSpacing(0)
        self.grid_layout_widget.setContentsMargins(5, 5, 5, 5)
        self.grid_layout_widget.setColumnStretch(0, 0)
        self.grid_layout_widget.setColumnStretch(1, 1)
        self.grid_layout_widget.setColumnStretch(2, 0)
        self.grid_layout_widget.setRowStretch(0, 0)
        self.grid_layout_widget.setRowStretch(1, 1)
        self.grid_layout_widget.setRowStretch(2, 0)

        self.frame_widgets.setLayout(self.grid_layout_widget)

        # виджет просмотра изображений
        self.image_viewer = ImageGraphicsView(path_image = self.path_image, data_theme = self.data_theme["frame_widgets"]["image_graphics_view"])

        self.grid_layout_widget.addWidget(self.image_viewer, 1, 1)

        # присоединения слотов к сигналам
        self.window_close.connect(self.close_window)

        self.set_style_sheet()

        self.show()
  
        self.move(QtCore.QPoint(self.parent.geometry().getCoords()[0], self.parent.geometry().getCoords()[1]) + self.parent.rect().center() - self.rect().center())

    def load_lesson(self):
        self.image_viewer.set_image()

    def clicked_push_button_exit(self):
        self.window_close.emit()

    def close_window(self):
        self.close()

    def set_icon(self, icon: QtGui.QPixmap):
        icon = icon.scaled(25, 25, transformMode = QtCore.Qt.SmoothTransformation)
        self.label_icon.setPixmap(icon)

    def set_title(self, title: str):
        self.label_title.setText(title)

    def set_style_sheet(self):
        # рамка заголовка
        self.frame_title.setStyleSheet("""
        #frame_title {
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            background: %(background)s;
        } """ % self.data_theme["frame_title"])

        # метка титла
        self.label_title.setStyleSheet("""
        #label_title {
            color: %(color)s;
        } """ % self.data_theme["frame_title"]["label_title"])

        # кнопка закрыть программу
        temp_data_theme = {
            "background_normal": self.data_theme["frame_title"]["push_button_close"]["normal"]["background"],
            "color_normal": self.data_theme["frame_title"]["push_button_close"]["normal"]["color"], 
            "background_hover": self.data_theme["frame_title"]["push_button_close"]["hover"]["background"], 
            "color_hover": self.data_theme["frame_title"]["push_button_close"]["hover"]["color"],
            "background_press": self.data_theme["frame_title"]["push_button_close"]["press"]["background"], 
            "color_press": self.data_theme["frame_title"]["push_button_close"]["press"]["color"]
        }

        self.push_button_close.setStyleSheet("""
        #push_button_close {
            border-top-right-radius: 10px;
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
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
            background: %(background)s;
        } """ % self.data_theme["frame_widgets"])

        # тень
        self.frame_main.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.frame_main.shadow.setBlurRadius(17)
        self.frame_main.shadow.setOffset(0, 0)
        self.frame_main.shadow.setColor(QtGui.QColor(0, 0, 0, 100))
        self.frame_main.setGraphicsEffect(self.frame_main.shadow)

class DialogTableResultsEmpty(QtWidgets.QDialog):
    push_button_clicked_ok = QtCore.pyqtSignal()
    def __init__(self, data_theme: dict, parent = None):
        self.parent = parent

        super().__init__(self.parent)
        self.setContentsMargins(7, 7, 7, 7)

        self.data_theme = data_theme
        
        self.setWindowTitle('Выход')
        self.setModal(True)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.FramelessWindowHint
        )

        # главная сетка
        self.grid_layout_main = QtWidgets.QGridLayout()
        self.grid_layout_main.setSpacing(0)
        self.grid_layout_main.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_main.setRowStretch(0, 0)
        self.grid_layout_main.setRowStretch(1, 1)
        self.grid_layout_main.setRowStretch(2, 0)
        self.grid_layout_main.setColumnStretch(0, 0)
        self.grid_layout_main.setColumnStretch(1, 1)
        self.grid_layout_main.setColumnStretch(2, 0)

        self.setLayout(self.grid_layout_main)

        # главная рамка
        self.frame_main = QtWidgets.QFrame()
        self.frame_main.setObjectName("frame_main")
        self.frame_main.setContentsMargins(30, 20, 30, 30)
        self.frame_main.setFixedWidth(440)

        self.grid_layout_main.addWidget(self.frame_main, 1, 1)

        # внутренний макет
        self.vbox_layout_internal = QtWidgets.QVBoxLayout()
        self.vbox_layout_internal.setSpacing(0)
        self.vbox_layout_internal.setContentsMargins(0, 0, 0, 0)

        self.frame_main.setLayout(self.vbox_layout_internal)

        # метка заголовка
        self.label_header = QtWidgets.QLabel()
        self.label_header.setFont(QtGui.QFont("Segoe UI", 20, weight = QtGui.QFont.Bold))
        self.label_header.setObjectName("label_header")
        self.label_header.setText("Действие невозможно")
        self.label_header.setWordWrap(True)
        self.label_header.setAlignment(QtCore.Qt.AlignCenter)

        self.vbox_layout_internal.addWidget(self.label_header)
        self.vbox_layout_internal.addSpacing(10)

        # метка подсказки
        self.label_hint = QtWidgets.QLabel()
        self.label_hint.setFont(QtGui.QFont("Segoe UI", 12))
        self.label_hint.setObjectName("label_hint")
        self.label_hint.setText("В таблице результатов ещё нет записей")
        self.label_hint.setWordWrap(True)
        self.label_hint.setAlignment(QtCore.Qt.AlignCenter)

        self.vbox_layout_internal.addWidget(self.label_hint)
        self.vbox_layout_internal.addSpacing(20)

        # макет инстументов
        self.hbox_layout_tools = QtWidgets.QHBoxLayout()
        self.hbox_layout_tools.setSpacing(0)
        self.hbox_layout_tools.setContentsMargins(0, 0, 0, 0)

        self.vbox_layout_internal.addLayout(self.hbox_layout_tools)

        self.hbox_layout_tools.addStretch(1)

        # кнопка ок
        self.push_button_ok = QtWidgets.QPushButton()
        self.push_button_ok.setObjectName("push_button_ok")
        self.push_button_ok.clicked.connect(self.clicked_push_button_ok)
        self.push_button_ok.setFont(QtGui.QFont("Segoe UI", 12))
        self.push_button_ok.setFixedSize(142, 42)
        self.push_button_ok.setText("Ок")
        self.push_button_ok.setFocusPolicy(QtCore.Qt.NoFocus)

        self.hbox_layout_tools.addWidget(self.push_button_ok)

        self.set_style_sheet()

        self.show()
  
        self.move(QtCore.QPoint(self.parent.geometry().getCoords()[0], self.parent.geometry().getCoords()[1]) + self.parent.rect().center() - self.rect().center())

    def clicked_push_button_ok(self):
        self.close()
        self.push_button_clicked_ok.emit()

    def set_style_sheet(self):
        # главная рамка
        self.frame_main.setStyleSheet("""
        #frame_main {
            border-radius: 14px;
            border: none;
            background: %(background)s;
        } """ % self.data_theme["frame_main"])

        # метка заголовка
        self.label_header.setStyleSheet("""
        #label_header {
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["label_header"])

        # метка подсказки
        self.label_hint.setStyleSheet("""
        #label_hint {
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["label_hint"])

        # кнопка ок
        self.push_button_ok.setStyleSheet("""
        #push_button_ok {
            outline: 0;
            border-radius: 7px;
            border: none;
            background: %(background)s; 
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["push_button_ok"])

        # тень
        self.frame_main.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.frame_main.shadow.setBlurRadius(17)
        self.frame_main.shadow.setOffset(0, 0)
        self.frame_main.shadow.setColor(QtGui.QColor(0, 0, 0, 100))
        self.frame_main.setGraphicsEffect(self.frame_main.shadow)

class DialogExit(QtWidgets.QDialog):
    push_button_clicked_exit = QtCore.pyqtSignal()
    push_button_clicked_cancel = QtCore.pyqtSignal()
    def __init__(self, data_theme: dict, parent = None):
        self.parent = parent

        super().__init__(self.parent)
        self.setContentsMargins(7, 7, 7, 7)

        self.data_theme = data_theme
        
        self.setWindowTitle('Выход')
        self.setModal(True)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        # главная сетка
        self.grid_layout_main = QtWidgets.QGridLayout()
        self.grid_layout_main.setSpacing(0)
        self.grid_layout_main.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_main.setRowStretch(0, 0)
        self.grid_layout_main.setRowStretch(1, 1)
        self.grid_layout_main.setRowStretch(2, 0)
        self.grid_layout_main.setColumnStretch(0, 0)
        self.grid_layout_main.setColumnStretch(1, 1)
        self.grid_layout_main.setColumnStretch(2, 0)

        self.setLayout(self.grid_layout_main)

        # главная рамка
        self.frame_main = QtWidgets.QFrame()
        self.frame_main.setObjectName("frame_main")
        self.frame_main.setContentsMargins(30, 20, 30, 30)
        self.frame_main.setFixedWidth(370)

        self.grid_layout_main.addWidget(self.frame_main, 1, 1)

        # внутренний макет
        self.vbox_layout_internal = QtWidgets.QVBoxLayout()
        self.vbox_layout_internal.setSpacing(0)
        self.vbox_layout_internal.setContentsMargins(0, 0, 0, 0)

        self.frame_main.setLayout(self.vbox_layout_internal)

        # метка заголовка
        self.label_header = QtWidgets.QLabel()
        self.label_header.setFont(QtGui.QFont("Segoe UI", 20, weight = QtGui.QFont.Bold))
        self.label_header.setObjectName("label_header")
        self.label_header.setText("Выйти из теста?")
        self.label_header.setWordWrap(True)
        self.label_header.setAlignment(QtCore.Qt.AlignCenter)

        self.vbox_layout_internal.addWidget(self.label_header)
        self.vbox_layout_internal.addSpacing(10)

        # метка подсказки
        self.label_hint = QtWidgets.QLabel()
        self.label_hint.setFont(QtGui.QFont("Segoe UI", 12))
        self.label_hint.setObjectName("label_hint")
        self.label_hint.setText("Результаты не сохранятся")
        self.label_hint.setWordWrap(True)
        self.label_hint.setAlignment(QtCore.Qt.AlignCenter)

        self.vbox_layout_internal.addWidget(self.label_hint)
        self.vbox_layout_internal.addSpacing(20)

        # макет инстументов
        self.hbox_layout_tools = QtWidgets.QHBoxLayout()
        self.hbox_layout_tools.setSpacing(0)
        self.hbox_layout_tools.setContentsMargins(0, 0, 0, 0)

        self.vbox_layout_internal.addLayout(self.hbox_layout_tools)

        # кнопка отменить
        self.push_button_cancel = QtWidgets.QPushButton()
        self.push_button_cancel.setObjectName("push_button_cancel")
        self.push_button_cancel.clicked.connect(self.clicked_push_button_cancel)
        self.push_button_cancel.setFont(QtGui.QFont("Segoe UI", 12))
        self.push_button_cancel.setFixedHeight(42)
        self.push_button_cancel.setText("Отмена")
        self.push_button_cancel.setFocusPolicy(QtCore.Qt.NoFocus)

        self.hbox_layout_tools.addWidget(self.push_button_cancel)
        self.hbox_layout_tools.addSpacing(15)

        # кнопка выход
        self.push_button_exit = QtWidgets.QPushButton()
        self.push_button_exit.setObjectName("push_button_exit")
        self.push_button_exit.clicked.connect(self.clicked_push_button_exit)
        self.push_button_exit.setFont(QtGui.QFont("Segoe UI", 12))
        self.push_button_exit.setFixedHeight(42)
        self.push_button_exit.setText("Выйти")
        self.push_button_exit.setFocusPolicy(QtCore.Qt.NoFocus)

        self.hbox_layout_tools.addWidget(self.push_button_exit)

        self.set_style_sheet()

        self.show()
  
        self.move(QtCore.QPoint(self.parent.geometry().getCoords()[0], self.parent.geometry().getCoords()[1]) + self.parent.rect().center() - self.rect().center())

    def clicked_push_button_exit(self):
        self.close()
        self.push_button_clicked_exit.emit()

    def clicked_push_button_cancel(self):
        self.close()
        self.push_button_clicked_cancel.emit()

    def set_style_sheet(self):
        # главная рамка
        self.frame_main.setStyleSheet("""
        #frame_main {
            border-radius: 14px;
            border: none;
            background: %(background)s;
        } """ % self.data_theme["frame_main"])

        # метка заголовка
        self.label_header.setStyleSheet("""
        #label_header {
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["label_header"])

        # метка подсказки
        self.label_hint.setStyleSheet("""
        #label_hint {
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["label_hint"])

        # кнопка остаться
        self.push_button_cancel.setStyleSheet("""
        #push_button_cancel {
            outline: 0;
            border-radius: 7px;
            border: none;
            background: %(background)s; 
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["push_button_cancel"])

        # кнопка выйти
        self.push_button_exit.setStyleSheet("""
        #push_button_exit {
            outline: 0;
            border-radius: 7px;
            border: none;
            background: %(background)s; 
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["push_button_exit"])

        # тень
        self.frame_main.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.frame_main.shadow.setBlurRadius(17)
        self.frame_main.shadow.setOffset(0, 0)
        self.frame_main.shadow.setColor(QtGui.QColor(0, 0, 0, 100))
        self.frame_main.setGraphicsEffect(self.frame_main.shadow)

class DialogInfo(QtWidgets.QDialog):
    push_button_clicked_ok = QtCore.pyqtSignal()
    def __init__(self, data_theme: dict, version: str, name: str, text_info: str, path_logo: str, parent = None):
        self.parent = parent

        super().__init__(self.parent)
        self.setContentsMargins(7, 7, 7, 7)

        self.data_theme = data_theme
        self.path_logo = path_logo
        self.version = version
        self.name = name
        self.text_info = text_info
        
        self.setWindowTitle('О программе')
        self.setModal(True)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        # главная сетка
        self.grid_layout_main = QtWidgets.QGridLayout()
        self.grid_layout_main.setSpacing(0)
        self.grid_layout_main.setContentsMargins(0, 0, 0, 0)
        self.grid_layout_main.setRowStretch(0, 0)
        self.grid_layout_main.setRowStretch(1, 1)
        self.grid_layout_main.setRowStretch(2, 0)
        self.grid_layout_main.setColumnStretch(0, 0)
        self.grid_layout_main.setColumnStretch(1, 1)
        self.grid_layout_main.setColumnStretch(2, 0)

        self.setLayout(self.grid_layout_main)

        # главная рамка
        self.frame_main = QtWidgets.QFrame()
        self.frame_main.setObjectName("frame_main")
        self.frame_main.setContentsMargins(0, 0, 0, 0)
        self.frame_main.setFixedWidth(550)

        self.grid_layout_main.addWidget(self.frame_main, 1, 1)

        # внутренний макет
        self.vbox_layout_internal = QtWidgets.QVBoxLayout()
        self.vbox_layout_internal.setSpacing(0)
        self.vbox_layout_internal.setContentsMargins(30, 30, 30, 30)

        self.frame_main.setLayout(self.vbox_layout_internal)

        # макет логотипа и меток заголовка с версией
        self.hbox_layout_header = QtWidgets.QHBoxLayout()
        self.hbox_layout_header.setSpacing(0)
        self.hbox_layout_header.setContentsMargins(0, 0, 0, 0)

        self.vbox_layout_internal.addLayout(self.hbox_layout_header)
        self.vbox_layout_internal.addSpacing(10)

        # логотип
        self.logo = QtGui.QPixmap(self.path_logo)
        self.logo = self.logo.scaled(110, 110, transformMode = QtCore.Qt.SmoothTransformation)

        # метка с логотипом
        self.label_logo = QtWidgets.QLabel()
        self.label_logo.setObjectName("label_logo")
        self.label_logo.setAlignment(QtCore.Qt.AlignCenter)
        self.label_logo.setPixmap(self.logo)
        self.label_logo.setFixedSize(self.logo.width(), self.logo.height())

        self.hbox_layout_header.addWidget(self.label_logo)

        # макет меток заголовка и версии
        self.vbox_layout_text_header = QtWidgets.QVBoxLayout()
        self.vbox_layout_text_header.setSpacing(0)
        self.vbox_layout_text_header.setContentsMargins(0, 0, 0, 0)
        self.vbox_layout_text_header.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.hbox_layout_header.addLayout(self.vbox_layout_text_header)

        # метка заголовка
        self.label_header = QtWidgets.QLabel()
        self.label_header.setFont(QtGui.QFont("Segoe UI", 20, weight = QtGui.QFont.Bold))
        self.label_header.setObjectName("label_header")
        self.label_header.setText(self.name)
        self.label_header.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.vbox_layout_text_header.addWidget(self.label_header)
        self.vbox_layout_text_header.addSpacing(10)

        # метка версии
        self.label_version = QtWidgets.QLabel()
        self.label_version.setFont(QtGui.QFont("Segoe UI", 11))
        self.label_version.setObjectName("label_version")
        self.label_version.setText(self.version)
        self.label_version.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.vbox_layout_text_header.addWidget(self.label_version)

        # метка с текстом с информацией
        self.label_text_info = QtWidgets.QLabel()
        self.label_text_info.setFont(QtGui.QFont("Segoe UI", 11))
        self.label_text_info.setObjectName("label_text_info")
        self.label_text_info.setWordWrap(True)
        self.label_text_info.setText(self.text_info)
        self.label_text_info.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.vbox_layout_internal.addWidget(self.label_text_info)
        self.vbox_layout_internal.addSpacing(20)

        # макет инстументов
        self.hbox_layout_tools = QtWidgets.QHBoxLayout()
        self.hbox_layout_tools.setSpacing(0)
        self.hbox_layout_tools.setContentsMargins(0, 0, 0, 0)

        self.vbox_layout_internal.addLayout(self.hbox_layout_tools)

        self.hbox_layout_tools.addStretch(1)

        # кнопка ок
        self.push_button_ok = QtWidgets.QPushButton()
        self.push_button_ok.setObjectName("push_button_ok")
        self.push_button_ok.clicked.connect(self.clicked_push_button_ok)
        self.push_button_ok.setFont(QtGui.QFont("Segoe UI", 12))
        self.push_button_ok.setFixedSize(142, 42)
        self.push_button_ok.setText("Ок")
        self.push_button_ok.setFocusPolicy(QtCore.Qt.NoFocus)

        self.hbox_layout_tools.addWidget(self.push_button_ok)

        self.set_style_sheet()

        self.show()
  
        self.move(QtCore.QPoint(self.parent.geometry().getCoords()[0], self.parent.geometry().getCoords()[1]) + self.parent.rect().center() - self.rect().center())

    def clicked_push_button_ok(self):
        self.close()
        self.push_button_clicked_ok.emit()

    def set_style_sheet(self):
        # главная рамка
        self.frame_main.setStyleSheet("""
        #frame_main {
            border-radius: 14px;
            border: none;
            background: %(background)s;
        } """ % self.data_theme["frame_main"])

        # метка заголовка
        self.label_header.setStyleSheet("""
        #label_header {
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["label_header"])

        # метка версии
        self.label_version.setStyleSheet("""
        #label_version {
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["label_version"])

        # метка с текстом с информацией
        self.label_text_info.setStyleSheet("""
        #label_text_info {
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["label_text_info"])

        # кнопка ок
        self.push_button_ok.setStyleSheet("""
        #push_button_ok {
            outline: 0;
            border-radius: 7px;
            border: none;
            background: %(background)s; 
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["push_button_ok"])

        # тень
        self.frame_main.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.frame_main.shadow.setBlurRadius(17)
        self.frame_main.shadow.setOffset(0, 0)
        self.frame_main.shadow.setColor(QtGui.QColor(0, 0, 0, 100))
        self.frame_main.setGraphicsEffect(self.frame_main.shadow)
