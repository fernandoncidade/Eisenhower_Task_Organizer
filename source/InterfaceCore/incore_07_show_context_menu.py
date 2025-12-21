from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import QCoreApplication, Qt
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)

def show_context_menu(app, point, list_widget):
    try:
        item = list_widget.itemAt(point)
        if not item:
            return

        if not bool(item.flags() & Qt.ItemIsSelectable):
            return

        menu = QMenu(list_widget)

        editar_data = QAction(get_text("Redefinir data...") or "Redefinir data...", app)
        editar_data.triggered.connect(lambda: app.edit_task_datetime(item, list_widget))
        menu.addAction(editar_data)

        mover_menu = menu.addMenu(get_text("Mover para") or "Mover para")

        q1 = QAction(get_text("Importante e Urgente"), app)
        q1.triggered.connect(lambda: app.move_task_to_quadrant(item, list_widget, app.quadrant1_list))
        mover_menu.addAction(q1)

        q2 = QAction(get_text("Importante, mas Não Urgente"), app)
        q2.triggered.connect(lambda: app.move_task_to_quadrant(item, list_widget, app.quadrant2_list))
        mover_menu.addAction(q2)

        q3 = QAction(get_text("Não Importante, mas Urgente"), app)
        q3.triggered.connect(lambda: app.move_task_to_quadrant(item, list_widget, app.quadrant3_list))
        mover_menu.addAction(q3)

        q4 = QAction(get_text("Não Importante e Não Urgente"), app)
        q4.triggered.connect(lambda: app.move_task_to_quadrant(item, list_widget, app.quadrant4_list))
        mover_menu.addAction(q4)

        menu.addSeparator()

        remover_acao = QAction(get_text("Remover Tarefa"), app)
        remover_acao.triggered.connect(lambda: app.remove_task(item, list_widget))
        menu.addAction(remover_acao)

        menu.exec(list_widget.mapToGlobal(point))

    except Exception as e:
        logger.error(f"Erro ao exibir menu de contexto: {e}", exc_info=True)
