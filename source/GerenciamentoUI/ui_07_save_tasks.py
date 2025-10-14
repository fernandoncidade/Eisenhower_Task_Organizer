import json
from PySide6.QtCore import Qt

def save_tasks(app):
    def list_to_entries(lst):
        entries = []
        for i in range(lst.count()):
            item = lst.item(i)
            if item.flags() & Qt.ItemIsSelectable:
                data = item.data(Qt.UserRole) or {}
                text = data.get("text", item.text())
                date = data.get("date")
                entries.append({"text": text, "date": date})

        return entries

    tasks = {
        "quadrant1": list_to_entries(app.quadrant1_list),
        "quadrant1_completed": list_to_entries(app.quadrant1_completed_list),
        "quadrant2": list_to_entries(app.quadrant2_list),
        "quadrant2_completed": list_to_entries(app.quadrant2_completed_list),
        "quadrant3": list_to_entries(app.quadrant3_list),
        "quadrant3_completed": list_to_entries(app.quadrant3_completed_list),
        "quadrant4": list_to_entries(app.quadrant4_list),
        "quadrant4_completed": list_to_entries(app.quadrant4_completed_list),
    }
    with open(app.tasks_path, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=2)
