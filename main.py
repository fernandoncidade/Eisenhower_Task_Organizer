import sys
from source.utils.LogManager import LogManager
# from source.utils.TrialManager import TrialManager

LogManager.enable_startup_diagnostics()
LogManager.install_exception_hook()
logger = LogManager.get_logger()

if __name__ == "__main__":
    try:
        from PySide6.QtWidgets import QApplication
        from source.eisenhower_app import EisenhowerMatrixApp
        from source.language.tr_01_gerenciadorTraducao import GerenciadorTraducao

        app = QApplication(sys.argv)
        gerenciador_traducao = GerenciadorTraducao()
        gerenciador_traducao.aplicar_traducao()

        # TrialManager.enforce_trial()  # Descomente esta linha para forçar o uso da versão de avaliação
        # TrialManager.delete_first_run_timestamp()  # Use esta linha para testes, removendo o timestamp de primeiro uso

        window = EisenhowerMatrixApp()
        window.show()
        exit_code = app.exec()
        logger.debug(f"Aplicação encerrada com código de saída: {exit_code}")
        sys.exit(exit_code)

    except Exception as e:
        logger.critical(f"Erro fatal ao iniciar aplicação: {e}", exc_info=True)
        LogManager.close_startup_diagnostics()
        sys.exit(1)
