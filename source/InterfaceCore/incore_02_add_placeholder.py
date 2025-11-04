from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem

def add_placeholder(app, list_widget, text):
    placeholder_item = QListWidgetItem(text)
    placeholder_item.setFlags(placeholder_item.flags() & ~Qt.ItemIsSelectable)
    placeholder_item.setForeground(Qt.gray)
    list_widget.addItem(placeholder_item)
