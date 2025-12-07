from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextBrowser, QSizePolicy, QHBoxLayout, QWidget, QTabWidget
from PySide6.QtCore import Qt
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

            history_browser = QTextBrowser()
            history_browser.setReadOnly(True)
            history_browser.setOpenExternalLinks(True)
            if texto_history:
                history_browser.setPlainText(texto_history)

            else:
                history_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            self.tabs.addTab(history_browser, sh_history)

            detalhes_browser = QTextBrowser()
            detalhes_browser.setReadOnly(True)
            detalhes_browser.setOpenExternalLinks(True)
            if detalhes:
                detalhes_browser.setPlainText(detalhes)

            else:
                detalhes_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            self.tabs.addTab(detalhes_browser, sh_details)

            licencas_browser = QTextBrowser()
            licencas_browser.setReadOnly(True)
            licencas_browser.setOpenExternalLinks(True)
            if licencas:
                texto_html = licencas.replace('\n', '<br>')
                texto_html += f"<br><br><h3>{site_oficial_text}</h3><ul>"
                for site in sites_licencas.strip().split('\n'):
                    if site.strip():
                        texto_html += f'<li><a href="{site.strip()}">{site.strip()}</a></li>'
                texto_html += "</ul>"
                licencas_browser.setHtml(texto_html)

            else:
                licencas_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            self.tabs.addTab(licencas_browser, sh_licenses)

            avisos_browser = QTextBrowser()
            avisos_browser.setReadOnly(True)
            avisos_browser.setOpenExternalLinks(True)
            if avisos:
                avisos_browser.setPlainText(avisos)

            else:
                avisos_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            self.tabs.addTab(avisos_browser, sh_notices)

            privacidade_browser = QTextBrowser()
            privacidade_browser.setReadOnly(True)
            privacidade_browser.setOpenExternalLinks(True)
            if Privacy_Policy:
                privacidade_browser.setPlainText(Privacy_Policy)

            else:
                privacidade_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            self.tabs.addTab(privacidade_browser, sh_privacy)

            release_notes_browser = QTextBrowser()
            release_notes_browser.setReadOnly(True)
            release_notes_browser.setOpenExternalLinks(True)
            if release_notes:
                release_notes_browser.setPlainText(release_notes)

            else:
                release_notes_browser.setHtml(f"<p>{info_not_available_text}.</p>")

            self.tabs.addTab(release_notes_browser, sh_release)

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
