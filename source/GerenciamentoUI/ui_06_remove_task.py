from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QCoreApplication, Qt
from source.utils.LogManager import LogManager
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
        if reply != QMessageBox.Yes:
            return

        list_widget.takeItem(list_widget.row(item))

        try:
            if hasattr(app, "cleanup_time_groups"):
                app.cleanup_time_groups(list_widget)

        except Exception as e:
            logger.error(f"Erro ao limpar grupos de horário após remoção: {e}", exc_info=True)

        def _has_selectable_items(lst) -> bool:
            for i in range(lst.count()):
                it = lst.item(i)
                if it and (it.flags() & Qt.ItemIsSelectable):
                    return True

            return False

        if not _has_selectable_items(list_widget):
            list_widget.clear()

            placeholders = {
                app.quadrant1_list: get_text("1º Quadrante"),
                app.quadrant2_list: get_text("2º Quadrante"),
                app.quadrant3_list: get_text("3º Quadrante"),
                app.quadrant4_list: get_text("4º Quadrante"),
                app.quadrant1_completed_list: get_text("Nenhuma Tarefa Concluída"),
                app.quadrant2_completed_list: get_text("Nenhuma Tarefa Concluída"),
                app.quadrant3_completed_list: get_text("Nenhuma Tarefa Concluída"),
                app.quadrant4_completed_list: get_text("Nenhuma Tarefa Concluída"),
            }

            app.add_placeholder(list_widget, placeholders.get(list_widget, get_text("Nenhuma Tarefa Concluída")))

        app.save_tasks()

    except Exception as e:
        logger.error(f"Erro ao remover tarefa: {e}", exc_info=True)
