import os
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QMainWindow
from utils.IconUtils import get_icon_path
from utils.CaminhoPersistenteUtils import obter_caminho_persistente
from language.tr_01_gerenciadorTraducao import GerenciadorTraducao
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

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)


class EisenhowerMatrixApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gerenciador_traducao = GerenciadorTraducao()
        self.gerenciador_traducao.idioma_alterado.connect(self.atualizar_textos)
        self.gerenciador_traducao.aplicar_traducao()

        self.setWindowTitle(get_text("Matriz de Eisenhower - Organizador de Tarefas"))
        self.setGeometry(100, 100, 900, 700)

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

    def add_placeholder(self, list_widget, text):
        core_add_placeholder(self, list_widget, text)

    def add_task(self):
        ui_add_task(self)

    def handle_item_checked(self, item, source_list, target_list):
        ui_handle_item_checked(self, item, source_list, target_list)

    def move_item_between_lists(self, item, source, target, new_check_state):
        ui_move_item_between_lists(self, item, source, target, new_check_state)

    def remove_task(self, item, list_widget):
        ui_remove_task(self, item, list_widget)

    def save_tasks(self):
        ui_save_tasks(self)

    def load_tasks(self):
        ui_load_tasks(self)

    def atualizar_textos(self):
        core_atualizar_textos(self)

    def atualizar_placeholders(self):
        core_atualizar_placeholders(self)

    def exibir_sobre(self):
        core_exibir_sobre(self)

    def show_context_menu(self, point, list_widget):
        core_show_context_menu(self, point, list_widget)

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
