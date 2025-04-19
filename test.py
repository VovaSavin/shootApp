import sys

from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import (
    QWidget, QApplication, QLabel,
    QVBoxLayout, QHBoxLayout,
    QSpinBox, QTableView, QStyledItemDelegate, QLineEdit,
)

lst = [
    "firs",
    "second",
    "third",
]

from PyQt6.QtWidgets import QStyledItemDelegate, QDateEdit
from PyQt6.QtCore import Qt, QModelIndex, QDate


class WidgetForDelegate:
    def __init__(self, ):
        pass

    def create_editor(self, editor: QSpinBox | QDateEdit | QLineEdit, ):
        pass

    def set_editor_data(self, editor: QSpinBox | QDateEdit | QLineEdit, value):
        pass

    def set_model_data(self, editor: QSpinBox | QDateEdit | QLineEdit, ):
        pass


class SpinWidgetForDelegate(WidgetForDelegate):
    def __init__(self, ):
        super().__init__()

    def create_editor(self, editor: QSpinBox, ):
        editor.setMinimum(0)
        editor.setMaximum(100)

    def set_editor_data(self, editor: QSpinBox, value):
        try:
            editor.setValue(int(value))
        except ValueError:
            editor.setValue(0)

    def set_model_data(self, editor: QSpinBox) -> int:
        editor.interpretText()
        return editor.value()


class DateWidgetForDelegate(WidgetForDelegate):
    def __init__(self, ):
        super().__init__()

    def create_editor(self, editor: QDateEdit, ):
        editor.setDisplayFormat("dd-MM-yy")  # Встановіть потрібний формат дати
        editor.setCalendarPopup(True)  # Увімкніть календар, що випадає
        editor.setDate(QDate.currentDate())

    def set_editor_data(self, editor: QDateEdit, value):
        editor.setDate(value)

    def set_model_data(self, editor: QDateEdit) -> QDate:
        return editor.date()


class MyDelegate(QStyledItemDelegate):
    """
    Встановити кастомний делегат для полів
    0 - SQpinBox
    1 - QDate
    2 - QLineEdit
    """

    def __init__(self, parent=None):
        super().__init__(parent)  # Тип даних для стовпця
        self.spin = SpinWidgetForDelegate()
        self.date_field = DateWidgetForDelegate()

    def createEditor(self, parent, option, index):
        if index.column() == 0:
            editor = QSpinBox(parent)
            self.spin.create_editor(editor)
        elif index.column() == 1:
            editor = QDateEdit(parent)
            self.date_field.create_editor(editor)
        else:
            editor = QLineEdit(parent)
        return editor

    def setEditorData(self, editor: QDateEdit | QSpinBox | QLineEdit, index: QModelIndex):

        value = index.model().data(index, Qt.ItemDataRole.DisplayRole)
        if value:
            if isinstance(editor, QDateEdit):
                self.date_field.set_editor_data(editor, value)
            elif isinstance(editor, QSpinBox):
                self.spin.set_editor_data(editor, value)
            elif isinstance(editor, QLineEdit):
                editor.setText(str(value))

    def setModelData(self, editor: QDateEdit | QSpinBox | QLineEdit, model, index: QModelIndex):
        if isinstance(editor, QSpinBox):
            value = self.spin.set_model_data(editor)
        elif isinstance(editor, QDateEdit):
            value = self.date_field.set_model_data(editor)
        else:
            value = editor.text()
        model.setData(index, value, Qt.ItemDataRole.EditRole)


class MyTableModel(QAbstractTableModel):
    def __init__(self, data, tb: QTableView):
        super().__init__()
        self._data = data
        self.tb = tb

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
                return lst[section]
            if orientation == Qt.Orientation.Vertical:
                return f"Р{section + 1}"
        return None

    def setData(self, index, value, role, ):

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

    @staticmethod
    def update_tb(tb: QTableView, ):
        tb.update()
        tb.viewport().update()


class WidgetRight(QWidget):
    """
    Віджет правої частини екрана
    """

    def __init__(self, ):
        super().__init__()
        self.setMinimumSize(600, 300)
        self.right_layout = QVBoxLayout(self)
        self.main_layout = QVBoxLayout()
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.tb_view = QTableView()
        self.tb_model = MyTableModel(
            [['' for _ in range(len(lst))]] * 3, self.tb_view
        )
        # self.tb_model = QStandardItemModel(5, len(lst))
        self.init_widgets()

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
        self.set_table_view()
        self.right_layout.addWidget(lbl)
        self.show()

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

    def set_table_view(self):
        """
        Встановлює таблицю
        :return:
        """
        self.tb_view.setModel(self.tb_model)

        # delegate_count_shoot_spinbox = SpinBoxDelegate("count")
        # self.tb_view.setItemDelegateForColumn(1, delegate_count_shoot_spinbox)
        # self.tb_view.setItemDelegateForColumn(0, delegate_count_shoot_spinbox)

        delegate = MyDelegate(self.tb_view)
        self.tb_view.setItemDelegateForColumn(0, delegate)
        self.tb_view.setItemDelegateForColumn(1, delegate)
        self.tb_view.setItemDelegateForColumn(2, delegate)

        self.right_layout.addWidget(self.tb_view)


app_test = QApplication(sys.argv)
window = WidgetRight()
sys.exit(app_test.exec())
