from PySide6.QtCore import Qt, QCoreApplication, QDate, QLocale
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QDateEdit, QCheckBox, QTimeEdit
from PySide6.QtWidgets import QListWidgetItem
from source.utils.LogManager import LogManager

logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)

def _get_locale_from_app(app) -> QLocale:
    try:
        idioma = None
        if hasattr(app, "gerenciador_traducao"):
            idioma = app.gerenciador_traducao.obter_idioma_atual()

        if idioma and idioma.startswith("pt"):
            return QLocale(QLocale.Portuguese, QLocale.Brazil)

        if idioma and idioma.startswith("en"):
            return QLocale(QLocale.English, QLocale.UnitedStates)

    except Exception as e:
        logger.error(f"Erro ao obter locale do app: {e}", exc_info=True)

    return QLocale.system()

def _placeholder_text_for_list(app, lst) -> str:
    mapping = {
        app.quadrant1_list: get_text("1º Quadrante"),
        app.quadrant2_list: get_text("2º Quadrante"),
        app.quadrant3_list: get_text("3º Quadrante"),
        app.quadrant4_list: get_text("4º Quadrante"),
        app.quadrant1_completed_list: get_text("Nenhuma Tarefa Concluída"),
        app.quadrant2_completed_list: get_text("Nenhuma Tarefa Concluída"),
        app.quadrant3_completed_list: get_text("Nenhuma Tarefa Concluída"),
        app.quadrant4_completed_list: get_text("Nenhuma Tarefa Concluída"),
    }
    return mapping.get(lst, get_text("Nenhuma Tarefa Concluída"))

def _has_selectable_items(lst) -> bool:
    for i in range(lst.count()):
        it = lst.item(i)
        if it and (it.flags() & Qt.ItemIsSelectable):
            return True

    return False

def _build_display_and_tooltip(app, text: str, date_iso: str | None, time_str: str | None):
    display_text = (text or "").strip()
    tooltip_lines = []

    if date_iso:
        qd = QDate.fromString(date_iso, Qt.ISODate)
        if qd.isValid():
            date_human = qd.toString(app.date_input.displayFormat())
            if time_str:
                display_text = f"{display_text} — {date_human} {time_str}"

            else:
                display_text = f"{display_text} — {date_human}"

            tooltip_lines.append(f"{get_text('Data') or 'Data'}: {date_human}")

    if time_str:
        tooltip_lines.append(f"{get_text('Horário') or 'Horário'}: {time_str}")

    return display_text, ("\n".join(tooltip_lines) if tooltip_lines else "")


class EditDateTimeDialog(QDialog):
    def __init__(self, app, current_date_iso: str | None, current_time_str: str | None, parent=None):
        super().__init__(parent or app)
        self.app = app
        self.setModal(True)
        self.setWindowTitle(get_text("Redefinir data da tarefa") or "Redefinir data da tarefa")

        self._lang_slot = None

        layout = QVBoxLayout(self)

        row_date = QHBoxLayout()
        self.date_enabled = QCheckBox(get_text("Vincular data") or "Vincular data")
        self.date_enabled.setChecked(bool(current_date_iso))
        row_date.addWidget(self.date_enabled)
        row_date.addStretch(1)
        layout.addLayout(row_date)

        self.date_edit = QDateEdit(self)
        self.date_edit.setCalendarPopup(True)
        if current_date_iso:
            qd = QDate.fromString(current_date_iso, Qt.ISODate)
            self.date_edit.setDate(qd if qd.isValid() else QDate.currentDate())

        else:
            self.date_edit.setDate(QDate.currentDate())

        try:
            self.date_edit.setDisplayFormat(app.date_input.displayFormat())

        except Exception:
            pass

        self._apply_locale_to_calendar_popup()

        try:
            if hasattr(self.app, "gerenciador_traducao"):
                self._lang_slot = lambda *_: self._apply_locale_to_calendar_popup()
                self.app.gerenciador_traducao.idioma_alterado.connect(self._lang_slot)

        except Exception as e:
            logger.error(f"Erro ao conectar idioma_alterado no EditDateTimeDialog: {e}", exc_info=True)

        layout.addWidget(self.date_edit)

        row_time = QHBoxLayout()
        self.time_enabled = QCheckBox(get_text("Vincular horário") or "Vincular horário")
        self.time_enabled.setChecked(bool(current_time_str) and bool(current_date_iso))
        row_time.addWidget(self.time_enabled)
        row_time.addStretch(1)
        layout.addLayout(row_time)

        self.time_edit = QTimeEdit(self)
        self.time_edit.setDisplayFormat("HH:mm")
        if current_time_str:
            try:
                from PySide6.QtCore import QTime
                qt = QTime.fromString(current_time_str, "HH:mm")
                if qt.isValid():
                    self.time_edit.setTime(qt)

            except Exception:
                pass

        layout.addWidget(self.time_edit)

        def _sync_enabled():
            date_on = self.date_enabled.isChecked()
            self.date_edit.setEnabled(date_on)
            self.time_enabled.setEnabled(date_on)
            self.time_edit.setEnabled(date_on and self.time_enabled.isChecked())
            if not date_on:
                self.time_enabled.setChecked(False)

        self.date_enabled.toggled.connect(lambda _: _sync_enabled())
        self.time_enabled.toggled.connect(lambda _: _sync_enabled())
        _sync_enabled()

        buttons = QHBoxLayout()
        buttons.addStretch(1)
        btn_cancel = QPushButton(get_text("Cancelar") or "Cancelar")
        btn_ok = QPushButton(get_text("OK") or "OK")
        btn_cancel.clicked.connect(self.reject)
        btn_ok.clicked.connect(self.accept)
        buttons.addWidget(btn_cancel)
        buttons.addWidget(btn_ok)
        layout.addLayout(buttons)

    def _apply_locale_to_calendar_popup(self):
        try:
            locale = _get_locale_from_app(self.app)
            self.date_edit.setLocale(locale)

            cal = self.date_edit.calendarWidget()
            if cal is not None:
                cal.setLocale(locale)
                cal.setFirstDayOfWeek(Qt.Sunday)

        except Exception as e:
            logger.error(f"Erro ao aplicar locale no calendário popup: {e}", exc_info=True)

    def closeEvent(self, event):
        try:
            if self._lang_slot and hasattr(self.app, "gerenciador_traducao"):
                try:
                    self.app.gerenciador_traducao.idioma_alterado.disconnect(self._lang_slot)

                except (RuntimeError, TypeError):
                    pass

        except Exception as e:
            logger.error(f"Erro ao desconectar idioma_alterado no EditDateTimeDialog: {e}", exc_info=True)

        super().closeEvent(event)

    def get_values(self):
        if not self.date_enabled.isChecked():
            return None, None

        date_iso = self.date_edit.date().toString(Qt.ISODate)
        time_str = None
        if self.time_enabled.isChecked():
            time_str = self.time_edit.time().toString("HH:mm")

        return date_iso, time_str

