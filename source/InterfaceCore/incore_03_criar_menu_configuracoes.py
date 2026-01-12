from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import QCoreApplication
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)

def criar_menu_configuracoes(app):
    try:
        mb = app.menuBar()
        for act in list(mb.actions()):
            mb.removeAction(act)

        arquivo_menu = QMenu(get_text("Arquivo"), app)
        acao_novo = QAction(get_text("Novo"), app)
        acao_novo.triggered.connect(app.nova_sessao)
        arquivo_menu.addAction(acao_novo)

        acao_abrir = QAction(get_text("Abrir"), app)
        acao_abrir.triggered.connect(app.abrir_arquivo)
        arquivo_menu.addAction(acao_abrir)

        acao_salvar = QAction(get_text("Salvar"), app)
        acao_salvar.triggered.connect(app.salvar_como)
        arquivo_menu.addAction(acao_salvar)

        acao_limpar = QAction(get_text("Limpar"), app)
        acao_limpar.triggered.connect(app.limpar_tudo)
        arquivo_menu.addAction(acao_limpar)

        arquivo_menu.addSeparator()
        acao_sair = QAction(get_text("Sair"), app)
        acao_sair.triggered.connect(app.sair_app)
        arquivo_menu.addAction(acao_sair)
        app.menuBar().addMenu(arquivo_menu)

        config_menu = QMenu(get_text("Configurações"), app)
        idioma_menu = QMenu(get_text("Idioma"), app)

        for codigo, nome in app.gerenciador_traducao.idiomas_disponiveis.items():
            acao_idioma = QAction(nome, app)
            acao_idioma.setCheckable(True)
            acao_idioma.setChecked(app.gerenciador_traducao.obter_idioma_atual() == codigo)
            acao_idioma.triggered.connect(lambda checked, c=codigo: app.definir_idioma(c))
            idioma_menu.addAction(acao_idioma)

        config_menu.addMenu(idioma_menu)

        acao_calendario = QAction(get_text("Calendário"), app)
        acao_calendario.triggered.connect(app.open_calendar)
        config_menu.addAction(acao_calendario)

        opcoes_menu = QMenu(get_text("Opções"), app)
        acao_sobre = QAction(get_text("Sobre"), app)
        acao_sobre.triggered.connect(app.exibir_sobre)
        opcoes_menu.addAction(acao_sobre)

        app.menuBar().addMenu(config_menu)
        app.menuBar().addMenu(opcoes_menu)

        app.menu_bar = app.menuBar()
        app.idioma_menu = idioma_menu

    except Exception as e:
        logger.error(f"Erro ao criar menu de configurações: {e}", exc_info=True)
