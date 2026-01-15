import os
import logging
from datetime import datetime
import sys
import traceback
import faulthandler

try:
    import ctypes

except Exception:
    ctypes = None


class LogManager:
    _instance = None
    _logger = None
    _log_file = None
    _startup_log_file = None
    _startup_fh = None

    @classmethod
    def _get_persistent_base_dir(cls) -> str:
        return os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')), 'EisenhowerOrganizer')

    @classmethod
    def _get_log_dir(cls) -> str:
        log_dir = os.path.join(cls._get_persistent_base_dir(), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        return log_dir

    @classmethod
    def get_logger(cls):
        if cls._logger is None:
            cls._configure_logging()

        return cls._logger

    @classmethod
    def get_log_file(cls):
        if cls._log_file is None:
            cls._configure_logging()

        return cls._log_file

    @classmethod
    def ensure_unicode(cls, message):
        if isinstance(message, bytes):
            return message.decode('utf-8', errors='replace')

        return str(message)

    @classmethod
    def _configure_logging(cls):
        try:
            log_dir = cls._get_log_dir()
            cls._log_file = os.path.join(log_dir, f'file_eisenhower_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                handlers=[
                    logging.FileHandler(cls._log_file, encoding='utf-8'),
                    logging.StreamHandler()
                ]
            )

            cls._logger = logging.getLogger('FileEisenhower')

            try:
                logging.getLogger('comtypes').setLevel(logging.CRITICAL)
                logging.getLogger('comtypes._comobject').setLevel(logging.CRITICAL)
                logging.getLogger('comtypes._vtbl').setLevel(logging.CRITICAL)
                logging.getLogger('comtypes._post_coinit.unknwn').setLevel(logging.CRITICAL)

            except Exception:
                pass

            try:
                cls._cleanup_logs()

            except Exception:
                pass

        except Exception as e:
            try:
                user_data_dir = os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'EisenhowerOrganizer', 'logs')
                os.makedirs(user_data_dir, exist_ok=True)
                cls._log_file = os.path.join(user_data_dir, f'file_eisenhower_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

                logging.basicConfig(
                    level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                    handlers=[
                        logging.FileHandler(cls._log_file, encoding='utf-8'),
                        logging.StreamHandler()
                    ]
                )

                cls._logger = logging.getLogger('FileEisenhower')

                try:
                    logging.getLogger('comtypes').setLevel(logging.CRITICAL)
                    logging.getLogger('comtypes._comobject').setLevel(logging.CRITICAL)
                    logging.getLogger('comtypes._vtbl').setLevel(logging.CRITICAL)
                    logging.getLogger('comtypes._post_coinit.unknwn').setLevel(logging.CRITICAL)

                except Exception:
                    pass

                cls._logger.error(f"Erro ao configurar logging no diretório padrão: {e}")

                try:
                    cls._cleanup_logs()

                except Exception:
                    pass

            except Exception:
                logging.basicConfig(level=logging.CRITICAL)
                cls._logger = logging.getLogger('FileEisenhower')

    @classmethod
    def _startup_log_path(cls) -> str:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(cls._get_log_dir(), f"Eisenhower_startup_{ts}.log")

    @classmethod
    def _write_startup_log(cls, text: str) -> None:
        try:
            path = cls._startup_log_file or cls._startup_log_path()
            with open(path, "a", encoding="utf-8") as f:
                f.write(text)
                if not text.endswith("\n"):
                    f.write("\n")

        except Exception:
            pass

    @classmethod
    def _show_fatal_message(cls, title: str, message: str) -> None:
        try:
            if ctypes is not None:
                ctypes.windll.user32.MessageBoxW(None, message, title, 0x10)

        except Exception:
            pass

    @classmethod
    def enable_startup_diagnostics(cls):
        try:
            cls._startup_log_file = cls._startup_log_path()
            fh = open(cls._startup_log_file, "a", encoding="utf-8")
            cls._startup_fh = fh
            faulthandler.enable(file=fh, all_threads=True)
            cls._write_startup_log("Eisenhower Organizer - startup log")
            cls._write_startup_log(f"argv={sys.argv}")
            cls._write_startup_log(f"executable={sys.executable}")

            try:
                cls._write_startup_log(f"cwd={os.getcwd()}")

            except Exception:
                pass

            cls._write_startup_log(f"sys.path[0:5]={sys.path[0:5]}")

            try:
                qt_debug = os.environ.get("EISENHOWER_QT_DEBUG", "").lower()
                if qt_debug in ("1", "true", "yes"):
                    os.environ["QT_DEBUG_PLUGINS"] = "1"
                    cls._write_startup_log("QT_DEBUG_PLUGINS enabled via EISENHOWER_QT_DEBUG")
                    try:
                        sys.stdout.flush()

                    except Exception:
                        pass

                    try:
                        sys.stderr.flush()

                    except Exception:
                        pass

                    sys.stdout = fh
                    sys.stderr = fh

            except Exception:
                pass

        except Exception as e:
            try:
                cls._write_startup_log(f"Falha ao ativar diagnostic startup: {e}")

            except Exception:
                pass

    @classmethod
    def install_exception_hook(cls):
        def _hook(exc_type, exc_value, exc_tb):
            try:
                tb_text = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
                cls._write_startup_log("\n=== FATAL ERROR ===")
                cls._write_startup_log(repr(exc_value))
                cls._write_startup_log(tb_text)

                try:
                    cls.get_logger().critical("Unhandled exception during startup", exc_info=(exc_type, exc_value, exc_tb))

                except Exception:
                    pass

                cls._show_fatal_message(
                    "Eisenhower - falha ao iniciar",
                    "O Eisenhower Organizer não conseguiu inicializar.\n\n"
                    f"Um log foi salvo em:\n{cls._startup_log_file}\n\n"
                    "Envie esse arquivo para diagnóstico.",
                )

            except Exception:
                pass

            sys.__excepthook__(exc_type, exc_value, exc_tb)

        sys.excepthook = _hook

    @classmethod
    def close_startup_diagnostics(cls):
        try:
            if cls._startup_fh is not None:
                try:
                    cls._startup_fh.flush()

                except Exception:
                    pass

                try:
                    cls._startup_fh.close()

                except Exception:
                    pass

                cls._startup_fh = None

        except Exception:
            pass

    @classmethod
    def debug(cls, message):
        cls.get_logger().debug(cls.ensure_unicode(message))

    @classmethod
    def info(cls, message):
        cls.get_logger().info(cls.ensure_unicode(message))

    @classmethod
    def warning(cls, message):
        cls.get_logger().warning(cls.ensure_unicode(message))

    @classmethod
    def error(cls, message, exc_info=False):
        cls.get_logger().error(cls.ensure_unicode(message), exc_info=exc_info)

    @classmethod
    def critical(cls, message, exc_info=True):
        cls.get_logger().critical(cls.ensure_unicode(message), exc_info=exc_info)

    @classmethod
    def _cleanup_logs(cls) -> None:
        try:
            log_dir = cls._get_log_dir()
            all_files = []
            for name in os.listdir(log_dir):
                if not name.endswith(".log"):
                    continue

                if name.startswith("file_eisenhower_") or name.startswith("Eisenhower_startup_"):
                    all_files.append(os.path.join(log_dir, name))

            file_logs = [p for p in all_files if os.path.basename(p).startswith("file_eisenhower_")]
            startup_logs = [p for p in all_files if os.path.basename(p).startswith("Eisenhower_startup_")]

            if len(file_logs) + len(startup_logs) < 10:
                return

            all_files_sorted = sorted(all_files, key=lambda p: os.path.getmtime(p))

            active_paths = set()
            if cls._log_file:
                active_paths.add(os.path.abspath(cls._log_file))

            if cls._startup_log_file:
                active_paths.add(os.path.abspath(cls._startup_log_file))

            removed = 0
            for path in all_files_sorted:
                if removed >= 2:
                    break

                try:
                    if os.path.abspath(path) in active_paths:
                        continue

                    os.remove(path)
                    removed += 1

                    try:
                        if cls._logger:
                            cls._logger.info(f"Removed old log file: {path}")

                    except Exception:
                        pass

                except Exception as e:
                    try:
                        if cls._logger:
                            cls._logger.warning(f"Failed to remove log file {path}: {e}")

                    except Exception:
                        pass

        except Exception:
            try:
                if cls._logger:
                    cls._logger.debug("Erro ao executar limpeza de logs")

            except Exception:
                pass
