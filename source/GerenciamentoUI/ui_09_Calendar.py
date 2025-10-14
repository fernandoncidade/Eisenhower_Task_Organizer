from PySide6.QtWidgets import (QDialog, QVBoxLayout, QCalendarWidget, QComboBox, QListWidget, QListWidgetItem, QLabel, QHBoxLayout, QAbstractItemView, QWidget)
from PySide6.QtCore import Qt, QDate, QCoreApplication, QLocale, QSize
from PySide6.QtGui import QPainter, QFontMetrics, QTextCharFormat, QBrush, QColor, QFont
from PySide6.QtWidgets import QSizePolicy

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)


class CalendarDialog(QDialog):
    def __init__(self, app):
        super().__init__(app)
        self.app = app
        self.setModal(True)
        self.setWindowTitle(get_text("Calendário de Tarefas"))
        self._date_format = app.date_input.displayFormat() if hasattr(app, "date_input") else "dd/MM/yyyy"
        self._highlighted_dates = set() 

        main_layout = QVBoxLayout(self)

        self.calendar = QCalendarWidget(self)
        initial_date = app.date_input.date() if hasattr(app, "date_input") else QDate.currentDate()
        self.calendar.setSelectedDate(initial_date)

        hint = self.calendar.minimumSizeHint()
        fallback = QSize(300, 260)
        self.calendar.setMinimumSize(hint.expandedTo(fallback))
        self.calendar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        self._apply_locale_to_calendar()

        main_layout.addWidget(self.calendar)

        controls_layout = QHBoxLayout()
        self.filter_label = QLabel(get_text("Exibir por"), self)
        controls_layout.addWidget(self.filter_label)

        self.filter_combo = QComboBox(self)
        self.filter_combo.addItem(get_text("Dia"), "day")
        self.filter_combo.addItem(get_text("Semana"), "week")
        self.filter_combo.addItem(get_text("Mês"), "month")
        controls_layout.addWidget(self.filter_combo)
        controls_layout.addStretch()
        main_layout.addLayout(controls_layout)

        self.tasks_list = QListWidget(self)
        self.tasks_list.setSelectionMode(QAbstractItemView.NoSelection)
        self.tasks_list.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        main_layout.addWidget(self.tasks_list, 1)

        self.calendar.selectionChanged.connect(self.update_task_list)
        self.filter_combo.currentIndexChanged.connect(self.update_task_list)

        if hasattr(self.app, "gerenciador_traducao"):
            self.app.gerenciador_traducao.idioma_alterado.connect(self._on_language_changed)

        self.update_task_list()

    def closeEvent(self, event):
        if hasattr(self.app, "gerenciador_traducao"):
            try:
                self.app.gerenciador_traducao.idioma_alterado.disconnect(self._on_language_changed)

            except (RuntimeError, TypeError):
                pass

        super().closeEvent(event)

    def _collect_tasks(self):
        tasks = []
        mapping = [
            (self.app.quadrant1_list, self.app.quadrant1_label.text(), False),
            (self.app.quadrant1_completed_list, f"{self.app.quadrant1_label.text()} - {self.app.quadrant1_completed_label.text()}", True),
            (self.app.quadrant2_list, self.app.quadrant2_label.text(), False),
            (self.app.quadrant2_completed_list, f"{self.app.quadrant2_label.text()} - {self.app.quadrant2_completed_label.text()}", True),
            (self.app.quadrant3_list, self.app.quadrant3_label.text(), False),
            (self.app.quadrant3_completed_list, f"{self.app.quadrant3_label.text()} - {self.app.quadrant3_completed_label.text()}", True),
            (self.app.quadrant4_list, self.app.quadrant4_label.text(), False),
            (self.app.quadrant4_completed_list, f"{self.app.quadrant4_label.text()} - {self.app.quadrant4_completed_label.text()}", True),
        ]
        for lst, category, completed in mapping:
            for i in range(lst.count()):
                item = lst.item(i)
                if not item or not (item.flags() & Qt.ItemIsSelectable):
                    continue

                data = item.data(Qt.UserRole) or {}
                text = data.get("text", item.text())
                date_str = data.get("date")
                tasks.append({
                    "text": text,
                    "date": date_str,
                    "category": category,
                    "completed": completed
                })

        return tasks

    def update_task_list(self):
        self.tasks_list.clear()
        self._apply_highlighted_dates()
        selected_date = self.calendar.selectedDate()
        filter_mode = self.filter_combo.currentData()
        filtered = []

        for task in self._collect_tasks():
            date_str = task.get("date")
            if not date_str:
                continue

            qdate = QDate.fromString(date_str, Qt.ISODate)
            if not qdate.isValid():
                continue

            if filter_mode == "day" and qdate != selected_date:
                continue

            if filter_mode == "week":
                selected_week = selected_date.weekNumber()
                task_week = qdate.weekNumber()
                if task_week[0] != selected_week[0] or qdate.year() != selected_date.year():
                    continue

            if filter_mode == "month":
                if qdate.month() != selected_date.month() or qdate.year() != selected_date.year():
                    continue

            filtered.append((qdate, task))

        if not filtered:
            placeholder = QListWidgetItem(get_text("Nenhuma tarefa para o período selecionado."))
            placeholder.setFlags((placeholder.flags() & ~Qt.ItemIsSelectable) & ~Qt.ItemIsEnabled)
            self.tasks_list.addItem(placeholder)
            return

        filtered.sort(key=lambda entry: (entry[0], entry[1]["text"].lower()))
        for qdate, task in filtered:
            status_text = get_text("Concluída") if task.get("completed") else get_text("Pendente")
            date_str = qdate.toString(self._date_format)
            item_text = f"{date_str} — {task['text']} — [{status_text}]"
            item = QListWidgetItem(item_text)
            item.setFlags((item.flags() & ~Qt.ItemIsSelectable) & ~Qt.ItemIsEnabled)
            self.tasks_list.addItem(item)

    def _on_language_changed(self):
        self.setWindowTitle(get_text("Calendário de Tarefas"))
        self.filter_label.setText(get_text("Exibir por"))
        self.filter_combo.setItemText(0, get_text("Dia"))
        self.filter_combo.setItemText(1, get_text("Semana"))
        self.filter_combo.setItemText(2, get_text("Mês"))
        self._date_format = self.app.date_input.displayFormat() if hasattr(self.app, "date_input") else self._date_format

        self._apply_locale_to_calendar()
        self.update_task_list()

    def _apply_locale_to_calendar(self):
        try:
            idioma = None
            if hasattr(self.app, "gerenciador_traducao"):
                idioma = self.app.gerenciador_traducao.obter_idioma_atual()

            if idioma and idioma.startswith("pt"):
                locale = QLocale(QLocale.Portuguese, QLocale.Brazil)

            elif idioma and idioma.startswith("en"):
                locale = QLocale(QLocale.English, QLocale.UnitedStates)

            else:
                locale = QLocale.system()

            self.calendar.setLocale(locale)
            try:
                self.calendar.setFirstDayOfWeek(locale.firstDayOfWeek())

            except Exception:
                pass

        except Exception:
            pass

    def _get_task_dates(self):
        dates = set()
        try:
            for task in self._collect_tasks():
                ds = task.get("date")
                if not ds:
                    continue

                qd = QDate.fromString(ds, Qt.ISODate)
                if qd.isValid():
                    dates.add(qd.toString(Qt.ISODate))

        except Exception:
            pass

        return dates

    def _apply_highlighted_dates(self):
        try:
            new_dates = self._get_task_dates()
            if not hasattr(self, "_highlighted_dates"):
                self._highlighted_dates = set()

            to_clear = self._highlighted_dates - new_dates
            if to_clear:
                blank = QTextCharFormat()
                for ds in to_clear:
                    qd = QDate.fromString(ds, Qt.ISODate)
                    if qd.isValid():
                        self.calendar.setDateTextFormat(qd, blank)

            fmt = QTextCharFormat()
            pal = self.palette()
            base = pal.highlight().color()
            color = QColor(base.red(), base.green(), base.blue(), 60)
            fmt.setBackground(QBrush(color))
            fmt.setFontWeight(QFont.Bold)

            for ds in new_dates:
                qd = QDate.fromString(ds, Qt.ISODate)
                if qd.isValid():
                    self.calendar.setDateTextFormat(qd, fmt)

            self._highlighted_dates = new_dates

        except Exception:
            pass


