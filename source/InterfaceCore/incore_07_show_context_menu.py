from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import QCoreApplication, Qt

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)

def show_context_menu(app, point, list_widget):
    item = list_widget.itemAt(point)
    if not item:
        return

    if not bool(item.flags() & Qt.ItemIsSelectable):
        return

    menu = QMenu(list_widget)
    remover_acao = QAction(get_text("Remover Tarefa"), app)
    remover_acao.triggered.connect(lambda: app.remove_task(item, list_widget))
    menu.addAction(remover_acao)
    menu.exec(list_widget.mapToGlobal(point))
