from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QCoreApplication, QDate, QLocale
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QComboBox, QDateEdit, QCheckBox
from utils.IconUtils import get_icon_path

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)

def init_ui(app):
    app.main_layout = QVBoxLayout()
    input_layout = QHBoxLayout()

    app.task_input = QLineEdit(app)
    app.task_input.setPlaceholderText(get_text("Adicione uma tarefa..."))
    input_layout.addWidget(app.task_input)

    app.date_checkbox = QCheckBox(get_text("Vincular data"))
    app.date_checkbox.setChecked(True)
    input_layout.addWidget(app.date_checkbox)

    app.date_input = QDateEdit(app)
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

        except Exception:
            locale = QLocale.system()

        app.date_input.setLocale(locale)
        try:
            fmt = locale.dateFormat(QLocale.ShortFormat)

        except Exception:
            fmt = "dd/MM/yyyy"

        try:
            import re
            fmt = re.sub(r'(?<!y)yy(?!y)', 'yyyy', fmt)

        except Exception:
            pass

        app.date_input.setDisplayFormat(fmt)

    _apply_locale_to_date_input()

    if hasattr(app, "gerenciador_traducao"):
        try:
            app.gerenciador_traducao.idioma_alterado.connect(lambda _: _apply_locale_to_date_input())

        except Exception:
            pass

    input_layout.addWidget(app.date_input)

    app.quadrant_selector = QComboBox(app)
    app.quadrant_selector.addItems([
        get_text("Importante e Urgente"),
        get_text("Importante, mas Não Urgente"),
        get_text("Não Importante, mas Urgente"),
        get_text("Não Importante e Não Urgente")
    ])
    input_layout.addWidget(app.quadrant_selector)

    app.add_button = QPushButton(get_text("Adicionar Tarefa"))
    add_icon_path = get_icon_path("organizador.png")
    if add_icon_path:
        app.add_button.setIcon(QIcon(add_icon_path))

    app.add_button.clicked.connect(app.add_task)
    input_layout.addWidget(app.add_button)

    app.calendar_button = QPushButton(get_text("Calendário"))
    add_icon_path = get_icon_path("calendar.png")
    if add_icon_path:
        app.calendar_button.setIcon(QIcon(add_icon_path))

    app.calendar_button.clicked.connect(app.open_calendar)
    input_layout.addWidget(app.calendar_button)

    app.main_layout.addLayout(input_layout)

    quadrant_layout = QHBoxLayout()

    app.quadrant1_layout = QVBoxLayout()
    app.quadrant1_label = QLabel(get_text("Importante e Urgente"))
    app.quadrant1_list = QListWidget()
    app.add_placeholder(app.quadrant1_list, get_text("1º Quadrante"))
    app.quadrant1_completed_label = QLabel(get_text("Concluídas"))
    app.quadrant1_completed_list = QListWidget()
    app.add_placeholder(app.quadrant1_completed_list, get_text("Nenhuma Tarefa Concluída"))
    app.quadrant1_layout.addWidget(app.quadrant1_label)
    app.quadrant1_layout.addWidget(app.quadrant1_list)
    app.quadrant1_layout.addWidget(app.quadrant1_completed_label)
    app.quadrant1_layout.addWidget(app.quadrant1_completed_list)

    app.quadrant2_layout = QVBoxLayout()
    app.quadrant2_label = QLabel(get_text("Importante, mas Não Urgente"))
    app.quadrant2_list = QListWidget()
    app.add_placeholder(app.quadrant2_list, get_text("2º Quadrante"))
    app.quadrant2_completed_label = QLabel(get_text("Concluídas"))
    app.quadrant2_completed_list = QListWidget()
    app.add_placeholder(app.quadrant2_completed_list, get_text("Nenhuma Tarefa Concluída"))
    app.quadrant2_layout.addWidget(app.quadrant2_label)
    app.quadrant2_layout.addWidget(app.quadrant2_list)
    app.quadrant2_layout.addWidget(app.quadrant2_completed_label)
    app.quadrant2_layout.addWidget(app.quadrant2_completed_list)

    app.quadrant3_layout = QVBoxLayout()
    app.quadrant3_label = QLabel(get_text("Não Importante, mas Urgente"))
    app.quadrant3_list = QListWidget()
    app.add_placeholder(app.quadrant3_list, get_text("3º Quadrante"))
    app.quadrant3_completed_label = QLabel(get_text("Concluídas"))
    app.quadrant3_completed_list = QListWidget()
    app.add_placeholder(app.quadrant3_completed_list, get_text("Nenhuma Tarefa Concluída"))
    app.quadrant3_layout.addWidget(app.quadrant3_label)
    app.quadrant3_layout.addWidget(app.quadrant3_list)
    app.quadrant3_layout.addWidget(app.quadrant3_completed_label)
    app.quadrant3_layout.addWidget(app.quadrant3_completed_list)

    app.quadrant4_layout = QVBoxLayout()
    app.quadrant4_label = QLabel(get_text("Não Importante e Não Urgente"))
    app.quadrant4_list = QListWidget()
    app.add_placeholder(app.quadrant4_list, get_text("4º Quadrante"))
    app.quadrant4_completed_label = QLabel(get_text("Concluídas"))
    app.quadrant4_completed_list = QListWidget()
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
