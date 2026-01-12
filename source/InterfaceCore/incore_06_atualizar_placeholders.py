from PySide6.QtCore import Qt, QCoreApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)

def atualizar_placeholders(app):
    try:
        placeholder_role = Qt.UserRole + 2
        group_header_role = Qt.UserRole + 1
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
            if lst is None:
                continue

            for i in range(lst.count()):
                item = lst.item(i)
                if not item:
                    continue

                is_placeholder = item.data(placeholder_role) is True

                if not is_placeholder:
                    try:
                        is_group_header = item.data(group_header_role) == "group_header"

                    except Exception:
                        is_group_header = False

                    if (not (item.flags() & Qt.ItemIsSelectable)) and (item.data(Qt.UserRole) is None) and (not is_group_header):
                        is_placeholder = True

                if is_placeholder:
                    item.setText(texto)
                    break

    except Exception as e:
        logger.error(f"Erro ao atualizar placeholders: {e}", exc_info=True)
