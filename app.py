import sys, random, string
from PyQt6.QtCore import Qt, QSize, QAbstractTableModel, QModelIndex
from PyQt6.QtWidgets import (
    QWidget, QApplication, QLabel,
    QPushButton, QLineEdit, QVBoxLayout,
    QHBoxLayout, QButtonGroup, QRadioButton,
    QSpinBox, QTextEdit, QComboBox,
    QStackedLayout, QMainWindow, QTableView,
    QInputDialog,
)

FONT_SIZE_LABEL = 14
DATA_APP = {
    "title": "Артилерія 1 БрОП",
    "sizes": (1000, 600),
    "head_labels": (
        # 0 - text,
        ("Дата",),
        ("Ціль",),
        ("Час початку",),
        ("Отримано від",),
        ("Тип цілі",),
        ("Коорд X",),
        ("Коорд Y",),
        ("Позиція",),
        ("Час завершення",),
        ("Тип снаряду",),
        ("К-ть пострілів",),
        ("Враження цілі",),
        ("Фото/відео",),
        ("Залишок",),
        ("Примітка",),
    ),
}


class MyTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        if len(self._data):
            return len(self._data[0])
        else:
            return 0

    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return [DATA_APP["head_labels"][i][0] for i in range(len(DATA_APP["head_labels"]))][section]
            if orientation == Qt.Orientation.Vertical:
                return f"Р{section + 1}"
        return None

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole])
            return True
        return False

    def flags(self, index):
        # Дозволяємо редагування клітинок
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable

    def addRow(self, row_data):
        self.beginInsertRows(QModelIndex(), self.rowCount(None), self.rowCount(None))
        self._data.append(row_data)
        self.endInsertRows()


class HeaderWidgetShoots(QWidget):
    def __init__(self, parent_widget: QWidget = None, parent_layout: QVBoxLayout | QHBoxLayout = None, ):
        super().__init__(parent_widget, )
        self.layout = QHBoxLayout(self)
        self.parent_layout = parent_layout
        self.init_widgets()

    def init_widgets(self):
        self.set_widget(
            self,
            self.layout,
            parent_layout=self.parent_layout,
            width=int(round(self.size().width() * 70 / 100)),
            height=50,
            background_color="white",
            border_color="black",
            border_width=1,
        )

    @staticmethod
    def set_widget(
            widget: QWidget,
            layout: QVBoxLayout | QHBoxLayout,
            parent_layout: QVBoxLayout | QHBoxLayout,
            width: int, height: int,
            background_color: str = "white",
            border_color: str = "black",
            border_width: int = 1,
    ):
        widget.setLayout(layout)
        widget.setMinimumWidth(width)
        widget.setFixedHeight(height)
        widget.setStyleSheet(
            f"background-color: {background_color}; border: {border_width}px solid {border_color};"
        )
        parent_layout.addWidget(widget)


class WidgetRight(QWidget):
    """
    Віджет правої частини екрана
    """

    def __init__(self, parent=None, main_layout: QVBoxLayout | QHBoxLayout = None, ):
        super().__init__(parent)
        self.right_layout = QVBoxLayout(self)
        self.main_layout = main_layout
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.init_widgets()

    def init_widgets(self):
        pass


