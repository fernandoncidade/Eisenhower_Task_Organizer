def definir_idioma(app, codigo_idioma):
    app.gerenciador_traducao.definir_idioma(codigo_idioma)
    for acao in app.idioma_menu.actions():
        acao.setChecked(acao.text() == app.gerenciador_traducao.idiomas_disponiveis[codigo_idioma])
