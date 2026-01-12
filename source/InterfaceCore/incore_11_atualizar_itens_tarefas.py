from __future__ import annotations
from PySide6.QtCore import Qt, QCoreApplication, QDate, QLocale
from PySide6.QtWidgets import QListWidgetItem
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text: str) -> str:
    return QCoreApplication.translate("App", text)

def _effective_locale(app) -> QLocale:
    try:
        if hasattr(app, "date_input") and app.date_input is not None:
            return app.date_input.locale()

    except Exception:
        pass

    try:
        if hasattr(app, "gerenciador_traducao") and app.gerenciador_traducao is not None:
            idioma = app.gerenciador_traducao.obter_idioma_atual()
            if idioma and idioma.startswith("pt"):
                return QLocale(QLocale.Portuguese, QLocale.Brazil)

            if idioma and idioma.startswith("en"):
                return QLocale(QLocale.English, QLocale.UnitedStates)

    except Exception:
        pass

    return QLocale.system()

def _base_text_from_item(item) -> str:
    try:
        txt = (item.text() or "").strip()
        if " — " in txt:
            return txt.split(" — ", 1)[0].strip()

        return txt

    except Exception:
        return ""

def _task_lists(app):
    for attr in (
        "quadrant1_list",
        "quadrant2_list",
        "quadrant3_list",
        "quadrant4_list",
        "quadrant1_completed_list",
        "quadrant2_completed_list",
        "quadrant3_completed_list",
        "quadrant4_completed_list",
    ):
        lst = getattr(app, attr, None)
        if lst is not None:
            yield lst

def atualizar_itens_tarefas(app):
    try:
        locale = _effective_locale(app)

        try:
            date_format = app.date_input.displayFormat() if hasattr(app, "date_input") else locale.dateFormat(QLocale.ShortFormat)

        except Exception:
            date_format = locale.dateFormat(QLocale.ShortFormat)

        group_header_role = Qt.UserRole + 1

        for lst in _task_lists(app):
            tasks = []

            for i in range(lst.count()):
                item = lst.item(i)
                if not item:
                    continue

                if not (item.flags() & Qt.ItemIsSelectable):
                    continue

                try:
                    if item.data(group_header_role) == "group_header":
                        continue

                except Exception:
                    pass

                data = item.data(Qt.UserRole) or {}
                base_text = (data.get("text") or "").strip() or _base_text_from_item(item)
                if not base_text:
                    continue

                tasks.append(
                    {
                        "data": dict(data) if isinstance(data, dict) else {},
                        "base_text": base_text,
                        "check_state": item.checkState(),
                    }
                )

            if not tasks:
                continue

            lst.blockSignals(True)
            try:
                lst.clear()

                for entry in tasks:
                    data = entry["data"]
                    base_text = entry["base_text"]
                    date_iso = data.get("date")
                    time_str = data.get("time")

                    display_text = base_text
                    tooltip_lines = []

                    if date_iso:
                        qd = QDate.fromString(date_iso, Qt.ISODate)
                        if qd.isValid():
                            try:
                                date_human = locale.toString(qd, date_format)

                            except Exception:
                                date_human = qd.toString(date_format)

                            if time_str:
                                display_text = f"{base_text} — {date_human} {time_str}"

                            else:
                                display_text = f"{base_text} — {date_human}"

                            tooltip_lines.append(f"{get_text('Data') or 'Data'}: {date_human}")

                    if time_str:
                        tooltip_lines.append(f"{get_text('Horário') or 'Horário'}: {time_str}")

                    new_item = QListWidgetItem(display_text)
                    new_item.setFlags(new_item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    new_item.setCheckState(entry["check_state"])

                    if isinstance(data, dict):
                        new_data = dict(data)
                        new_data["text"] = base_text
                        new_item.setData(Qt.UserRole, new_data)

                    else:
                        new_item.setData(Qt.UserRole, {"text": base_text, "date": date_iso, "time": time_str})

                    if tooltip_lines:
                        new_item.setToolTip("\n".join(tooltip_lines))

                    if hasattr(app, "insert_task_into_quadrant_list"):
                        app.insert_task_into_quadrant_list(lst, new_item)

                    else:
                        lst.addItem(new_item)

                if hasattr(app, "cleanup_time_groups"):
                    app.cleanup_time_groups(lst)

            finally:
                lst.blockSignals(False)

    except Exception as e:
        logger.error(f"Erro ao atualizar itens de tarefas: {e}", exc_info=True)
