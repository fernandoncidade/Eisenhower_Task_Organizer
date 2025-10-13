from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import QListWidgetItem, QMessageBox

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)

def add_task(app):
    task_text = app.task_input.text().strip()
    if not task_text:
        QMessageBox.warning(app, get_text("Erro"), get_text("A tarefa não pode estar vazia."))
        return

    selected_quadrant = app.quadrant_selector.currentIndex()

    def clear_placeholder_if_needed(lst):
        if lst.count() == 1 and not (lst.item(0).flags() & Qt.ItemIsSelectable):
            lst.clear()

    clear_placeholder_if_needed(app.quadrant1_list)
    clear_placeholder_if_needed(app.quadrant2_list)
    clear_placeholder_if_needed(app.quadrant3_list)
    clear_placeholder_if_needed(app.quadrant4_list)

    task_item = QListWidgetItem(task_text)
    task_item.setFlags(task_item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    task_item.setCheckState(Qt.Unchecked)

    if selected_quadrant == 0:
        app.quadrant1_list.addItem(task_item)

    elif selected_quadrant == 1:
        app.quadrant2_list.addItem(task_item)

    elif selected_quadrant == 2:
        app.quadrant3_list.addItem(task_item)

    elif selected_quadrant == 3:
        app.quadrant4_list.addItem(task_item)

    app.task_input.clear()
    app.save_tasks()
