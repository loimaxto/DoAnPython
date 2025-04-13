from PyQt6.QtWidgets import QStyledItemDelegate, QRadioButton, QButtonGroup
from PyQt6.QtCore import Qt, QModelIndex

class RadioButtonDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.button_group = QButtonGroup(parent)
        self.button_group.setExclusive(True)

    def createEditor(self, parent, option, index):
        editor = QRadioButton(parent)
        self.button_group.addButton(editor)
        return editor

    def setEditorData(self, editor, index):
        editor.setChecked(index.data(Qt.ItemDataRole.CheckStateRole) == Qt.CheckState.Checked)

    def setModelData(self, editor, model, index):
        model.setData(index, Qt.CheckState.Checked if editor.isChecked() else Qt.CheckState.Unchecked, 
                     Qt.ItemDataRole.CheckStateRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)