class WidgetLeft(QWidget):
    """
    Віджет з лівої частини екрана
    Постріли
    """

    def __init__(self, parent=None, main_layout: QVBoxLayout | QHBoxLayout = None, ):
        super().__init__(parent)
        self.left_layout = QVBoxLayout(self)
        self.main_layout = main_layout
        self.left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.header_widget_shoots = HeaderWidgetShoots(self, self.left_layout)
        self.add_cells_button = QPushButton()
        self.test_data = [
            [''.join(random.choices(string.ascii_letters, k=random.randint(1, 7))) for _ in range(15)]
            for _ in range(15)
        ]
        # Table
        self.tb_model = MyTableModel(
            self.test_data + [['' for _ in range(15)]] + [['' for _ in range(15)]]
        )
        self.tb_view = QTableView()

    def init_widgets(self):
        self.set_side_widget(
            self,
            self.left_layout,
            width=int(round(self.size().width() * 30 / 100)),
            height=self.size().height() - 50,
            background_color="white",
            border_color="black",
            border_width=1,
        )
        self.set_table_view()
        self.set_button(
            self.add_cells_button,
            "Додати ряд",
            self.left_layout,
            self.add_cells,
        )

        self.header_widget_shoots.init_widgets()

    def set_side_widget(
            self, widget: QWidget, layout: QVBoxLayout | QHBoxLayout, width: int, height: int,
            background_color: str = "white",
            border_color: str = "black",
            border_width: int = 1,
    ):
        widget.setLayout(layout)
        widget.setMinimumWidth(width)
        widget.setMinimumHeight(height)
        widget.setStyleSheet(
            f"background-color: {background_color}; border: {border_width}px solid {border_color};"
        )
        self.main_layout.addWidget(widget)

    # SetButton
    @staticmethod
    def set_button(btn: QPushButton, text: str, layout: QVBoxLayout | QHBoxLayout, handler: callable, ):
        layout.addWidget(btn)
        btn.setText(text)
        btn.setStyleSheet(
            "background-color: white; border: 0px solid black;"
        )
        btn.clicked.connect(handler)

    def set_table_view(self):
        """
        Встановлює таблицю
        :return:
        """
        self.tb_view.setModel(self.tb_model)
        self.left_layout.addWidget(self.tb_view)

    # Handlers
    def add_row(self):
        # Введення нового рядка через діалогове вікно
        new_row = []
        for col in range(3):  # У нашій таблиці 3 колонки
            value, ok = QInputDialog.getText(self, "Додавання запису", f"Введіть дані для стовпця {col + 1}:")
            if ok:
                new_row.append(value)
        if new_row:
            self.tb_model.addRow(new_row)

    def add_cells(self):
        self.tb_model.addRow(['' for _ in range(15)])


class WidgetWrapAll(QWidget):
    """
    Віджет обгргортка
    """

    def __init__(self):
        super().__init__()
        self.set_widget_wrap(
            self, background_color="white", border_color="black", border_width=1,
        )
        self.main_layout = QHBoxLayout(self)
        self.widget_left = WidgetLeft(self, self.main_layout)

        # RightWidget
        self.widget_right = QWidget(self)
        self.right_layout = QVBoxLayout()

        # ButtonAddRow
        self.add_cells_button = QPushButton()

    def init_widgets(self):
        self.set_side_widget(
            self.widget_right,
            self.right_layout,
            width=int(round(self.size().width() * 30 / 100)),
            height=self.size().height() - 50
        )
        self.widget_left.init_widgets()

    # CreateHeaderWidget
    @staticmethod
    def set_widget(
            widget: QWidget,
            layout: QVBoxLayout | QHBoxLayout,
            parent_layout: QVBoxLayout | QHBoxLayout,
            width: int, height: int,
            background_color: str = "white",
            border_color: str = "black",
            border_width: int = 1,
    ):
        widget.setLayout(layout)
        widget.setMinimumWidth(width)
        widget.setFixedHeight(height)
        widget.setStyleSheet(
            f"background-color: {background_color}; border: {border_width}px solid {border_color};"
        )
        parent_layout.addWidget(widget)

    # CreateSideWidgets
    def set_side_widget(
            self, widget: QWidget, layout: QVBoxLayout | QHBoxLayout, width: int, height: int,
            background_color: str = "white",
            border_color: str = "black",
            border_width: int = 1,
    ):
        widget.setLayout(layout)
        widget.setMinimumWidth(width)
        widget.setMinimumHeight(height)
        widget.setStyleSheet(
            f"background-color: {background_color}; border: {border_width}px solid {border_color};"
        )
        self.main_layout.addWidget(widget)

    @staticmethod
    def set_widget_wrap(
            widget: QWidget, background_color: str = "white",
            border_color: str = "black", border_width: int = 1,
    ):
        widget.setStyleSheet(
            f"background-color: {background_color}; border: {border_width}px solid {border_color};"
        )

    def resizeEvent(self, event):
        # Отримуємо новий розмір
        new_size: QSize = event.size()
        self.widget_right.setMinimumWidth(
            int(round(new_size.width() * 20 / 100), )
        )
        self.widget_left.setMinimumWidth(
            int(round(new_size.width() * 79 / 100), )
        )

        # Викликаємо перевизначений метод з базового класу
        super().resizeEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            DATA_APP["title"]
        )
        # MainWrapper
        self.widget_wrap_all = WidgetWrapAll()

        #
        self.initUI()

    def initUI(self):
        self.setMinimumSize(
            QSize(*DATA_APP["sizes"], )
        )

        self.setCentralWidget(self.widget_wrap_all)
        self.widget_wrap_all.init_widgets()
        self.show()


app3 = QApplication(sys.argv)
window = MainWindow()
sys.exit(app3.exec())
