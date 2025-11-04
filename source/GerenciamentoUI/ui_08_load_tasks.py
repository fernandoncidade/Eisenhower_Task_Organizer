import json
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt

def load_tasks(app):
    try:
        with open(app.tasks_path, "r", encoding="utf-8") as file:
            tasks = json.load(file)
            def populate_list(key, lst, completed=False):
                if key in tasks and tasks[key]:
                    lst.clear()
                    for task in tasks[key]:
                        item = QListWidgetItem(task)
                        item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        item.setCheckState(Qt.Checked if completed else Qt.Unchecked)
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