class RotatedTabButton(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self._text = text
        self.setMinimumWidth(25)
        self._recompute_size()

    def setText(self, text):
        self._text = text
        self._recompute_size()
        self.update()

    def text(self):
        return self._text

    def _recompute_size(self):
        fm = QFontMetrics(self.font())
        text_w = fm.horizontalAdvance(self._text)
        text_h = fm.height()
        width = text_h + 5
        height = text_w + 20
        self.setFixedSize(QSize(width, height))

    def mousePressEvent(self, event):
        self.parent().toggle_panel()
        super().mousePressEvent(event)

    def paintEvent(self, event):
        try:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.save()
            painter.fillRect(self.rect(), self.palette().button().color())
            painter.setPen(self.palette().dark().color())
            painter.drawRect(0, 0, self.width()-1, self.height()-1)
            painter.translate(0, self.height())
            painter.rotate(270)
            fm = painter.fontMetrics()
            text_w = fm.horizontalAdvance(self._text)
            x = (self.height() - text_w) / 2
            y = (self.width() + fm.ascent() - fm.descent()) / 2
            painter.setPen(self.palette().buttonText().color())
            painter.drawText(x, y, self._text)
            painter.restore()

        except Exception:
            pass


class CalendarPanel(QWidget):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self._date_format = app.date_input.displayFormat() if hasattr(app, "date_input") else "dd/MM/yyyy"
        self._highlighted_dates = set()  # manter estado local de destaques

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 1, 5, 9)
        main_layout.setSpacing(6)

        self.calendar = QCalendarWidget(self)
        initial_date = app.date_input.date() if hasattr(app, "date_input") else QDate.currentDate()
        self.calendar.setSelectedDate(initial_date)
        hint = self.calendar.minimumSizeHint()
        fallback = QSize(300, 260)
        self.calendar.setMinimumSize(hint.expandedTo(fallback))
        self.calendar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self._apply_locale_to_calendar()
        main_layout.addWidget(self.calendar)

        controls_layout = QHBoxLayout()
        self.filter_label = QLabel(get_text("Exibir por"), self)
        controls_layout.addWidget(self.filter_label)

        self.filter_combo = QComboBox(self)
        self.filter_combo.addItem(get_text("Dia"), "day")
        self.filter_combo.addItem(get_text("Semana"), "week")
        self.filter_combo.addItem(get_text("Mês"), "month")
        controls_layout.addWidget(self.filter_combo)
        controls_layout.addStretch()
        main_layout.addLayout(controls_layout)

        self.tasks_list = QListWidget(self)
        self.tasks_list.setSelectionMode(QAbstractItemView.NoSelection)
        self.tasks_list.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        main_layout.addWidget(self.tasks_list, 1)

        self.calendar.selectionChanged.connect(self.update_task_list)
        self.filter_combo.currentIndexChanged.connect(self.update_task_list)

        if hasattr(self.app, "gerenciador_traducao"):
            self.app.gerenciador_traducao.idioma_alterado.connect(self._on_language_changed)

        self.update_task_list()

    def _collect_tasks(self):
        return CalendarDialog._collect_tasks(self)

    def update_task_list(self):
        return CalendarDialog.update_task_list(self)

    def _get_task_dates(self):
        return CalendarDialog._get_task_dates(self)

    def _apply_highlighted_dates(self):
        return CalendarDialog._apply_highlighted_dates(self)

    def _on_language_changed(self):
        self.filter_label.setText(get_text("Exibir por"))
        self.filter_combo.setItemText(0, get_text("Dia"))
        self.filter_combo.setItemText(1, get_text("Semana"))
        self.filter_combo.setItemText(2, get_text("Mês"))
        self._date_format = self.app.date_input.displayFormat() if hasattr(self.app, "date_input") else self._date_format
        self._apply_locale_to_calendar()
        self.update_task_list()

    def _apply_locale_to_calendar(self):
        return CalendarDialog._apply_locale_to_calendar(self)


