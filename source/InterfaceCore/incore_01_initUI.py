from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QCoreApplication, QDate, QLocale, QTime
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit, QCheckBox, QTimeEdit, QSizePolicy
from source.utils.IconUtils import get_icon_path
from source.utils.LogManager import LogManager
from source.InterfaceCore.incore_10_task_list_widget import TaskListWidget
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)


class CustomTimeEdit(QTimeEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWrapping(True)
        self._last_time = self.time()

    def stepBy(self, steps):
        current_time = self.time()
        current_section = self.currentSection()

        if current_section == QTimeEdit.MinuteSection:
            total_minutes = current_time.hour() * 60 + current_time.minute()
            total_minutes += steps

            if total_minutes < 0:
                total_minutes = 1439

            elif total_minutes >= 1440:
                total_minutes = 0

            new_hour = total_minutes // 60
            new_minute = total_minutes % 60
            new_time = QTime(new_hour, new_minute, current_time.second())
            self.setTime(new_time)

        else:
            super().stepBy(steps)

        self._last_time = self.time()

_COMMON_CTX_TRANSLATIONS = {
    "undo": "Desfazer",
    "redo": "Refazer",
    "cut": "Recortar",
    "copy": "Copiar",
    "paste": "Colar",
    "delete": "Excluir",
    "select all": "Selecionar Tudo",
    "clear": "Limpar",
    "insert": "Inserir",
    "today": "Hoje",
    "none": "Nenhum"
}

def _normalize_action_text(text: str) -> str:
    if not text:
        return ""

    t = text.replace("&", "").strip()
    if t.endswith("..."):
        t = t[:-3].strip()

    return t.lower()

def _localize_menu(menu, app):
    try:
        idioma = None
        if hasattr(app, "gerenciador_traducao"):
            idioma = app.gerenciador_traducao.obter_idioma_atual()

        use_pt = bool(idioma and idioma.startswith("pt"))

    except Exception:
        use_pt = False

    for action in menu.actions():
        if action.menu():  # submenu
            _localize_menu(action.menu(), app)
            continue

        txt = action.text()
        key = _normalize_action_text(txt)
        if use_pt and key in _COMMON_CTX_TRANSLATIONS:
            action.setText(_COMMON_CTX_TRANSLATIONS[key])


class LocalizedDateEdit(QDateEdit):
    def contextMenuEvent(self, event):
        try:
            menu = self.createStandardContextMenu()
            _localize_menu(menu, self.window().parent() if self.window() else None or self)
            menu.exec(event.globalPos())

        except Exception:
            super().contextMenuEvent(event)


class LocalizedTimeEdit(CustomTimeEdit):
    def contextMenuEvent(self, event):
        try:
            menu = self.createStandardContextMenu()
            _localize_menu(menu, self.window().parent() if self.window() else None or self)
            menu.exec(event.globalPos())

        except Exception:
            super().contextMenuEvent(event)

def init_ui(app):
    app.main_layout = QVBoxLayout()

    input_layout_top = QHBoxLayout()

    app.task_input = QLineEdit(app)
    app.task_input.setPlaceholderText(get_text("Adicione uma tarefa..."))
    app.task_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    input_layout_top.addWidget(app.task_input, 1)

    app.add_button = QPushButton(get_text("Adicionar Tarefa"))
    add_icon_path = get_icon_path("organizador.png")
    if add_icon_path:
        app.add_button.setIcon(QIcon(add_icon_path))

    app.add_button.clicked.connect(app.add_task)
    input_layout_top.addWidget(app.add_button)

    app.calendar_button = QPushButton(get_text("Calendário"))
    add_icon_path = get_icon_path("calendar.png")
    if add_icon_path:
        app.calendar_button.setIcon(QIcon(add_icon_path))

    app.calendar_button.clicked.connect(app.open_calendar)
    input_layout_top.addWidget(app.calendar_button)

    second_row_layout = QHBoxLayout()
    second_row_layout.setAlignment(Qt.AlignLeft)

    app.date_checkbox = QCheckBox(get_text("Vincular data"))
    app.date_checkbox.setChecked(True)
    second_row_layout.addWidget(app.date_checkbox)

    app.date_input = LocalizedDateEdit(app)
    app.date_input.setCalendarPopup(True)
    app.date_input.setDate(QDate.currentDate())

    def _apply_locale_to_date_input():
        locale = QLocale.system()
        try:
            if hasattr(app, "gerenciador_traducao"):
                idioma = app.gerenciador_traducao.obter_idioma_atual()
                if idioma and idioma.startswith("pt"):
                    locale = QLocale(QLocale.Portuguese, QLocale.Brazil)

                elif idioma and idioma.startswith("en"):
                    locale = QLocale(QLocale.English, QLocale.UnitedStates)

        except Exception as e:
            logger.error(f"Erro ao aplicar locale à data: {e}", exc_info=True)
            locale = QLocale.system()

        app.date_input.setLocale(locale)
        try:
            fmt = locale.dateFormat(QLocale.ShortFormat)

        except Exception as e:
            logger.error(f"Erro ao obter formato de data: {e}", exc_info=True)
            fmt = "dd/MM/yyyy"

        try:
            import re
            fmt = re.sub(r'(?<!y)yy(?!y)', 'yyyy', fmt)

        except Exception as e:
            logger.error(f"Erro ao ajustar formato de data: {e}", exc_info=True)

        app.date_input.setDisplayFormat(fmt)

    _apply_locale_to_date_input()

    if hasattr(app, "gerenciador_traducao"):
        try:
            app.gerenciador_traducao.idioma_alterado.connect(lambda _: _apply_locale_to_date_input())

        except Exception as e:
            logger.error(f"Erro ao conectar sinal de idioma_alterado para data: {e}", exc_info=True)

    second_row_layout.addWidget(app.date_input)

    app.time_checkbox = QCheckBox(get_text("Vincular horário"))
    app.time_checkbox.setChecked(True)
    second_row_layout.addWidget(app.time_checkbox)

    app.time_input = LocalizedTimeEdit(app)
    app.time_input.setDisplayFormat("HH:mm")
    app.time_input.setEnabled(True)
    second_row_layout.addWidget(app.time_input)

    def _apply_locale_to_time_input():
        try:
            app.time_input.setDisplayFormat("HH:mm")

        except Exception as e:
            logger.error(f"Erro ao aplicar locale ao horário: {e}", exc_info=True)

    _apply_locale_to_time_input()

    if hasattr(app, "gerenciador_traducao"):
        try:
            app.gerenciador_traducao.idioma_alterado.connect(lambda _: _apply_locale_to_time_input())
            app.gerenciador_traducao.idioma_alterado.connect(lambda _: app.time_checkbox.setText(get_text("Vincular horário")))

        except Exception as e:
            logger.error(f"Erro ao conectar sinal de idioma_alterado para horário: {e}", exc_info=True)

    def _on_time_checkbox_toggled(checked: bool):
        try:
            app.time_input.setEnabled(checked and app.date_checkbox.isChecked())

        except Exception as e:
            logger.error(f"Erro ao alternar checkbox de horário: {e}", exc_info=True)

    def _on_date_checkbox_toggled(checked: bool):
        try:
            app.time_checkbox.setEnabled(checked)
            app.time_input.setEnabled(checked and app.time_checkbox.isChecked())
            if not checked:
                app.time_checkbox.setChecked(False)

        except Exception as e:
            logger.error(f"Erro ao alternar checkbox de data: {e}", exc_info=True)

    app.time_checkbox.toggled.connect(_on_time_checkbox_toggled)
    app.date_checkbox.toggled.connect(_on_date_checkbox_toggled)
    app.time_checkbox.setEnabled(app.date_checkbox.isChecked())

    app.quadrant_selector = QComboBox(app)
    app.quadrant_selector.addItems([
        get_text("🔴 Importante e Urgente"),
        get_text("🟠 Importante, mas Não Urgente"),
        get_text("🟡 Não Importante, mas Urgente"),
        get_text("🟢 Não Importante e Não Urgente")
    ])
    second_row_layout.addWidget(app.quadrant_selector)

    app.main_layout.addLayout(input_layout_top)
    app.main_layout.addLayout(second_row_layout)

    quadrant_layout = QHBoxLayout()

    app.quadrant1_layout = QVBoxLayout()
    app.quadrant1_label = QLabel(get_text("🔴 Importante e Urgente"))
    app.quadrant1_list = TaskListWidget(app, is_completed=False)
    app.add_placeholder(app.quadrant1_list, get_text("1º Quadrante"))
    app.quadrant1_completed_label = QLabel(get_text("Concluídas"))
    app.quadrant1_completed_list = TaskListWidget(app, is_completed=True)
    app.add_placeholder(app.quadrant1_completed_list, get_text("Nenhuma Tarefa Concluída"))
    app.quadrant1_layout.addWidget(app.quadrant1_label)
    app.quadrant1_layout.addWidget(app.quadrant1_list)
    app.quadrant1_layout.addWidget(app.quadrant1_completed_label)
    app.quadrant1_layout.addWidget(app.quadrant1_completed_list)

    app.quadrant2_layout = QVBoxLayout()
    app.quadrant2_label = QLabel(get_text("🟠 Importante, mas Não Urgente"))
    app.quadrant2_list = TaskListWidget(app, is_completed=False)
    app.add_placeholder(app.quadrant2_list, get_text("2º Quadrante"))
    app.quadrant2_completed_label = QLabel(get_text("Concluídas"))
    app.quadrant2_completed_list = TaskListWidget(app, is_completed=True)
    app.add_placeholder(app.quadrant2_completed_list, get_text("Nenhuma Tarefa Concluída"))
    app.quadrant2_layout.addWidget(app.quadrant2_label)
    app.quadrant2_layout.addWidget(app.quadrant2_list)
    app.quadrant2_layout.addWidget(app.quadrant2_completed_label)
    app.quadrant2_layout.addWidget(app.quadrant2_completed_list)

    app.quadrant3_layout = QVBoxLayout()
    app.quadrant3_label = QLabel(get_text("🟡 Não Importante, mas Urgente"))
    app.quadrant3_list = TaskListWidget(app, is_completed=False)
    app.add_placeholder(app.quadrant3_list, get_text("3º Quadrante"))
    app.quadrant3_completed_label = QLabel(get_text("Concluídas"))
    app.quadrant3_completed_list = TaskListWidget(app, is_completed=True)
    app.add_placeholder(app.quadrant3_completed_list, get_text("Nenhuma Tarefa Concluída"))
    app.quadrant3_layout.addWidget(app.quadrant3_label)
    app.quadrant3_layout.addWidget(app.quadrant3_list)
    app.quadrant3_layout.addWidget(app.quadrant3_completed_label)
    app.quadrant3_layout.addWidget(app.quadrant3_completed_list)

    app.quadrant4_layout = QVBoxLayout()
    app.quadrant4_label = QLabel(get_text("🟢 Não Importante e Não Urgente"))
    app.quadrant4_list = TaskListWidget(app, is_completed=False)
    app.add_placeholder(app.quadrant4_list, get_text("4º Quadrante"))
    app.quadrant4_completed_label = QLabel(get_text("Concluídas"))
    app.quadrant4_completed_list = TaskListWidget(app, is_completed=True)
    app.add_placeholder(app.quadrant4_completed_list, get_text("Nenhuma Tarefa Concluída"))
    app.quadrant4_layout.addWidget(app.quadrant4_label)
    app.quadrant4_layout.addWidget(app.quadrant4_list)
    app.quadrant4_layout.addWidget(app.quadrant4_completed_label)
    app.quadrant4_layout.addWidget(app.quadrant4_completed_list)

    quadrant_layout.addLayout(app.quadrant1_layout)
    quadrant_layout.addLayout(app.quadrant2_layout)
    quadrant_layout.addLayout(app.quadrant3_layout)
    quadrant_layout.addLayout(app.quadrant4_layout)

    app.main_layout.addLayout(quadrant_layout)

    container = QWidget()
    container.setLayout(app.main_layout)
    app.setCentralWidget(container)

    app.quadrant1_list.itemChanged.connect(lambda item: app.handle_item_checked(item, app.quadrant1_list, app.quadrant1_completed_list))
    app.quadrant2_list.itemChanged.connect(lambda item: app.handle_item_checked(item, app.quadrant2_list, app.quadrant2_completed_list))
    app.quadrant3_list.itemChanged.connect(lambda item: app.handle_item_checked(item, app.quadrant3_list, app.quadrant3_completed_list))
    app.quadrant4_list.itemChanged.connect(lambda item: app.handle_item_checked(item, app.quadrant4_list, app.quadrant4_completed_list))

    app.quadrant1_completed_list.itemChanged.connect(lambda item: app.handle_item_checked(item, app.quadrant1_completed_list, app.quadrant1_list))
    app.quadrant2_completed_list.itemChanged.connect(lambda item: app.handle_item_checked(item, app.quadrant2_completed_list, app.quadrant2_list))
    app.quadrant3_completed_list.itemChanged.connect(lambda item: app.handle_item_checked(item, app.quadrant3_completed_list, app.quadrant3_list))
    app.quadrant4_completed_list.itemChanged.connect(lambda item: app.handle_item_checked(item, app.quadrant4_completed_list, app.quadrant4_list))

    for lst in (
        app.quadrant1_list, app.quadrant2_list, app.quadrant3_list, app.quadrant4_list,
        app.quadrant1_completed_list, app.quadrant2_completed_list, app.quadrant3_completed_list, app.quadrant4_completed_list
    ):
        lst.setContextMenuPolicy(Qt.CustomContextMenu)
        lst.customContextMenuRequested.connect(lambda point, l=lst: app.show_context_menu(point, l))
