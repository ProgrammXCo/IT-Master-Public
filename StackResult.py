from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtChart import QChart, QChartView, QPieSeries
import re

class LabelLegend(QtWidgets.QWidget):
    def __init__(self, text: str, data_theme: dict):
        super().__init__()
            
        self.text = text
        self.data_theme = data_theme

        # главный макет
        self.hbox_layout_main = QtWidgets.QHBoxLayout()
        self.hbox_layout_main.setSpacing(0)
        self.hbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.hbox_layout_main)

        # метка индикатор
        self.label_indicator = QtWidgets.QLabel()
        self.label_indicator.setObjectName("label_indicator")
        self.label_indicator.setFixedSize(24, 24)

        self.hbox_layout_main.addWidget(self.label_indicator)
        self.hbox_layout_main.addSpacing(10)

        # метка с текстом
        self.label_text = QtWidgets.QLabel()
        self.label_text.setObjectName("label_text")
        self.label_text.setFont(QtGui.QFont("Segoe UI", 16))
        self.label_text.setText(self.text)

        self.hbox_layout_main.addWidget(self.label_text)

        self.set_style_sheet()

    def set_style_sheet(self):
        # метка индикатор
        self.label_indicator.setStyleSheet("""
        #label_indicator {
            background: %(background)s;
            border-radius: 12px;
        } """ % self.data_theme["indicator"])

        # метка с текстом
        self.label_text.setStyleSheet("""
        #label_text {
            color: %(color)s;
        } """ % self.data_theme)

class BarNavigation(QtWidgets.QWidget):
    def __init__(self, dict_result: dict , data_theme: dict):
        super().__init__()

        self.dict_result = dict_result
        self.data_theme = data_theme

        # главный макет
        self.hbox_layout_main = QtWidgets.QHBoxLayout()
        self.hbox_layout_main.setSpacing(0)
        self.hbox_layout_main.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.hbox_layout_main)

        # панель инструментов и навигации
        self.frame_tools = QtWidgets.QFrame()
        self.frame_tools.setObjectName("frame_tools")

        self.hbox_layout_main.addWidget(self.frame_tools)

        # макет панели инстументов
        self.hbox_layout_tools = QtWidgets.QHBoxLayout()
        self.hbox_layout_tools.setSpacing(10)
        self.hbox_layout_tools.setContentsMargins(20, 10, 20, 10)

        self.frame_tools.setLayout(self.hbox_layout_tools)

        self.hbox_layout_tools.addStretch(1)

        for i in range(max(self.dict_result.keys()) + 1):
            label_number = QtWidgets.QLabel()
            label_number.setObjectName("label_number")
            label_number.setText(f"{i + 1}")
            label_number.setAlignment(QtCore.Qt.AlignCenter)
            label_number.setFont(QtGui.QFont("Segoe UI", 12))
            label_number.setFixedSize(50, 50)

            self.hbox_layout_tools.addWidget(label_number)

            if self.dict_result[i] == "right":
                temp_data_theme = self.data_theme["label_number_right"]
            elif self.dict_result[i] == "wrong":
                temp_data_theme = self.data_theme["label_number_wrong"]
            elif self.dict_result[i] == "skip":
                temp_data_theme = self.data_theme["label_number_skip"]

            label_number.setStyleSheet("""
            #label_number {
                border-radius: 25px;
                background: %(background)s;
                color: %(color)s;
            } """ % temp_data_theme)

        self.hbox_layout_tools.addStretch(1)

        self.set_style_sheet()

    def set_style_sheet(self):
        # панель инструментов и навигации
        self.frame_tools.setStyleSheet("""
        #frame_tools {
            border-radius: 20px;
            background: %(background)s;
        } """ % self.data_theme)

