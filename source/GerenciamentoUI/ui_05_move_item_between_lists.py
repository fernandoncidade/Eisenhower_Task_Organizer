from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtCore import QCoreApplication, QDate
from PySide6.QtGui import QFont
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)

def move_item_between_lists(app, item, source, target, new_check_state):
    try:
        data = item.data(Qt.UserRole) or {}
        base_text = data.get("text", item.text())
        date_value = data.get("date")
        time_value = data.get("time")

        display_text = base_text
        if date_value:
            qd = QDate.fromString(date_value, Qt.ISODate)
            if qd.isValid():
                date_human = qd.toString(app.date_input.displayFormat())
                if time_value:
                    display_text = f"{base_text} — {date_human} {time_value}"

                else:
                    display_text = f"{base_text} — {date_human}"

        row = source.row(item)
        source.takeItem(row)
        tooltip = item.toolTip()

        if hasattr(app, "cleanup_time_groups"):
            app.cleanup_time_groups(source)

        def _has_selectable_items(lst) -> bool:
            for i in range(lst.count()):
                it = lst.item(i)
                if it and (it.flags() & Qt.ItemIsSelectable):
                    return True

            return False

        if not _has_selectable_items(source):
            source.clear()

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
            app.add_placeholder(source, placeholders.get(source, get_text("Nenhuma Tarefa Concluída")))

        if target.count() == 1 and not (target.item(0).flags() & Qt.ItemIsSelectable):
            target.clear()

        new_item = QListWidgetItem(display_text)
        new_item.setFlags(new_item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        if data is not None:
            new_data = dict(data)
            new_data["time"] = time_value

            try:
                if target in (app.quadrant1_list, app.quadrant1_completed_list):
                    new_data["priority"] = 1

                elif target in (app.quadrant2_list, app.quadrant2_completed_list):
                    new_data["priority"] = 2

                elif target in (app.quadrant3_list, app.quadrant3_completed_list):
                    new_data["priority"] = 3

                elif target in (app.quadrant4_list, app.quadrant4_completed_list):
                    new_data["priority"] = 4

                else:
                    new_data["priority"] = new_data.get("priority")

            except Exception:
                new_data["priority"] = new_data.get("priority")

            new_item.setData(Qt.UserRole, new_data)

            try:
                if new_data.get("file_path"):
                    font = new_item.font() or QFont()
                    font.setBold(True)
                    new_item.setFont(font)
                    new_item.setForeground(Qt.blue)

            except Exception:
                pass

        if tooltip:
            new_item.setToolTip(tooltip)

        new_item.setCheckState(new_check_state)

        if hasattr(app, "insert_task_into_quadrant_list"):
            app.insert_task_into_quadrant_list(target, new_item)

        else:
            target.addItem(new_item)

    except Exception as e:
        logger.error(f"Erro ao mover item entre listas: {e}", exc_info=True)
