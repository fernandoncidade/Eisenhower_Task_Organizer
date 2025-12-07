from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def add_placeholder(app, list_widget, text):
    try:
        placeholder_item = QListWidgetItem(text)
        placeholder_item.setFlags(placeholder_item.flags() & ~Qt.ItemIsSelectable)
        placeholder_item.setForeground(Qt.gray)
        placeholder_item.setData(Qt.UserRole, None)
        list_widget.addItem(placeholder_item)

    except Exception as e:
        logger.error(f"Erro ao adicionar placeholder: {e}", exc_info=True)
