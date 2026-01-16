from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import QCoreApplication, Qt, QDate
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel
from PySide6.QtGui import QFont
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)

def show_context_menu(app, point, list_widget):
    try:
        item = list_widget.itemAt(point)
        if not item:
            return

        if not bool(item.flags() & Qt.ItemIsSelectable):
            return

        menu = QMenu(list_widget)

        try:
            def _edit_description():
                try:
                    class DescriptionDialog(QDialog):
                        def __init__(self, parent=None, initial_text=""):
                            super().__init__(parent or app)
                            self.setModal(True)
                            self.setWindowTitle(get_text("Descrição da Tarefa") or "Descrição da Tarefa")
                            layout = QVBoxLayout(self)
                            layout.addWidget(QLabel(get_text("Adicione uma descrição para a tarefa:")))
                            self.text = QTextEdit(self)
                            self.text.setPlainText(initial_text or "")
                            self.text.setMinimumSize(400, 150)
                            layout.addWidget(self.text)
                            btns = QHBoxLayout()
                            btns.addStretch(1)
                            btn_cancel = QPushButton(get_text("Cancelar") or "Cancelar")
                            btn_ok = QPushButton(get_text("OK") or "OK")
                            btn_cancel.clicked.connect(self.reject)
                            btn_ok.clicked.connect(self.accept)
                            btns.addWidget(btn_cancel)
                            btns.addWidget(btn_ok)
                            layout.addLayout(btns)

                        def get_text(self):
                            return self.text.toPlainText()

                    current_data = item.data(Qt.UserRole) or {}
                    existing = current_data.get("description", "")
                    dlg = DescriptionDialog(parent=app, initial_text=existing)
                    if dlg.exec() == QDialog.Accepted:
                        desc = dlg.get_text().strip()
                        data = dict(current_data) if isinstance(current_data, dict) else {}
                        if desc:
                            data["description"] = desc

                        else:
                            data.pop("description", None)

                        try:
                            list_widget.blockSignals(True)

                        except Exception:
                            pass

                        try:
                            item.setData(Qt.UserRole, data)

                            tooltip_lines = []
                            try:
                                date_val = data.get("date")
                                time_val = data.get("time")
                                if date_val:
                                    qd = QDate.fromString(date_val, Qt.ISODate)
                                    if qd.isValid() and hasattr(app, "date_input"):
                                        date_human = qd.toString(app.date_input.displayFormat())
                                        tooltip_lines.append(f"{get_text('Data') or 'Data'}: {date_human}")
                                        if time_val:
                                            tooltip_lines.append(f"{get_text('Horário') or 'Horário'}: {time_val}")

                            except Exception:
                                pass

                            try:
                                fp = data.get("file_path")
                                if fp:
                                    tooltip_lines.append((get_text("Arquivo") or "Arquivo") + f": {fp}")

                            except Exception:
                                pass

                            try:
                                desc_full = data.get("description")
                                if desc_full:
                                    preview_lines = [ln for ln in desc_full.splitlines() if ln.strip()]
                                    preview = "\n".join(preview_lines[:3])
                                    if preview:
                                        tooltip_lines.append((get_text("Descrição") or "Descrição") + ":")
                                        tooltip_lines.append(preview)

                            except Exception:
                                pass

                            if tooltip_lines:
                                item.setToolTip("\n".join(tooltip_lines))

                        finally:
                            try:
                                list_widget.blockSignals(False)

                            except Exception:
                                pass

                        try:
                            app.save_tasks()

                        except Exception:
                            pass

                except Exception as e:
                    logger.error(f"Erro no diálogo de descrição: {e}", exc_info=True)

            descricao_acao = QAction(get_text("Adicionar/Editar Descrição...") or "Adicionar/Editar Descrição...", app)
            descricao_acao.triggered.connect(_edit_description)
            menu.addAction(descricao_acao)

        except Exception:
            pass

        editar_data = QAction(get_text("Redefinir data...") or "Redefinir data...", app)
        editar_data.triggered.connect(lambda: app.edit_task_datetime(item, list_widget))
        menu.addAction(editar_data)

        mover_menu = menu.addMenu(get_text("Mover para") or "Mover para")

        q1 = QAction(get_text("🔴 Importante e Urgente"), app)
        q1.triggered.connect(lambda: app.move_task_to_quadrant(item, list_widget, app.quadrant1_list))
        mover_menu.addAction(q1)

        q2 = QAction(get_text("🟠 Importante, mas Não Urgente"), app)
        q2.triggered.connect(lambda: app.move_task_to_quadrant(item, list_widget, app.quadrant2_list))
        mover_menu.addAction(q2)

        q3 = QAction(get_text("🟡 Não Importante, mas Urgente"), app)
        q3.triggered.connect(lambda: app.move_task_to_quadrant(item, list_widget, app.quadrant3_list))
        mover_menu.addAction(q3)

        q4 = QAction(get_text("🟢 Não Importante e Não Urgente"), app)
        q4.triggered.connect(lambda: app.move_task_to_quadrant(item, list_widget, app.quadrant4_list))
        mover_menu.addAction(q4)

        menu.addSeparator()

        remover_acao = QAction(get_text("Remover Tarefa"), app)
        remover_acao.triggered.connect(lambda: app.remove_task(item, list_widget))
        menu.addAction(remover_acao)

        menu.exec(list_widget.mapToGlobal(point))

    except Exception as e:
        logger.error(f"Erro ao exibir menu de contexto: {e}", exc_info=True)
