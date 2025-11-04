from PySide6.QtCore import Qt, QCoreApplication

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)

def atualizar_placeholders(app):
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
    for lst, texto in placeholders.items():
        for i in range(lst.count()):
            item = lst.item(i)
            if item and not (item.flags() & Qt.ItemIsSelectable):
                item.setText(texto)
                break
