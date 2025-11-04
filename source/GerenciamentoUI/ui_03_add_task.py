from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import QListWidgetItem, QMessageBox
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)

def add_task(app):
    try:
        task_text = app.task_input.text().strip()
        if not task_text:
            QMessageBox.warning(app, get_text("Erro"), get_text("A tarefa não pode estar vazia."))
            return

        selected_quadrant = app.quadrant_selector.currentIndex()

        if app.date_checkbox.isChecked():
            date_str = app.date_input.date().toString(Qt.ISODate)
            date_human = app.date_input.date().toString(app.date_input.displayFormat())
            time_str = None
            if hasattr(app, "time_checkbox") and hasattr(app, "time_input") and app.time_checkbox.isChecked():
                time_str = app.time_input.time().toString("HH:mm")

            tooltip_lines = [f"{get_text('Data') or 'Data'}: {date_human}"]
            if time_str:
                tooltip_lines.append(f"{get_text('Horário') or 'Horário'}: {time_str}")

            tooltip_text = "\n".join(tooltip_lines)

        else:
            date_str = None
            time_str = None
            tooltip_text = ""

        def clear_placeholder_if_needed(lst):
            if lst.count() == 1 and not (lst.item(0).flags() & Qt.ItemIsSelectable):
                lst.clear()

        clear_placeholder_if_needed(app.quadrant1_list)
        clear_placeholder_if_needed(app.quadrant2_list)
        clear_placeholder_if_needed(app.quadrant3_list)
        clear_placeholder_if_needed(app.quadrant4_list)

        display_text = task_text
        if date_str:
            if time_str:
                display_text = f"{task_text} — {date_human} {time_str}"

            else:
                display_text = f"{task_text} — {date_human}"

        task_item = QListWidgetItem(display_text)
        task_item.setFlags(task_item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        task_item.setCheckState(Qt.Unchecked)
        task_item.setData(Qt.UserRole, {"text": task_text, "date": date_str, "time": time_str})
        task_item.setToolTip(tooltip_text)

        if selected_quadrant == 0:
            app.insert_task_into_quadrant_list(app.quadrant1_list, task_item)

        elif selected_quadrant == 1:
            app.insert_task_into_quadrant_list(app.quadrant2_list, task_item)

        elif selected_quadrant == 2:
            app.insert_task_into_quadrant_list(app.quadrant3_list, task_item)

        elif selected_quadrant == 3:
            app.insert_task_into_quadrant_list(app.quadrant4_list, task_item)

        app.task_input.clear()
        app.save_tasks()

    except Exception as e:
        logger.error(f"Erro ao adicionar tarefa: {e}", exc_info=True)
