from PySide6.QtCore import QCoreApplication
from source.GerenciamentoUI.ui_01_SobreDialog import SobreDialog
from source.GerenciamentoUI.ui_02_OpcoesSobre import (
    SITE_LICENSES,
    LICENSE_TEXT_PT_BR, LICENSE_TEXT_EN_US,
    NOTICE_TEXT_PT_BR, NOTICE_TEXT_EN_US,
    ABOUT_TEXT_PT_BR, ABOUT_TEXT_EN_US,
    Privacy_Policy_pt_BR, Privacy_Policy_en_US,
    History_APP_pt_BR, History_APP_en_US,
    RELEASE_NOTES_pt_BR, RELEASE_NOTES_en_US
)
from PySide6.QtWidgets import QMessageBox
from utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)

def exibir_sobre(app):
    try:
        idioma = app.gerenciador_traducao.obter_idioma_atual()
        textos_sobre = { "pt_BR": ABOUT_TEXT_PT_BR, "en_US": ABOUT_TEXT_EN_US }
        textos_licenca = { "pt_BR": LICENSE_TEXT_PT_BR, "en_US": LICENSE_TEXT_EN_US }
        textos_aviso = { "pt_BR": NOTICE_TEXT_PT_BR, "en_US": NOTICE_TEXT_EN_US }
        textos_privacidade = { "pt_BR": Privacy_Policy_pt_BR, "en_US": Privacy_Policy_en_US }
        history_texts = { "pt_BR": History_APP_pt_BR, "en_US": History_APP_en_US }
        release_notes_texts = { "pt_BR": RELEASE_NOTES_pt_BR, "en_US": RELEASE_NOTES_en_US }

        texto_sobre = textos_sobre.get(idioma, textos_sobre["en_US"])
        texto_licenca = textos_licenca.get(idioma, textos_licenca["en_US"])
        texto_aviso = textos_aviso.get(idioma, textos_aviso["en_US"])
        texto_privacidade = textos_privacidade.get(idioma, textos_privacidade["en_US"])
        texto_history = history_texts.get(idioma, history_texts["en_US"])
        texto_release_notes = release_notes_texts.get(idioma, release_notes_texts["en_US"])

        cabecalho_fixo = (
            "<h3>EISENHOWER ORGANIZER</h3>"
            f"<p><b>{get_text('version') or 'Version'}:</b> 0.0.3.0</p>"
            f"<p><b>{get_text('authors') or 'Authors'}:</b> Fernando Nillsson Cidade</p>"
            f"<p><b>{get_text('description') or 'Description'}:</b> {get_text('description_text') or ''}</p>"
        )

        dialog = SobreDialog(
            app,
            titulo=f"{get_text('Sobre') or 'Sobre'} - EISENHOWER ORGANIZER",
            texto_fixo=cabecalho_fixo,
            texto_history=texto_history,
            detalhes=texto_sobre,
            licencas=texto_licenca,
            sites_licencas=SITE_LICENSES,
            show_history_text=get_text("show_history") or "History",
            hide_history_text=get_text("hide_history") or "Hide history",
            show_details_text=get_text("show_details") or "Details",
            hide_details_text=get_text("hide_details") or "Hide details",
            show_licenses_text=get_text("show_licenses") or "Licenses",
            hide_licenses_text=get_text("hide_licenses") or "Hide licenses",
            ok_text=get_text("OK") or "OK",
            site_oficial_text=get_text("site_oficial") or "Official site",
            avisos=texto_aviso,
            show_notices_text=get_text("show_notices") or "Notices",
            hide_notices_text=get_text("hide_notices") or "Hide notices",
            Privacy_Policy=texto_privacidade,
            show_privacy_policy_text=get_text("show_privacy_policy") or "Privacy Policy",
            hide_privacy_policy_text=get_text("hide_privacy_policy") or "Hide privacy policy",
            info_not_available_text=get_text("information_not_available") or "Information not available",
            release_notes=texto_release_notes,
            show_release_notes_text=get_text("show_release_notes") or "Release Notes",
            hide_release_notes_text=get_text("hide_release_notes") or "Hide release notes"
        )
        dialog.resize(900, 500)
        dialog.show()

    except Exception as e:
        logger.error(f"Erro ao exibir diálogo Sobre: {e}", exc_info=True)
        QMessageBox.critical(app, get_text("Erro") or "Erro", f"{get_text('Erro') or 'Erro'}: {e}")
