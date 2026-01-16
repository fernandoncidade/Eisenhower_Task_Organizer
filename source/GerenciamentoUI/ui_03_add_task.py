from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import QListWidgetItem, QMessageBox
from PySide6.QtGui import QFont
from source.utils.LogManager import LogManager
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

        quadrant_map = {
            0: app.quadrant1_list,
            1: app.quadrant2_list,
            2: app.quadrant3_list,
            3: app.quadrant4_list,
        }
        target_list = quadrant_map.get(selected_quadrant)
        if target_list is None:
            logger.error(f"Quadrante inválido selecionado: {selected_quadrant}")
            return

        clear_placeholder_if_needed(target_list)

        display_text = task_text
        if date_str:
            if time_str:
                display_text = f"{task_text} — {date_human} {time_str}"

            else:
                display_text = f"{task_text} — {date_human}"

        task_item = QListWidgetItem(display_text)
        task_item.setFlags(task_item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        task_item.setCheckState(Qt.Unchecked)

        try:
            priority = int(selected_quadrant) + 1

        except Exception:
            priority = None

        task_item.setData(Qt.UserRole, {"text": task_text, "date": date_str, "time": time_str, "priority": priority})
        task_item.setToolTip(tooltip_text)

        try:
            dragged_path = getattr(app, "_dragged_file_path", None)
            if dragged_path:
                reply = QMessageBox.question(
                    app,
                    get_text("Vincular Arquivo"),
                    get_text("Deseja vincular o arquivo a esta tarefa?"),
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    try:
                        data = task_item.data(Qt.UserRole) or {}
                        data["file_path"] = dragged_path
                        task_item.setData(Qt.UserRole, data)
                        tt = task_item.toolTip() or ""
                        if tt:
                            tt = tt + "\n"

                        tt = tt + (get_text("Arquivo") or "Arquivo") + f": {dragged_path}"
                        task_item.setToolTip(tt)

                        try:
                            font = task_item.font() or QFont()
                            font.setBold(True)
                            task_item.setFont(font)
                            task_item.setForeground(Qt.blue)

                        except Exception:
                            pass

                    except Exception:
                        logger.error("Erro ao vincular arquivo à tarefa", exc_info=True)

                try:
                    delattr(app, "_dragged_file_path")

                except Exception:
                    try:
                        setattr(app, "_dragged_file_path", None)

                    except Exception:
                        pass

        except Exception:
            logger.error("Erro ao processar arquivo arrastado antes de adicionar tarefa", exc_info=True)

        app.insert_task_into_quadrant_list(target_list, task_item)
        app.task_input.clear()
        app.save_tasks()

    except Exception as e:
        logger.error(f"Erro ao adicionar tarefa: {e}", exc_info=True)
