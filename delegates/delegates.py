from PyQt6.QtCore import QDate, QTime
from PyQt6.QtWidgets import (
    QSpinBox,
    QLineEdit,
    QDateEdit,
    QTimeEdit,
    QComboBox,
)


class WidgetForDelegate:
    def __init__(self, ):
        pass

    def create_editor(self, editor: QSpinBox | QDateEdit | QLineEdit | QComboBox, ):
        pass

    def set_editor_data(self, editor: QSpinBox | QDateEdit | QLineEdit | QComboBox, value):
        pass

    def set_model_data(self, editor: QSpinBox | QDateEdit | QLineEdit | QComboBox, ):
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


class TimeWidgetDelegate(WidgetForDelegate):
    """
    Time
    """

    def __init__(self):
        super().__init__()

    def create_editor(self, editor: QTimeEdit):
        editor.setDisplayFormat("hh:mm")
        editor.setTime(QTime.currentTime())

    def set_editor_data(self, editor: QTimeEdit, value):
        editor.setTime(value)

    def set_model_data(self, editor: QTimeEdit, ) -> QTime:
        return editor.time()


class ComboWidgetDelegate(WidgetForDelegate):
    """
    ComboBox
    """

    def __init__(self, items: list | tuple):
        super().__init__()
        self.items = items

    def create_editor(self, editor: QComboBox, ):
        editor.addItems(
            [item["name"] for item in self.items]
        )

    def set_editor_data(self, editor: QComboBox, value):
        editor.setCurrentText(value)

    def set_model_data(self, editor: QComboBox, ) -> str:
        return editor.currentText()
