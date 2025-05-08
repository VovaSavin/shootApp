import sys, random, string

from PyQt6.QtCore import Qt, QSize, QAbstractTableModel, QModelIndex, QDate
from PyQt6.QtWidgets import (
    QWidget, QApplication, QLabel,
    QPushButton, QLineEdit, QVBoxLayout,
    QSpinBox, QMainWindow, QTableView,
    QInputDialog, QStyledItemDelegate, QDateEdit, QHBoxLayout, QTimeEdit, QComboBox,
)

from delegates.delegates import (
    SpinWidgetForDelegate,
    DateWidgetForDelegate,
    TimeWidgetDelegate,
    ComboWidgetDelegate,
)
from database.database import DBWorker, connector
from services.services import PopulatedTb

DATA_APP = {
    "head_labels": [["Дата"], ["Ціль"], ["Час початку"], ["Отримано від"], ["Тип цілі"], ["Коорд X"], ["Коорд Y"],
                    ["Позиція"], ["Час завершення"], ["Тип снаряду"], ["К-ть пострілів"], ["Враження цілі"],
                    ["Фото/відео"], ["Залишок"], ["Примітка"]
                    ],
    "connection_data": {
        'NAME': 'hows',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


class MyDelegate(QStyledItemDelegate):
    """
    Встановити кастомний делегат для полів
    0 - дата;
    2, 8 - час;
    10, 13 - числа;
    7 - список, що випадає;
    """

    def __init__(self, parent=None):
        super().__init__(parent)  # Тип даних для стовпця
        self.conn = DBWorker(
            DATA_APP["connection_data"]
        )
        self.positions = self.conn.get_data(
            "hw_position",
            ('id', 'name', 'remainder',)
        )
        self.spin = SpinWidgetForDelegate()
        self.date_field = DateWidgetForDelegate()
        self.time_field = TimeWidgetDelegate()
        self.combo = ComboWidgetDelegate(self.positions)

    def createEditor(self, parent, option, index):
        if index.column() in (10, 13):
            editor = QSpinBox(parent)
            self.spin.create_editor(editor)
        elif index.column() == 0:
            editor = QDateEdit(parent)
            self.date_field.create_editor(editor)
        elif index.column() in (2, 8):
            editor = QTimeEdit(parent)
            self.time_field.create_editor(editor)
        elif index.column() == 7:
            editor = QComboBox(parent)
            self.combo.create_editor(editor)
            self.combo.set_styles(editor)
        else:
            editor = QLineEdit(parent)
        return editor

    def setEditorData(self, editor: QDateEdit | QSpinBox | QLineEdit | QTimeEdit, index: QModelIndex):
        value = index.model().data(index, Qt.ItemDataRole.DisplayRole)
        if value:
            if isinstance(editor, QDateEdit):
                self.date_field.set_editor_data(editor, value)
            elif isinstance(editor, QSpinBox):
                self.spin.set_editor_data(editor, value)
            elif isinstance(editor, QTimeEdit):
                self.time_field.set_editor_data(editor, value)
            elif isinstance(editor, QComboBox):
                self.combo.set_editor_data(editor, value)
            elif isinstance(editor, QLineEdit):
                editor.setText(str(value))

    def setModelData(self, editor: QDateEdit | QSpinBox | QLineEdit | QTimeEdit, model, index: QModelIndex):
        if isinstance(editor, QSpinBox):
            value = self.spin.set_model_data(editor)
        elif isinstance(editor, QDateEdit):
            value = self.date_field.set_model_data(editor)
        elif isinstance(editor, QTimeEdit):
            value = self.time_field.set_model_data(editor)
        elif isinstance(editor, QComboBox):
            value = self.combo.set_model_data(editor)
        else:
            value = editor.text()
        model.setData(index, value, Qt.ItemDataRole.EditRole)


class MyTableModel(QAbstractTableModel):
    def __init__(self, data, tb: QTableView, cols: list):
        super().__init__()
        self._data = data
        self.tb = tb
        self.cols = cols

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
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
                return [self.cols[i][0] for i in range(len(self.cols))][section]
            if orientation == Qt.Orientation.Vertical:
                return f"Р{section + 1}"
        return None

    def setData(self, index, value, role, ):
        if role == Qt.ItemDataRole.EditRole:
            self._data[index.row()][index.column()] = value
            populated_tb = PopulatedTb(
                index, 0, 3, self._data, value, "Розвідка1БрОП"
            )
            populated_tb.populated()
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

    @staticmethod
    def update_tb(tb: QTableView, ):
        tb.update()
        tb.viewport().update()


class HeaderWidgetShoots(QWidget):
    def __init__(self, parent: QWidget = None, parent_layout: QVBoxLayout | QHBoxLayout = None, ):
        super().__init__(parent, )
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 5, 0, 5)
        self.parent_layout = parent_layout

    def init_widgets(self):
        self.set_widget(
            self,
            self.layout,
            width=int(round(self.size().width() * 70 / 100)),
            height=50,
            background_color="yellow",
            border_color="black",
            border_width=1,
        )
        lbl = QLabel()
        lbl.setText("Header")
        self.layout.addWidget(lbl)

    def set_widget(
            self,
            widget: QWidget,
            layout: QVBoxLayout | QHBoxLayout,
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
        self.parent_layout.addWidget(widget)


class WidgetRight(QWidget):
    """
    Віджет правої частини екрана
    """

    def __init__(self, parent=None, main_layout: QVBoxLayout | QHBoxLayout = None, ):
        super().__init__(parent)
        self.right_layout = QVBoxLayout(self)
        self.main_layout = main_layout
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def init_widgets(self):
        self.set_side_widget(
            self,
            self.right_layout,
            background_color="yellow",
            border_color="black",
            border_width=1,
        )
        lbl = QLabel()
        lbl.setText("Right")
        self.right_layout.addWidget(lbl)

    def set_side_widget(
            self, widget: QWidget, layout: QVBoxLayout | QHBoxLayout,
            background_color: str = "white",
            border_color: str = "black",
            border_width: int = 1,
    ):
        widget.setLayout(layout)
        widget.setStyleSheet(
            f"background-color: {background_color}; border: {border_width}px solid {border_color};"
        )
        self.main_layout.addWidget(widget)


class WidgetLeft(QWidget):
    """
    Віджет з лівої частини екрана
    Постріли
    """

    def __init__(self, parent=None, main_layout: QVBoxLayout | QHBoxLayout = None, cols=None):
        super().__init__(parent)
        self.cols = cols
        self.left_layout = QVBoxLayout(self)
        self.left_layout.setContentsMargins(0, 5, 0, 5)
        self.left_layout.setSpacing(0)
        self.main_layout = main_layout
        self.left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # Header
        self.header_widget_shoots = HeaderWidgetShoots(self, self.left_layout)
        self.add_cells_button = QPushButton()
        # Table
        self.tb_view = QTableView()
        self.tb_model = MyTableModel(
            [['' for _ in range(len(self.cols))]], self.tb_view, self.cols
        )
        # GetDataTb
        self.get_data_button = QPushButton()
        self.data_tables = []

    def init_widgets(self):
        self.set_side_widget(
            self,
            self.left_layout,
            background_color="white",
            border_color="black",
            border_width=1,
        )
        self.header_widget_shoots.init_widgets()
        self.set_table_view()
        self.set_button(
            self.add_cells_button,
            "Додати ряд",
            self.left_layout,
            self.add_cells,
        )
        self.set_button(
            self.get_data_button,
            "get",
            self.left_layout,
            self.get_data,
        )
        for x in range(3):
            self.add_cells()

    def set_side_widget(
            self, widget: QWidget, layout: QVBoxLayout | QHBoxLayout,
            background_color: str = "white",
            border_color: str = "black",
            border_width: int = 1,
    ):
        widget.setLayout(layout)
        widget.setStyleSheet(
            f"background-color: {background_color}; border: {border_width}px solid {border_color};"
        )
        self.main_layout.addWidget(widget)

    # SetButton
    @staticmethod
    def set_button(btn: QPushButton, text: str, layout: QVBoxLayout | QHBoxLayout, handler: callable, ):
        layout.addWidget(btn)
        layout.setAlignment(btn, Qt.AlignmentFlag.AlignRight)
        btn.setText(text)
        btn.setStyleSheet(
            "background-color: #e0e0e0; border: 1px solid black; font-weight: bold;"
        )
        btn.clicked.connect(handler)
        btn.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        btn.setFixedWidth(150)

    def set_table_view(self):
        """
        Встановлює таблицю
        :return:
        """
        self.tb_view.setModel(self.tb_model)
        delegate = MyDelegate()
        # Дата
        self.tb_view.setItemDelegateForColumn(0, delegate)
        # Час
        self.tb_view.setItemDelegateForColumn(2, delegate)
        self.tb_view.setItemDelegateForColumn(8, delegate)
        # Числа
        self.tb_view.setItemDelegateForColumn(10, delegate)
        self.tb_view.setItemDelegateForColumn(13, delegate)

        # Списки, що випадають
        self.tb_view.setItemDelegateForColumn(7, delegate)

        self.left_layout.addWidget(self.tb_view)

    # Handlers
    def add_cells(self):
        """
        Додавання нового рядка
        :return:
        """
        self.tb_model.addRow(['' for _ in range(15)])

    def get_data(self):
        model = self.tb_model
        for row in range(model.rowCount()):
            temp_inner_data = []
            for column in range(model.columnCount()):
                index = model.index(row, column)
                value = model.data(index, Qt.ItemDataRole.DisplayRole)
                if value != "":
                    temp_inner_data.append(
                        value
                    )
            if len(temp_inner_data):
                self.data_tables.append(
                    temp_inner_data
                )
        print(self.data_tables)


class WidgetWrapAll(QWidget):
    """
    Віджет обгортка
    """

    def __init__(self, parent=None, cols=None):
        super().__init__(parent=parent)
        self.cols = cols
        self.main_layout_wrap = QHBoxLayout(self)
        self.widget_left = WidgetLeft(self, self.main_layout_wrap, cols=self.cols)
        self.widget_right = WidgetRight(self, self.main_layout_wrap)

        self.init_widgets()

    def init_widgets(self):
        self.widget_left.init_widgets()
        self.widget_right.init_widgets()
        self.set_widget_wrap(
            self,
            "white",
            "black",
            1,
        )

    @staticmethod
    def set_widget_wrap(
            widget, background_color: str = "white",
            border_color: str = "black", border_width: int = 1,
    ):
        widget.setStyleSheet(
            f"background-color: {background_color}; border: {border_width}px solid {border_color};"
        )

    def resizeEvent(self, event):
        # Отримуємо новий розмір
        new_size: QSize = event.size()
        self.widget_right.setMinimumWidth(
            int(round(new_size.width() * 18 / 100), )
        )
        self.widget_left.setMinimumWidth(
            int(round(new_size.width() * 78 / 100), )
        )

        # Викликаємо перевизначений метод з базового класу
        super().resizeEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.in_app = QApplication(sys.argv)

        self.db_object = connector()
        self.conn = self.db_object.get_data(
            "hw_listheadtable",
            ("id", "names",)
        )
        self.setWindowTitle(
            self.conn[0]["names"]["title"]
        )
        self.widget_wrap_all = None

        self.initUI()

    def initUI(self):
        self.setMinimumSize(
            QSize(
                int(self.in_app.primaryScreen().size().width() / 1.1),
                int(self.in_app.primaryScreen().size().height() / 1.3)
            )
        )
        self.widget_wrap_all = WidgetWrapAll(self, cols=self.conn[0]["names"]["head_labels"])
        self.setCentralWidget(self.widget_wrap_all)
        self.show()


app3 = QApplication(sys.argv)
window = MainWindow()
sys.exit(app3.exec())
