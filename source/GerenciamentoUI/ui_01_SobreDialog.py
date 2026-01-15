from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextBrowser, QSizePolicy, QHBoxLayout, QWidget, QTabWidget
from PySide6.QtCore import Qt, QCoreApplication, QEvent
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()


class SobreDialog(QDialog):
    def __init__(self, parent, titulo, texto_fixo, texto_history, detalhes, licencas, sites_licencas, 
                 show_history_text=None, hide_history_text=None, 
                 show_details_text=None, hide_details_text=None, 
                 show_licenses_text=None, hide_licenses_text=None, 
                 ok_text=None, site_oficial_text=None, avisos=None, 
                 show_notices_text=None, hide_notices_text=None, 
                 Privacy_Policy=None, show_privacy_policy_text=None, hide_privacy_policy_text=None, 
                 info_not_available_text="Information not available", 
                 release_notes=None, show_release_notes_text=None, hide_release_notes_text=None):
        super().__init__(parent)
        try:
            self.setWindowTitle(titulo)
            self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
            self.setModal(False)

            layout = QVBoxLayout(self)

            header_widget = QWidget()
            header_layout = QVBoxLayout(header_widget)
            header_layout.setContentsMargins(0, 0, 0, 0)
            header_layout.setSpacing(5)

            self.fixed_label = QLabel(texto_fixo)
            self.fixed_label.setTextFormat(Qt.TextFormat.RichText)
            self.fixed_label.setWordWrap(True)
            self.fixed_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            self.fixed_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
            header_layout.addWidget(self.fixed_label)

            header_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
            layout.addWidget(header_widget)

            sh_history = show_history_text or "Histórico"
            hi_history = hide_history_text or "Ocultar histórico"
            sh_details = show_details_text or "Detalhes"
            hi_details = hide_details_text or "Ocultar detalhes"
            sh_licenses = show_licenses_text or "Licenças"
            hi_licenses = hide_licenses_text or "Ocultar licenças"
            sh_notices = show_notices_text or "Avisos"
            hi_notices = hide_notices_text or "Ocultar avisos"
            sh_privacy = show_privacy_policy_text or "Política de privacidade"
            hi_privacy = hide_privacy_policy_text or "Ocultar política de privacidade"
            sh_release = show_release_notes_text or "Notas de versão"
            hi_release = hide_release_notes_text or "Ocultar notas de versão"
            ok_text = ok_text or "OK"
            site_oficial_text = site_oficial_text or "Official site"

            self.tabs = QTabWidget()
            self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            self.history_browser = QTextBrowser()
            self.history_browser.setReadOnly(True)
            self.history_browser.setOpenExternalLinks(True)

            if texto_history:
                self.history_browser.setPlainText(texto_history)

            else:
                self.history_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            self.tabs.addTab(self.history_browser, sh_history)

            self.detalhes_browser = QTextBrowser()
            self.detalhes_browser.setReadOnly(True)
            self.detalhes_browser.setOpenExternalLinks(True)

            if detalhes:
                self.detalhes_browser.setPlainText(detalhes)

            else:
                self.detalhes_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            self.tabs.addTab(self.detalhes_browser, sh_details)

            self.licencas_browser = QTextBrowser()
            self.licencas_browser.setReadOnly(True)
            self.licencas_browser.setOpenExternalLinks(True)

            if licencas:
                texto_html = licencas.replace('\n', '<br>')
                texto_html += f"<br><br><h3>{site_oficial_text}</h3><ul>"
                for site in sites_licencas.strip().split('\n'):
                    if site.strip():
                        texto_html += f'<li><a href="{site.strip()}">{site.strip()}</a></li>'
                texto_html += "</ul>"
                self.licencas_browser.setHtml(texto_html)

            else:
                self.licencas_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            self.tabs.addTab(self.licencas_browser, sh_licenses)

            self.avisos_browser = QTextBrowser()
            self.avisos_browser.setReadOnly(True)
            self.avisos_browser.setOpenExternalLinks(True)

            if avisos:
                self.avisos_browser.setPlainText(avisos)

            else:
                self.avisos_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            self.tabs.addTab(self.avisos_browser, sh_notices)

            self.privacidade_browser = QTextBrowser()
            self.privacidade_browser.setReadOnly(True)
            self.privacidade_browser.setOpenExternalLinks(True)

            if Privacy_Policy:
                self.privacidade_browser.setPlainText(Privacy_Policy)

            else:
                self.privacidade_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            self.tabs.addTab(self.privacidade_browser, sh_privacy)

            self.release_notes_browser = QTextBrowser()
            self.release_notes_browser.setReadOnly(True)
            self.release_notes_browser.setOpenExternalLinks(True)

            if release_notes:
                self.release_notes_browser.setPlainText(release_notes)

            else:
                self.release_notes_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            self.tabs.addTab(self.release_notes_browser, sh_release)

            self._tab_show_texts = [
                sh_history,
                sh_details,
                sh_licenses,
                sh_notices,
                sh_privacy,
                sh_release
            ]

            self._tab_hide_texts = [
                hi_history,
                hi_details,
                hi_licenses,
                hi_notices,
                hi_privacy,
                hi_release
            ]

            self.tabs.currentChanged.connect(self._on_tab_changed)
            self._update_tab_labels(self.tabs.currentIndex())

            layout.addWidget(self.tabs)

            button_layout = QHBoxLayout()
            self.ok_button = QPushButton(ok_text)
            self.ok_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            self.ok_button.clicked.connect(self.accept)
            button_layout.addStretch(1)
            button_layout.addWidget(self.ok_button)
            layout.addLayout(button_layout)

            self.setMinimumSize(400, 200)

        except Exception as e:
            logger.error(f"Erro ao criar dialog sobre: {e}", exc_info=True)

    def _on_tab_changed(self, index):
        try:
            self._update_tab_labels(index)

        except Exception as e:
            logger.error(f"Erro ao atualizar rótulos das abas: {e}", exc_info=True)

    def _update_tab_labels(self, current_index):
        count = self.tabs.count()
        while len(self._tab_show_texts) < count:
            self._tab_show_texts.append("")

        while len(self._tab_hide_texts) < count:
            self._tab_hide_texts.append("")

        for i in range(count):
            show = self._tab_show_texts[i] or ""
            hide = self._tab_hide_texts[i] or ""
            self.tabs.setTabText(i, hide if i == current_index else show)

    def changeEvent(self, event: QEvent) -> None:
        super().changeEvent(event)
        if event.type() == QEvent.Type.LanguageChange:
            try:
                self._retranslate_ui()

            except Exception:
                logger.debug("Falha ao retraduzir SobreDialog", exc_info=True)

    def _tr_multi(self, key: str) -> str:
        val = QCoreApplication.translate("App", key)
        if val and val != key:
            return val

        val = QCoreApplication.translate("InterfaceGrafica", key)
        return val if val and val != key else key

    def _retranslate_ui(self) -> None:
        version_label = self._tr_multi('version') or 'Version'
        authors_label = self._tr_multi('authors') or 'Authors'
        description_label = self._tr_multi('description_text') or ''

        cabecalho = (
            "<h3>EISENHOWER ORGANIZER</h3>"
            f"<p><b>{version_label}:</b> 0.0.7.0</p>"
            f"<p><b>{authors_label}:</b> Fernando Nillsson Cidade</p>"
            f"<p><b>{self._tr_multi('description') or 'Description'}:</b> {description_label}</p>"
        )
        try:
            self.fixed_label.setText(cabecalho)

        except Exception:
            pass

        try:
            from source.GerenciamentoUI.ui_02_OpcoesSobre import (
                SITE_LICENSES,
                LICENSE_TEXT_PT_BR, LICENSE_TEXT_EN_US,
                NOTICE_TEXT_PT_BR, NOTICE_TEXT_EN_US,
                ABOUT_TEXT_PT_BR, ABOUT_TEXT_EN_US,
                Privacy_Policy_pt_BR, Privacy_Policy_en_US,
                History_APP_pt_BR, History_APP_en_US,
                RELEASE_NOTES_pt_BR, RELEASE_NOTES_en_US,
            )

        except Exception:
            logger.debug("Falha ao importar constantes de OpcoesSobre para retraducao", exc_info=True)

        idioma = 'pt_BR'
        try:
            parent = self.parent()
            if hasattr(parent, 'gerenciador_traducao') and parent.gerenciador_traducao:
                idioma = parent.gerenciador_traducao.obter_idioma_atual() or 'pt_BR'

        except Exception:
            pass

        if idioma == 'pt_BR':
            history = History_APP_pt_BR
            detalhes = ABOUT_TEXT_PT_BR
            licencas = LICENSE_TEXT_PT_BR
            avisos = NOTICE_TEXT_PT_BR
            priv = Privacy_Policy_pt_BR
            release = RELEASE_NOTES_pt_BR

        else:
            history = History_APP_en_US
            detalhes = ABOUT_TEXT_EN_US
            licencas = LICENSE_TEXT_EN_US
            avisos = NOTICE_TEXT_EN_US
            priv = Privacy_Policy_en_US
            release = RELEASE_NOTES_en_US

        info_nao = self._tr_multi('information_not_available') or 'Information not available'

        try:
            if history:
                self.history_browser.setPlainText(history)

            else:
                self.history_browser.setHtml(f"<p>{info_nao}.</p>")

            if detalhes:
                self.detalhes_browser.setPlainText(detalhes)

            else:
                self.detalhes_browser.setHtml(f"<p>{info_nao}.</p>")

            if licencas:
                texto_html = licencas.replace('\n', '<br>')
                texto_html += f"<br><br><h3>{self._tr_multi('site_oficial') or 'Official site'}</h3><ul>"
                for site in SITE_LICENSES.strip().split('\n'):
                    if site.strip():
                        texto_html += f'<li><a href="{site.strip()}">{site.strip()}</a></li>'

                texto_html += "</ul>"
                self.licencas_browser.setHtml(texto_html)

            else:
                self.licencas_browser.setHtml(f"<p>{info_nao}.</p>")

            if avisos:
                self.avisos_browser.setPlainText(avisos)

            else:
                self.avisos_browser.setHtml(f"<p>{info_nao}.</p>")

            if priv:
                self.privacidade_browser.setPlainText(priv)

            else:
                self.privacidade_browser.setHtml(f"<p>{info_nao}.</p>")

            if release:
                self.release_notes_browser.setPlainText(release)

            else:
                self.release_notes_browser.setHtml(f"<p>{info_nao}.</p>")

        except Exception:
            logger.debug("Falha ao atualizar conteúdos do diálogo Sobre", exc_info=True)

        sh_history = self._tr_multi('show_history') or 'History'
        hi_history = self._tr_multi('hide_history') or 'Hide history'
        sh_details = self._tr_multi('show_details') or 'Details'
        hi_details = self._tr_multi('hide_details') or 'Hide details'
        sh_licenses = self._tr_multi('show_licenses') or 'Licenses'
        hi_licenses = self._tr_multi('hide_licenses') or 'Hide licenses'
        sh_notices = self._tr_multi('show_notices') or 'Notices'
        hi_notices = self._tr_multi('hide_notices') or 'Hide notices'
        sh_privacy = self._tr_multi('show_privacy_policy') or 'Privacy Policy'
        hi_privacy = self._tr_multi('hide_privacy_policy') or 'Hide privacy policy'
        sh_release = self._tr_multi('show_release_notes') or 'Release Notes'
        hi_release = self._tr_multi('hide_release_notes') or 'Hide release notes'

        self._tab_show_texts = [sh_history, sh_details, sh_licenses, sh_notices, sh_privacy, sh_release]
        self._tab_hide_texts = [hi_history, hi_details, hi_licenses, hi_notices, hi_privacy, hi_release]

        try:
            self.ok_button.setText(self._tr_multi('OK') or 'OK')

        except Exception:
            pass

        self._update_tab_labels(self.tabs.currentIndex())