class Calendar(QWidget):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self._expanded = False
        self._panel_width = 360

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 11, 0, 0)
        layout.setSpacing(0)

        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.toggle_button = RotatedTabButton(get_text("Mostrar Calendário"), self)
        self.toggle_button.setMinimumWidth(25)
        layout.addWidget(self.toggle_button, 0, Qt.AlignLeft | Qt.AlignTop)

        self.calendar_panel = CalendarPanel(app, self)
        self.calendar_panel.setFixedWidth(self._panel_width)
        self.calendar_panel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout.addWidget(self.calendar_panel, 1)

        self.calendar_panel.setVisible(False)
        self._apply_fixed_width()

        if hasattr(self.app, "gerenciador_traducao"):
            self.app.gerenciador_traducao.idioma_alterado.connect(self.on_language_changed)

    def _apply_fixed_width(self):
        btn_w = self.toggle_button.width()
        total = btn_w + (self._panel_width if self._expanded else 0)
        self.setFixedWidth(total)

    def toggle_panel(self, open_if_hidden=False):
        previous = self._expanded
        if open_if_hidden and not self._expanded:
            self._expanded = True

        else:
            self._expanded = not self._expanded

        self.calendar_panel.setVisible(self._expanded)

        if self._expanded:
            hint_w = max(self.calendar_panel.sizeHint().width(), 300)
            self._panel_width = max(self._panel_width, hint_w)
            self.calendar_panel.setFixedWidth(self._panel_width)
            self.toggle_button.setText(get_text("Recolher Calendário"))

        else:
            self.toggle_button.setText(get_text("Mostrar Calendário"))

        self._apply_fixed_width()

        try:
            main_win = getattr(self, "app", None)
            if not main_win:
                return

            if main_win.isMaximized():
                try:
                    central = main_win.centralWidget()
                    if central:
                        central.updateGeometry()

                except Exception:
                    pass

                main_win.update()
                return

            avail_w = None
            try:
                wh = main_win.windowHandle()
                if wh and wh.screen():
                    avail_w = wh.screen().availableGeometry().width()

            except Exception:
                avail_w = None

            if avail_w is None:
                try:
                    avail_w = main_win.screen().availableGeometry().width()

                except Exception:
                    avail_w = 99999

            if self._expanded and not previous:
                desired = main_win.width() + self._panel_width
                new_w = min(desired, avail_w)
                main_win.resize(new_w, main_win.height())

            elif (not self._expanded) and previous:
                new_w = max(400, main_win.width() - self._panel_width)
                main_win.resize(new_w, main_win.height())

        except Exception:
            pass

    def on_language_changed(self):
        self.toggle_button.setText(get_text("Recolher Calendário") if self._expanded else get_text("Mostrar Calendário"))
        try:
            self.calendar_panel._on_language_changed()

        except Exception:
            pass