class StackResult(QtWidgets.QWidget):
    def __init__(self, data_result, data_theme: dict, func: callable):
        super().__init__()

        self.data_result = data_result
        self.data_theme = data_theme
        self.func = func

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

        self.vbox_layout_internal.addStretch(1)

        # макет диаграммы и легенды
        self.hbox_layout_chart = QtWidgets.QHBoxLayout()
        self.hbox_layout_chart.setSpacing(0)
        self.hbox_layout_chart.setContentsMargins(0, 0, 0, 0)

        self.hbox_layout_chart.addStretch(2)

        self.vbox_layout_internal.addLayout(self.hbox_layout_chart)
        self.vbox_layout_internal.addStretch(1)

        # диаграмма
        self.series = QPieSeries()
        self.series.setHoleSize(0.4)

        self.slice_right = self.series.append("Правильные", round(self.data_result.points_right / self.data_result.points_max * 100))
        self.slice_wrong = self.series.append("Неправильные", round(self.data_result.points_wrong / self.data_result.points_max * 100))
        self.slice_skip = self.series.append("Пропущенные", round(self.data_result.points_skip / self.data_result.points_max * 100))

        self.chart = QChart()
        self.chart.legend().hide()
        self.chart.layout().setContentsMargins(0, 0, 0, 0)
        self.chart.setBackgroundRoundness(0)
        self.chart.setContentsMargins(-82,-82,-82, -82)
        self.chart.addSeries(self.series)

        self.chartview = QChartView(self.chart)
        self.chartview.setFixedSize(QtCore.QSize(293, 293))
        self.chartview.setObjectName("chartview")

        self.hbox_layout_chart.addWidget(self.chartview)
        self.hbox_layout_chart.addStretch(1)

        # рамка легенды
        self.frame_legend = QtWidgets.QFrame()
        self.frame_legend.setObjectName("frame_legend")
        
        self.hbox_layout_chart.addWidget(self.frame_legend)
        self.hbox_layout_chart.addStretch(2)

        # макет легенды
        self.vbox_layout_legend = QtWidgets.QVBoxLayout()
        self.vbox_layout_legend.setSpacing(0)
        self.vbox_layout_legend.setContentsMargins(30, 30, 30, 30)

        self.frame_legend.setLayout(self.vbox_layout_legend)

        # метка количества баллов
        self.label_result = QtWidgets.QLabel()
        self.label_result.setObjectName("label_result")
        self.label_result.setText(f"{round(self.data_result.points_right / self.data_result.points_max * 100)} / 100")
        self.label_result.setFont(QtGui.QFont("Segoe UI", 20))
        self.label_result.setAlignment(QtCore.Qt.AlignCenter)

        self.vbox_layout_legend.addWidget(self.label_result)
        self.vbox_layout_legend.addSpacing(10)

        # метка заголовка
        self.label_header = QtWidgets.QLabel()
        self.label_header.setObjectName("label_header")
        self.label_header.setText(f"Результат теста в баллах")
        self.label_header.setFont(QtGui.QFont("Segoe UI", 16))
        self.label_header.setAlignment(QtCore.Qt.AlignCenter)

        self.vbox_layout_legend.addWidget(self.label_header)
        self.vbox_layout_legend.addSpacing(10)

        # метка легенды правильно
        self.label_legent_right = LabelLegend(
            text = f"Правильные: {self.data_result.points_right} ({round(self.data_result.points_right / self.data_result.points_max * 100)}%)",
            data_theme = self.data_theme["frame_main"]["frame_legend"]["label_legend_right"]
        )

        self.vbox_layout_legend.addWidget(self.label_legent_right)
        self.vbox_layout_legend.addSpacing(10)

        # метка легенды неправильно
        self.label_legent_right = LabelLegend(
            text = f"Неправильные: {self.data_result.points_wrong} ({round(self.data_result.points_wrong / self.data_result.points_max * 100)}%)",
            data_theme = self.data_theme["frame_main"]["frame_legend"]["label_legend_wrong"]
        )

        self.vbox_layout_legend.addWidget(self.label_legent_right)
        self.vbox_layout_legend.addSpacing(10)

        # метка легенды пропущенно
        self.label_legent_right = LabelLegend(
            text = f"Пропущенные: {self.data_result.points_skip} ({round(self.data_result.points_skip / self.data_result.points_max * 100)}%)",
            data_theme = self.data_theme["frame_main"]["frame_legend"]["label_legend_skip"]
        )

        self.vbox_layout_legend.addWidget(self.label_legent_right)

        # макет панель навигации
        self.hbox_layout_bar_navigation = QtWidgets.QHBoxLayout()
        self.hbox_layout_bar_navigation.setSpacing(0)
        self.hbox_layout_bar_navigation.setContentsMargins(20, 20, 20, 20)

        self.vbox_layout_internal.addLayout(self.hbox_layout_bar_navigation)

        # панель навигации
        self.bar_navigation = BarNavigation(
            dict_result = self.data_result.dict_result,
            data_theme = self.data_theme["frame_main"]["bar_navigation"] 
        )

        self.hbox_layout_bar_navigation.addWidget(self.bar_navigation)

        # панель инструментов
        self.frame_tools = QtWidgets.QFrame()
        self.frame_tools.setObjectName("frame_tools")
        
        self.vbox_layout_internal.addWidget(self.frame_tools)

        # макет инструментов
        self.hbox_layout_tools = QtWidgets.QHBoxLayout()
        self.hbox_layout_tools.setSpacing(0)
        self.hbox_layout_tools.setContentsMargins(20, 10, 20, 10)

        self.frame_tools.setLayout(self.hbox_layout_tools)

        self.hbox_layout_tools.addStretch(1)

        # кнопка вернуться на главную
        self.push_button_to_main = QtWidgets.QPushButton()
        self.push_button_to_main.setObjectName("push_button_to_main")
        self.push_button_to_main.clicked.connect(self.func)
        self.push_button_to_main.setFont(QtGui.QFont("Segoe UI", 14))
        self.push_button_to_main.setText("На главную")
        self.push_button_to_main.setFixedHeight(42)

        self.hbox_layout_tools.addWidget(self.push_button_to_main)
        self.hbox_layout_tools.addStretch(1)

        self.set_style_sheet()

    def init_variables(self):
        pattern = re.compile(r"^\s*rgb\s*\(\s*|\s*,\s*|\s*\)\s*$")

        self.indicator_background_right = QtGui.QColor(*[int(i) for i in pattern.split(self.data_theme["frame_main"]["frame_legend"]["label_legend_right"]["indicator"]["background"])[1:-1]])
        self.indicator_background_wrong = QtGui.QColor(*[int(i) for i in pattern.split(self.data_theme["frame_main"]["frame_legend"]["label_legend_wrong"]["indicator"]["background"])[1:-1]])
        self.indicator_background_skip = QtGui.QColor(*[int(i) for i in pattern.split(self.data_theme["frame_main"]["frame_legend"]["label_legend_skip"]["indicator"]["background"])[1:-1]])
        self.chartview_background = QtGui.QColor(*[int(i) for i in pattern.split(self.data_theme["frame_main"]["chartview"]["background"])[1:-1]])

    def set_style_sheet(self):
        # диаграмма
        self.chartview.chart().setBackgroundBrush(QtGui.QBrush(self.chartview_background))

        self.slice_right.setBrush(self.indicator_background_right)
        self.slice_wrong.setBrush(self.indicator_background_wrong)
        self.slice_skip.setBrush(self.indicator_background_skip)

        # главная рамка
        self.frame_main.setStyleSheet("""
        #frame_main {
            background: %(background)s;
        } """ % self.data_theme["frame_main"])

        # метка количества баллов
        self.label_result.setStyleSheet("""
        #label_result {
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["frame_legend"]["label_result"])

        # метка заголовка
        self.label_header.setStyleSheet("""
        #label_header {
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["frame_legend"]["label_header"])

        # рамка легенды
        self.frame_legend.setStyleSheet("""
        #frame_legend {
            border-radius: 14px;
            background: %(background)s;
        } """ % self.data_theme["frame_main"]["frame_legend"])

        # тень рамки легенды
        self.frame_legend.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.frame_legend.shadow.setBlurRadius(17)
        self.frame_legend.shadow.setOffset(0, 0)
        self.frame_legend.shadow.setColor(QtGui.QColor(0, 0, 0, 100))
        self.frame_legend.setGraphicsEffect(self.frame_legend.shadow)

        # панель инструментов
        self.frame_tools.setStyleSheet("""
        #frame_tools {
            border-top-left-radius: 40px;
            border-top-right-radius: 40px;
            background: %(background)s;
        } """ % self.data_theme["frame_main"]["frame_tools"])

        # кнопка вернуться на главную
        self.push_button_to_main.setStyleSheet("""
        #push_button_to_main {
            outline: 0;
            padding-left: 10;
            padding-right: 10;
            border-radius: 7px;
            background: %(background)s;
            color: %(color)s;
        } """ % self.data_theme["frame_main"]["frame_tools"]["push_button_to_main"])
