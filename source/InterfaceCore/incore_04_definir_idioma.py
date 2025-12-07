from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def definir_idioma(app, codigo_idioma):
    try:
        app.gerenciador_traducao.definir_idioma(codigo_idioma)
        for acao in app.idioma_menu.actions():
            acao.setChecked(acao.text() == app.gerenciador_traducao.idiomas_disponiveis[codigo_idioma])

    except Exception as e:
        logger.error(f"Erro ao definir idioma: {e}", exc_info=True)
