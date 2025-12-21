import os
from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QPushButton
from source.utils.IconUtils import get_icon_path
from source.utils.CaminhoPersistenteUtils import obter_caminho_persistente
from source.language.tr_01_gerenciadorTraducao import GerenciadorTraducao
from source.InterfaceCore.incore_01_initUI import init_ui as core_init_ui
from source.InterfaceCore.incore_02_add_placeholder import add_placeholder as core_add_placeholder
from source.InterfaceCore.incore_03_criar_menu_configuracoes import criar_menu_configuracoes as core_criar_menu
from source.InterfaceCore.incore_04_definir_idioma import definir_idioma as core_definir_idioma
from source.InterfaceCore.incore_05_atualizar_textos import atualizar_textos as core_atualizar_textos
from source.InterfaceCore.incore_06_atualizar_placeholders import atualizar_placeholders as core_atualizar_placeholders
from source.InterfaceCore.incore_07_show_context_menu import show_context_menu as core_show_context_menu
from source.InterfaceCore.incore_08_exibir_sobre import exibir_sobre as core_exibir_sobre
from source.InterfaceCore.incore_09_arquivo import novo as arquivo_novo, abrir_arquivo as arquivo_abrir, salvar_como as arquivo_salvar, limpar_tudo as arquivo_limpar, sair as arquivo_sair
from source.GerenciamentoUI.ui_03_add_task import add_task as ui_add_task
from source.GerenciamentoUI.ui_04_handle_item_checked import handle_item_checked as ui_handle_item_checked
from source.GerenciamentoUI.ui_05_move_item_between_lists import move_item_between_lists as ui_move_item_between_lists
from source.GerenciamentoUI.ui_06_remove_task import remove_task as ui_remove_task
from source.GerenciamentoUI.ui_07_save_tasks import save_tasks as ui_save_tasks
from source.GerenciamentoUI.ui_08_load_tasks import load_tasks as ui_load_tasks
from source.GerenciamentoUI.ui_09_Calendar import Calendar
from source.GerenciamentoUI.ui_10_edit_task import edit_task_datetime as ui_edit_task_datetime
from source.GerenciamentoUI.ui_10_edit_task import move_task_to_quadrant as ui_move_task_to_quadrant
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)


class EisenhowerMatrixApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gerenciador_traducao = GerenciadorTraducao()
        self.gerenciador_traducao.idioma_alterado.connect(self.atualizar_textos)
        self.gerenciador_traducao.aplicar_traducao()

        self.setWindowTitle(get_text("Matriz de Eisenhower - Organizador de Tarefas"))
        self.setGeometry(100, 100, 1000, 700)

        icon_path = get_icon_path("organizador.ico")
        if icon_path:
            from PySide6.QtGui import QIcon
            self.setWindowIcon(QIcon(icon_path))

        self.tasks_path = os.path.join(obter_caminho_persistente(), "tasks.json")

        self.initUI()
        self.load_tasks()
        self.criar_menu_configuracoes()

    def criar_menu_configuracoes(self):
        core_criar_menu(self)

    def definir_idioma(self, codigo_idioma):
        core_definir_idioma(self, codigo_idioma)

    def initUI(self):
        core_init_ui(self)
        try:
            old_central = self.centralWidget()
            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

            self.calendar_pane = Calendar(self)
            layout.addWidget(self.calendar_pane, 0, Qt.AlignLeft)
            layout.addWidget(old_central, 1)

            self.setCentralWidget(container)
            self._hide_legacy_calendar_button()

        except Exception as e:
            logger.error(f"Erro ao inicializar UI: {e}", exc_info=True)

    def _hide_legacy_calendar_button(self):
        try:
            for btn in self.findChildren(QPushButton):
                if btn.text().strip().lower() in {
                    get_text("Calendário").strip().lower(),
                    "calendário", "calendario", "calendar"
                }:
                    btn.hide()

        except Exception as e:
            logger.error(f"Erro ao ocultar botão legado do calendário: {e}", exc_info=True)

    def add_placeholder(self, list_widget, text):
        core_add_placeholder(self, list_widget, text)

    def _is_group_header(self, item):
        try:
            return item.data(Qt.UserRole + 1) == "group_header"

        except Exception:
            return False

    def _time_group_label(self, time_str: str) -> str:
        try:
            hh = int((time_str or "0:0").split(":")[0])

        except Exception:
            hh = 0

        return f"{hh:02d}:00–{hh:02d}:59"

    def _time_key(self, time_str: str):
        if not time_str:
            return (999, 999)

        try:
            parts = time_str.split(":")
            return (int(parts[0]), int(parts[1]))

        except Exception:
            return (999, 999)

    def insert_task_into_quadrant_list(self, lst, item):
        data = item.data(Qt.UserRole) or {}
        time_str = data.get("time")
        if not time_str:
            lst.addItem(item)
            return

        if lst.count() == 1 and not (lst.item(0).flags() & Qt.ItemIsSelectable):
            lst.clear()

        label = self._time_group_label(time_str)

        header_index = None
        insert_header_index = None
        existing_headers = []
        for i in range(lst.count()):
            it = lst.item(i)
            if not it:
                continue

            if self._is_group_header(it):
                existing_headers.append((i, it.text()))

        for idx, text in existing_headers:
            if text == label:
                header_index = idx
                break

        if header_index is None:
            try:
                hour = int(label.split(":")[0])

            except Exception:
                hour = 0

            insert_header_index = lst.count()
            for idx, text in existing_headers:
                try:
                    h2 = int(text.split(":")[0])

                except Exception:
                    h2 = 0

                if hour < h2:
                    insert_header_index = idx
                    break

            from PySide6.QtWidgets import QListWidgetItem
            header = QListWidgetItem(label)
            from PySide6.QtCore import Qt as _Qt
            header.setFlags((header.flags() & ~_Qt.ItemIsSelectable) & ~_Qt.ItemIsEnabled)
            header.setData(_Qt.UserRole + 1, "group_header")
            lst.insertItem(insert_header_index, header)
            header_index = insert_header_index

        start = header_index + 1
        end = lst.count()
        for i in range(start, lst.count()):
            it = lst.item(i)
            if it and self._is_group_header(it):
                end = i
                break

        new_key = (self._time_key(time_str), (data.get("text") or item.text()).lower())
        pos = end
        for i in range(start, end):
            it = lst.item(i)
            idata = it.data(Qt.UserRole) or {}
            ikey = (self._time_key(idata.get("time")), (idata.get("text") or it.text()).lower())
            if new_key < ikey:
                pos = i
                break

        lst.insertItem(pos, item)

    def cleanup_time_groups(self, lst):
        i = 0
        from PySide6.QtCore import Qt as _Qt
        while i < lst.count():
            it = lst.item(i)
            if it and self._is_group_header(it):
                if i + 1 >= lst.count() or self._is_group_header(lst.item(i + 1)) or (lst.item(i + 1).flags() & _Qt.ItemIsSelectable) == 0:
                    j = i + 1
                    found_task = False
                    while j < lst.count():
                        it2 = lst.item(j)
                        if self._is_group_header(it2):
                            break

                        if it2.flags() & _Qt.ItemIsSelectable:
                            found_task = True
                            break

                        j += 1

                    if not found_task:
                        lst.takeItem(i)
                        continue

            i += 1

    def add_task(self):
        ui_add_task(self)
        try:
            if hasattr(self, "calendar_pane") and self.calendar_pane:
                self.calendar_pane.calendar_panel.update_task_list()

        except Exception as e:
            logger.error(f"Erro ao atualizar lista de tarefas no calendário: {e}", exc_info=True)

    def handle_item_checked(self, item, source_list, target_list):
        ui_handle_item_checked(self, item, source_list, target_list)

    def move_item_between_lists(self, item, source, target, new_check_state):
        ui_move_item_between_lists(self, item, source, target, new_check_state)

    def remove_task(self, item, list_widget):
        ui_remove_task(self, item, list_widget)
        try:
            self.cleanup_time_groups(list_widget)
            if hasattr(self, "calendar_pane") and self.calendar_pane:
                self.calendar_pane.calendar_panel.update_task_list()

        except Exception as e:
            logger.error(f"Erro ao remover tarefa: {e}", exc_info=True)

    def save_tasks(self):
        ui_save_tasks(self)

    def load_tasks(self):
        ui_load_tasks(self)
        try:
            if hasattr(self, "calendar_pane") and self.calendar_pane:
                self.calendar_pane.calendar_panel.update_task_list()

        except Exception as e:
            logger.error(f"Erro ao carregar tarefas: {e}", exc_info=True)

    def atualizar_textos(self):
        core_atualizar_textos(self)
        try:
            if hasattr(self, "calendar_pane") and self.calendar_pane:
                self.calendar_pane.on_language_changed()

        except Exception as e:
            logger.error(f"Erro ao atualizar textos: {e}", exc_info=True)

    def atualizar_placeholders(self):
        core_atualizar_placeholders(self)

    def exibir_sobre(self):
        core_exibir_sobre(self)

    def show_context_menu(self, point, list_widget):
        core_show_context_menu(self, point, list_widget)

    def open_calendar(self):
        try:
            if hasattr(self, "calendar_pane") and self.calendar_pane:
                self.calendar_pane.toggle_panel(open_if_hidden=True)

        except Exception as e:
            logger.error(f"Erro ao abrir calendário: {e}", exc_info=True)

    def nova_sessao(self):
        arquivo_novo(self)

    def abrir_arquivo(self):
        arquivo_abrir(self)

    def salvar_como(self):
        arquivo_salvar(self)

    def limpar_tudo(self):
        arquivo_limpar(self)

    def sair_app(self):
        arquivo_sair(self)

    def edit_task_datetime(self, item, list_widget):
        ui_edit_task_datetime(self, item, list_widget)

    def move_task_to_quadrant(self, item, source_list, target_list):
        ui_move_task_to_quadrant(self, item, source_list, target_list)
