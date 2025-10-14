import json
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt, QDate, QCoreApplication

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)

def load_tasks(app):
    try:
        with open(app.tasks_path, "r", encoding="utf-8") as file:
            tasks = json.load(file)
            date_format = app.date_input.displayFormat() if hasattr(app, "date_input") else "dd/MM/yyyy"

            def create_item(text, date_value, completed):
                display_text = text
                tooltip = ""
                if date_value:
                    qdate = QDate.fromString(date_value, Qt.ISODate)
                    if qdate.isValid():
                        date_human = qdate.toString(date_format)
                        display_text = f"{text} — {date_human}"
                        tooltip = f"{get_text('Data') or 'Data'}: {date_human}"

                item = QListWidgetItem(display_text)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setCheckState(Qt.Checked if completed else Qt.Unchecked)
                item.setData(Qt.UserRole, {"text": text, "date": date_value})
                if tooltip:
                    item.setToolTip(tooltip)

                return item

            def populate_list(key, lst, completed=False):
                if key in tasks and tasks[key]:
                    lst.clear()
                    for entry in tasks[key]:
                        if isinstance(entry, dict):
                            text = entry.get("text", "")
                            date_value = entry.get("date")

                        else:
                            text = str(entry)
                            date_value = None

                        text = text.strip()
                        if not text:
                            continue

                        item = create_item(text, date_value, completed)
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