def edit_task_datetime(app, item, list_widget):
    try:
        if not (item.flags() & Qt.ItemIsSelectable):
            return

        data = item.data(Qt.UserRole) or {}
        text = data.get("text", item.text())
        current_date_iso = data.get("date")
        current_time_str = data.get("time")

        dlg = EditDateTimeDialog(app, current_date_iso, current_time_str, parent=app)
        if dlg.exec() != QDialog.Accepted:
            return

        new_date_iso, new_time_str = dlg.get_values()

        display_text, tooltip = _build_display_and_tooltip(app, text, new_date_iso, new_time_str)

        new_item = QListWidgetItem(display_text)
        new_item.setFlags(new_item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        new_item.setCheckState(item.checkState())

        new_item.setData(Qt.UserRole, {"text": text, "date": new_date_iso, "time": new_time_str})
        if tooltip:
            new_item.setToolTip(tooltip)

        else:
            new_item.setToolTip("")

        list_widget.blockSignals(True)
        try:
            list_widget.takeItem(list_widget.row(item))

            if hasattr(app, "cleanup_time_groups"):
                app.cleanup_time_groups(list_widget)

            if not _has_selectable_items(list_widget):
                list_widget.clear()
                app.add_placeholder(list_widget, _placeholder_text_for_list(app, list_widget))

            if list_widget.count() == 1 and not (list_widget.item(0).flags() & Qt.ItemIsSelectable):
                list_widget.clear()

            if hasattr(app, "insert_task_into_quadrant_list"):
                app.insert_task_into_quadrant_list(list_widget, new_item)

            else:
                list_widget.addItem(new_item)

        finally:
            list_widget.blockSignals(False)

        app.save_tasks()
        if hasattr(app, "calendar_pane") and app.calendar_pane:
            app.calendar_pane.calendar_panel.update_task_list()

    except Exception as e:
        logger.error(f"Erro ao editar data/horário da tarefa: {e}", exc_info=True)

def move_task_to_quadrant(app, item, source_list, target_list):
    try:
        if not (item.flags() & Qt.ItemIsSelectable):
            return

        if source_list is target_list:
            return

        source_list.blockSignals(True)
        target_list.blockSignals(True)
        try:
            app.move_item_between_lists(item, source_list, target_list, Qt.Unchecked)

        finally:
            source_list.blockSignals(False)
            target_list.blockSignals(False)

        app.save_tasks()
        if hasattr(app, "calendar_pane") and app.calendar_pane:
            app.calendar_pane.calendar_panel.update_task_list()

    except Exception as e:
        logger.error(f"Erro ao mover tarefa de quadrante via menu: {e}", exc_info=True)
