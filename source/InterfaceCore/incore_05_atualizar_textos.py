from PySide6.QtCore import QCoreApplication

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)

def atualizar_textos(app):
    app.setWindowTitle(get_text("Matriz de Eisenhower - Organizador de Tarefas"))
    app.task_input.setPlaceholderText(get_text("Adicione uma tarefa..."))
    app.add_button.setText(get_text("Adicionar Tarefa"))
    app.quadrant_selector.clear()
    app.quadrant_selector.addItems([
        get_text("Importante e Urgente"),
        get_text("Importante, mas Não Urgente"),
        get_text("Não Importante, mas Urgente"),
        get_text("Não Importante e Não Urgente")
    ])
    app.quadrant1_label.setText(get_text("Importante e Urgente"))
    app.quadrant2_label.setText(get_text("Importante, mas Não Urgente"))
    app.quadrant3_label.setText(get_text("Não Importante, mas Urgente"))
    app.quadrant4_label.setText(get_text("Não Importante e Não Urgente"))

    app.quadrant1_completed_label.setText(get_text("Concluídas"))
    app.quadrant2_completed_label.setText(get_text("Concluídas"))
    app.quadrant3_completed_label.setText(get_text("Concluídas"))
    app.quadrant4_completed_label.setText(get_text("Concluídas"))

    if app.quadrant1_list.count() == 0:
        app.add_placeholder(app.quadrant1_list, get_text("1º Quadrante"))

    if app.quadrant2_list.count() == 0:
        app.add_placeholder(app.quadrant2_list, get_text("2º Quadrante"))

    if app.quadrant3_list.count() == 0:
        app.add_placeholder(app.quadrant3_list, get_text("3º Quadrante"))

    if app.quadrant4_list.count() == 0:
        app.add_placeholder(app.quadrant4_list, get_text("4º Quadrante"))

    if app.quadrant1_completed_list.count() == 0:
        app.add_placeholder(app.quadrant1_completed_list, get_text("Nenhuma Tarefa Concluída"))

    if app.quadrant2_completed_list.count() == 0:
        app.add_placeholder(app.quadrant2_completed_list, get_text("Nenhuma Tarefa Concluída"))

    if app.quadrant3_completed_list.count() == 0:
        app.add_placeholder(app.quadrant3_completed_list, get_text("Nenhuma Tarefa Concluída"))

    if app.quadrant4_completed_list.count() == 0:
        app.add_placeholder(app.quadrant4_completed_list, get_text("Nenhuma Tarefa Concluída"))

    app.atualizar_placeholders()
    app.criar_menu_configuracoes()
