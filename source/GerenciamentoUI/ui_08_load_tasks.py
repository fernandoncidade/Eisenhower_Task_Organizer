import json
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt, QDate, QCoreApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)

def load_tasks(app):
    try:
        with open(app.tasks_path, "r", encoding="utf-8") as file:
            tasks = json.load(file)
            date_format = app.date_input.displayFormat() if hasattr(app, "date_input") else "dd/MM/yyyy"

            def create_item(text, date_value, time_value, completed):
                display_text = text
                tooltip_lines = []
                if date_value:
                    qdate = QDate.fromString(date_value, Qt.ISODate)
                    if qdate.isValid():
                        date_human = qdate.toString(date_format)
                        if time_value:
                            display_text = f"{text} — {date_human} {time_value}"

                        else:
                            display_text = f"{text} — {date_human}"

                        tooltip_lines.append(f"{get_text('Data') or 'Data'}: {date_human}")

                if time_value:
                    tooltip_lines.append(f"{get_text('Horário') or 'Horário'}: {time_value}")

                item = QListWidgetItem(display_text)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setCheckState(Qt.Checked if completed else Qt.Unchecked)
                item.setData(Qt.UserRole, {"text": text, "date": date_value, "time": time_value})
                if tooltip_lines:
                    item.setToolTip("\n".join(tooltip_lines))

                return item

            def populate_list(key, lst, completed=False):
                if key in tasks and tasks[key]:
                    lst.clear()
                    for entry in tasks[key]:
                        if isinstance(entry, dict):
                            text = entry.get("text", "")
                            date_value = entry.get("date")
                            time_value = entry.get("time")

                        else:
                            text = str(entry)
                            date_value = None
                            time_value = None

                        text = text.strip()
                        if not text:
                            continue

                        item = create_item(text, date_value, time_value, completed)
                        if hasattr(app, "insert_task_into_quadrant_list"):
                            app.insert_task_into_quadrant_list(lst, item)

                        else:
                            lst.addItem(item)

            populate_list("quadrant1", app.quadrant1_list, completed=False)
            populate_list("quadrant1_completed", app.quadrant1_completed_list, completed=True)
            populate_list("quadrant2", app.quadrant2_list, completed=False)
            populate_list("quadrant2_completed", app.quadrant2_completed_list, completed=True)
            populate_list("quadrant3", app.quadrant3_list, completed=False)
            populate_list("quadrant3_completed", app.quadrant3_completed_list, completed=True)
            populate_list("quadrant4", app.quadrant4_list, completed=False)
            populate_list("quadrant4_completed", app.quadrant4_completed_list, completed=True)

    except FileNotFoundError:
        pass

    except Exception as e:
        logger.error(f"Erro ao carregar tarefas: {e}", exc_info=True)
