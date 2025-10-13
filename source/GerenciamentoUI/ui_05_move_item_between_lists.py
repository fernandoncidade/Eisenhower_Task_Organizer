from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtCore import QCoreApplication

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)

def move_item_between_lists(app, item, source, target, new_check_state):
    text = item.text()
    row = source.row(item)
    source.takeItem(row)

    if source.count() == 0:
        if source in (app.quadrant1_list,):
            app.add_placeholder(app.quadrant1_list, get_text("1º Quadrante"))

        if source in (app.quadrant2_list,):
            app.add_placeholder(app.quadrant2_list, get_text("2º Quadrante"))

        if source in (app.quadrant3_list,):
            app.add_placeholder(app.quadrant3_list, get_text("3º Quadrante"))

        if source in (app.quadrant4_list,):
            app.add_placeholder(app.quadrant4_list, get_text("4º Quadrante"))

        if source in (app.quadrant1_completed_list,):
            app.add_placeholder(app.quadrant1_completed_list, get_text("Nenhuma Tarefa Concluída"))

        if source in (app.quadrant2_completed_list,):
            app.add_placeholder(app.quadrant2_completed_list, get_text("Nenhuma Tarefa Concluída"))

        if source in (app.quadrant3_completed_list,):
            app.add_placeholder(app.quadrant3_completed_list, get_text("Nenhuma Tarefa Concluída"))

        if source in (app.quadrant4_completed_list,):
            app.add_placeholder(app.quadrant4_completed_list, get_text("Nenhuma Tarefa Concluída"))

    if target.count() == 1 and not (target.item(0).flags() & Qt.ItemIsSelectable):
        target.clear()

    new_item = QListWidgetItem(text)
    new_item.setFlags(new_item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    new_item.setCheckState(new_check_state)
    target.addItem(new_item)
