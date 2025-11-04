from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QCoreApplication
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)

def remove_task(app, item, list_widget):
    try:
        reply = QMessageBox.question(
            app,
            get_text("Remover Tarefa"),
            get_text("Deseja remover a tarefa '{item}'?").replace("{item}", item.text()),
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            list_widget.takeItem(list_widget.row(item))
            if list_widget.count() == 0:
                if list_widget in (app.quadrant1_list,):
                    app.add_placeholder(list_widget, get_text("1º Quadrante"))

                elif list_widget in (app.quadrant2_list,):
                    app.add_placeholder(list_widget, get_text("2º Quadrante"))

                elif list_widget in (app.quadrant3_list,):
                    app.add_placeholder(list_widget, get_text("3º Quadrante"))

                elif list_widget in (app.quadrant4_list,):
                    app.add_placeholder(list_widget, get_text("4º Quadrante"))

                else:
                    app.add_placeholder(list_widget, get_text("Nenhuma Tarefa Concluída"))

            app.save_tasks()

    except Exception as e:
        logger.error(f"Erro ao remover tarefa: {e}", exc_info=True)
