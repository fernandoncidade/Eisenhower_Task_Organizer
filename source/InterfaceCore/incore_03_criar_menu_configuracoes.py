from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction, QKeySequence, QShortcut
from PySide6.QtCore import QCoreApplication, Qt
from source.utils.LogManager import LogManager
from source.InterfaceCore.incore_08_exibir_sobre import exibir_manual as core_exibir_manual
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)

def criar_menu_configuracoes(app):
    try:
        mb = app.menuBar()
        for act in list(mb.actions()):
            mb.removeAction(act)

        # ARQUIVO MENU
        arquivo_menu = QMenu(get_text("Arquivo"), app)
        acao_novo = QAction(get_text("Novo"), app)

        try:
            acao_novo.setShortcut(QKeySequence.New)

        except Exception:
            pass

        acao_novo.triggered.connect(app.nova_sessao)
        arquivo_menu.addAction(acao_novo)

        # ABRIR MENU
        acao_abrir = QAction(get_text("Abrir"), app)

        try:
            acao_abrir.setShortcut(QKeySequence.Open)

        except Exception:
            pass

        acao_abrir.triggered.connect(app.abrir_arquivo)
        arquivo_menu.addAction(acao_abrir)

        # SALVAR MENU
        acao_salvar = QAction(get_text("Salvar"), app)

        try:
            acao_salvar.setShortcut(QKeySequence.Save)

        except Exception:
            pass

        acao_salvar.triggered.connect(app.salvar_como)
        arquivo_menu.addAction(acao_salvar)

        # LIMPAR MENU
        acao_limpar = QAction(get_text("Limpar"), app)

        try:
            acao_limpar.setShortcut(QKeySequence("Ctrl+Shift+L"))

        except Exception:
            pass

        acao_limpar.triggered.connect(app.limpar_tudo)
        arquivo_menu.addAction(acao_limpar)

        # SAIR MENU
        arquivo_menu.addSeparator()
        acao_sair = QAction(get_text("Sair"), app)

        try:
            acao_sair.setShortcut(QKeySequence("Ctrl+Q"))
            acao_sair.setShortcutContext(Qt.ApplicationShortcut)

        except Exception:
            pass

        acao_sair.triggered.connect(app.sair_app)
        arquivo_menu.addAction(acao_sair)
        app.menuBar().addMenu(arquivo_menu)

        try:
            for attr in ("atalho_arquivo",):
                old = getattr(app, attr, None)
                if old is not None:
                    try:
                        old.deleteLater()

                    except Exception:
                        pass

            def abrir_menu(menu, menubar):
                try:
                    geom = menubar.actionGeometry(menu.menuAction())
                    pos = menubar.mapToGlobal(geom.bottomLeft())
                    menu.popup(pos)

                except Exception:
                    try:
                        menu.popup(menu.pos())

                    except Exception:
                        pass

            app.atalho_arquivo = QShortcut(QKeySequence("Alt+A"), app)
            app.atalho_arquivo.setContext(Qt.ApplicationShortcut)
            app.atalho_arquivo.activated.connect(lambda m=arquivo_menu, mb=mb: abrir_menu(m, mb))

        except Exception:
            pass

        # CONFIGURAÇÕES MENU
        config_menu = QMenu(get_text("Configurações"), app)
        idioma_menu = QMenu(get_text("Idioma"), app)

        for codigo, nome in app.gerenciador_traducao.idiomas_disponiveis.items():
            acao_idioma = QAction(nome, app)
            acao_idioma.setCheckable(True)
            acao_idioma.setChecked(app.gerenciador_traducao.obter_idioma_atual() == codigo)
            acao_idioma.triggered.connect(lambda checked, c=codigo: app.definir_idioma(c))
            idioma_menu.addAction(acao_idioma)

        config_menu.addMenu(idioma_menu)

        try:
            old = getattr(app, "atalho_idioma", None)
            if old is not None:
                try:
                    old.deleteLater()

                except Exception:
                    pass

            app.atalho_idioma = QShortcut(QKeySequence("Alt+I"), app)
            app.atalho_idioma.setContext(Qt.ApplicationShortcut)
            app.atalho_idioma.activated.connect(lambda m=idioma_menu, mb=mb: abrir_menu(m, mb))

        except Exception:
            pass

        # CALENDÁRIO MENU
        acao_calendario = QAction(get_text("Calendário"), app)

        try:
            acao_calendario.setShortcut(QKeySequence("Ctrl+M"))

        except Exception:
            pass

        acao_calendario.triggered.connect(app.open_calendar)
        config_menu.addAction(acao_calendario)

        # OPÇÕES MENU
        opcoes_menu = QMenu(get_text("Opções"), app)
        try:
            old = getattr(app, "atalho_opcoes", None)
            if old is not None:
                try:
                    old.deleteLater()

                except Exception:
                    pass

            app.atalho_opcoes = QShortcut(QKeySequence("Alt+O"), app)
            app.atalho_opcoes.setContext(Qt.ApplicationShortcut)
            app.atalho_opcoes.activated.connect(lambda m=opcoes_menu, mb=mb: abrir_menu(m, mb))

        except Exception:
            pass

        # SOBRE MENU
        acao_sobre = QAction(get_text("Sobre"), app)

        try:
            acao_sobre.setShortcut(QKeySequence.HelpContents)

        except Exception:
            try:
                acao_sobre.setShortcut(QKeySequence("F1"))

            except Exception:
                pass

        acao_sobre.triggered.connect(app.exibir_sobre)
        opcoes_menu.addAction(acao_sobre)

        # MANUAL MENU
        acao_manual = QAction(get_text("Manual"), app)

        try:
            acao_manual.setShortcut(QKeySequence("Ctrl+Shift+M"))
            acao_manual.setShortcutContext(Qt.ApplicationShortcut)

        except Exception:
            pass

        acao_manual.triggered.connect(lambda: core_exibir_manual(app))
        opcoes_menu.addAction(acao_manual)

        app.menuBar().addMenu(config_menu)
        app.menuBar().addMenu(opcoes_menu)

        app.menu_bar = app.menuBar()
        app.idioma_menu = idioma_menu

    except Exception as e:
        logger.error(f"Erro ao criar menu de configurações: {e}", exc_info=True)
