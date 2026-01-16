import json
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt, QDate, QCoreApplication
from PySide6.QtGui import QFont
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)

def load_tasks(app):
    try:
        with open(app.tasks_path, "r", encoding="utf-8") as file:
            tasks = json.load(file)
            date_format = app.date_input.displayFormat() if hasattr(app, "date_input") else "dd/MM/yyyy"

            def create_item(text, date_value, time_value, completed):
                display_text = text
                tooltip_lines = []
                if date_value:
                    qdate = QDate.fromString(date_value, Qt.ISODate)
                    if qdate.isValid():
                        date_human = qdate.toString(date_format)
                        if time_value:
                            display_text = f"{text} — {date_human} {time_value}"

                        else:
                            display_text = f"{text} — {date_human}"

                        tooltip_lines.append(f"{get_text('Data') or 'Data'}: {date_human}")

                if time_value:
                    tooltip_lines.append(f"{get_text('Horário') or 'Horário'}: {time_value}")

                item = QListWidgetItem(display_text)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                item.setCheckState(Qt.Checked if completed else Qt.Unchecked)
                data = {"text": text, "date": date_value, "time": time_value}
                item.setData(Qt.UserRole, data)
                if tooltip_lines:
                    item.setToolTip("\n".join(tooltip_lines))

                return item

            def populate_list(key, lst, completed=False):
                if key in tasks and tasks[key]:
                    lst.clear()
                    for entry in tasks[key]:
                        if isinstance(entry, dict):
                            text = entry.get("text", "")
                            date_value = entry.get("date")
                            time_value = entry.get("time")

                        else:
                            text = str(entry)
                            date_value = None
                            time_value = None

                        text = text.strip()
                        if not text:
                            continue

                        item = create_item(text, date_value, time_value, completed)

                        try:
                            if lst in (app.quadrant1_list, app.quadrant1_completed_list):
                                pr = 1

                            elif lst in (app.quadrant2_list, app.quadrant2_completed_list):
                                pr = 2

                            elif lst in (app.quadrant3_list, app.quadrant3_completed_list):
                                pr = 3

                            elif lst in (app.quadrant4_list, app.quadrant4_completed_list):
                                pr = 4

                            else:
                                pr = None

                            if pr is not None:
                                try:
                                    data = item.data(Qt.UserRole) or {}
                                    data["priority"] = pr
                                    item.setData(Qt.UserRole, data)

                                except Exception:
                                    pass

                        except Exception:
                            pass

                        if isinstance(entry, dict) and entry.get("file_path"):
                            try:
                                data = item.data(Qt.UserRole) or {}
                                data["file_path"] = entry.get("file_path")
                                item.setData(Qt.UserRole, data)
                                tt = item.toolTip() or ""
                                if tt:
                                    tt = tt + "\n"

                                tt = tt + (get_text("Arquivo") or "Arquivo") + f": {entry.get('file_path')}"
                                item.setToolTip(tt)

                                try:
                                    font = item.font() or QFont()
                                    font.setBold(True)
                                    item.setFont(font)
                                    item.setForeground(Qt.blue)

                                except Exception:
                                    pass

                            except Exception:
                                logger.error("Erro ao aplicar file_path carregado", exc_info=True)

                        if isinstance(entry, dict) and entry.get("description"):
                            try:
                                data = item.data(Qt.UserRole) or {}
                                data["description"] = entry.get("description")
                                item.setData(Qt.UserRole, data)

                                try:
                                    tt = item.toolTip() or ""
                                    if tt:
                                        tt = tt + "\n"

                                    desc_full = entry.get("description") or ""
                                    preview_lines = [ln for ln in desc_full.splitlines() if ln.strip()]
                                    preview = "\n".join(preview_lines[:3])
                                    if preview:
                                        tt = tt + (get_text("Descrição") or "Descrição") + ":\n" + preview

                                    item.setToolTip(tt)

                                except Exception:
                                    pass

                            except Exception:
                                logger.error("Erro ao aplicar description carregada", exc_info=True)

                        if hasattr(app, "insert_task_into_quadrant_list"):
                            app.insert_task_into_quadrant_list(lst, item)

                        else:
                            lst.addItem(item)

            populate_list("quadrant1", app.quadrant1_list, completed=False)
            populate_list("quadrant1_completed", app.quadrant1_completed_list, completed=True)
            populate_list("quadrant2", app.quadrant2_list, completed=False)
            populate_list("quadrant2_completed", app.quadrant2_completed_list, completed=True)
            populate_list("quadrant3", app.quadrant3_list, completed=False)
            populate_list("quadrant3_completed", app.quadrant3_completed_list, completed=True)
            populate_list("quadrant4", app.quadrant4_list, completed=False)
            populate_list("quadrant4_completed", app.quadrant4_completed_list, completed=True)

    except FileNotFoundError:
        pass

    except Exception as e:
        logger.error(f"Erro ao carregar tarefas: {e}", exc_info=True)
