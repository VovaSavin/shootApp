from PyQt6.QtCore import QModelIndex


class PopulatedTb:
    """
    Підставляє певні дані в поля таблиці
    """

    def __init__(self, index: QModelIndex, idx_main: int, idx_dep: int, data, value, text, ):
        self.index = index
        self.idx_main = idx_main
        self.idx_dep = idx_dep
        self.data = data
        self.value = value
        self.text = text

    def populated(self):
        if self.idx_main == self.idx_main:
            if self.value:
                self.data[self.index.row()][self.idx_dep] = self.text
            else:
                self.data[self.index.row()][self.idx_dep] = ""
