from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QFileDialog, QMessageBox, QListWidgetItem
from PySide6.QtCore import Qt
import os
from source.utils.LogManager import LogManager
logger = LogManager.get_logger()

def get_text(text):
    return QCoreApplication.translate("InterfaceGrafica", text)

def _clear_all_lists(app):
    for lst in (
        app.quadrant1_list, app.quadrant2_list, app.quadrant3_list, app.quadrant4_list,
        app.quadrant1_completed_list, app.quadrant2_completed_list, app.quadrant3_completed_list, app.quadrant4_completed_list
    ):
        lst.clear()

def _add_placeholders_after_clear(app):
    app.add_placeholder(app.quadrant1_list, get_text("1º Quadrante"))
    app.add_placeholder(app.quadrant2_list, get_text("2º Quadrante"))
    app.add_placeholder(app.quadrant3_list, get_text("3º Quadrante"))
    app.add_placeholder(app.quadrant4_list, get_text("4º Quadrante"))
    app.add_placeholder(app.quadrant1_completed_list, get_text("Nenhuma Tarefa Concluída"))
    app.add_placeholder(app.quadrant2_completed_list, get_text("Nenhuma Tarefa Concluída"))
    app.add_placeholder(app.quadrant3_completed_list, get_text("Nenhuma Tarefa Concluída"))
    app.add_placeholder(app.quadrant4_completed_list, get_text("Nenhuma Tarefa Concluída"))

def novo(app):
    _clear_all_lists(app)
    _add_placeholders_after_clear(app)
    app.task_input.clear()
    try:
        app.save_tasks()
        if hasattr(app, "calendar_pane") and app.calendar_pane:
            app.calendar_pane.calendar_panel.update_task_list()

    except Exception as e:
        logger.error(f"Erro ao iniciar nova sessão: {e}", exc_info=True)

    QMessageBox.information(app, get_text("Novo"), get_text("Nova sessão iniciada.") or "Nova sessão iniciada.")

def limpar_tudo(app):
    _clear_all_lists(app)
    _add_placeholders_after_clear(app)
    app.task_input.clear()
    try:
        app.save_tasks()
        if hasattr(app, "calendar_pane") and app.calendar_pane:
            app.calendar_pane.calendar_panel.update_task_list()

    except Exception as e:
        logger.error(f"Erro ao limpar tudo: {e}", exc_info=True)

    QMessageBox.information(app, get_text("Limpar"), get_text("Todos os dados foram removidos.") or "Todos os dados foram removidos.")

def sair(app):
    from PySide6.QtWidgets import QApplication
    QApplication.quit()

def abrir_arquivo(app):
    path, filt = QFileDialog.getOpenFileName(app, get_text("Abrir"), os.path.expanduser("~"), "Excel (*.xlsx);;PDF (*.pdf)")
    if not path:
        return

    def _parse_text_date_time(raw_text: str):
        base = (raw_text or "").strip()
        date_iso = None
        time_str = None
        if " — " in base:
            left, right = base.rsplit(" — ", 1)
            tail = right.strip()
            try:
                from PySide6.QtCore import QDate, QTime
                fmts = []
                try:
                    fmts.append(app.date_input.displayFormat())

                except Exception as e:
                    logger.error(f"Erro ao obter formato de data para parsing: {e}", exc_info=True)

                fmts += ["dd/MM/yyyy", "d/M/yyyy", "MM/dd/yyyy", "M/d/yyyy", "yyyy-MM-dd"]

                parts = tail.split()
                if len(parts) == 2:
                    d_candidate, t_candidate = parts
                    for fmt in fmts:
                        qd = QDate.fromString(d_candidate, fmt)
                        if qd and qd.isValid():
                            qt = QTime.fromString(t_candidate, "HH:mm")
                            if qt.isValid():
                                date_iso = qd.toString(Qt.ISODate)
                                time_str = qt.toString("HH:mm")
                                base = left.strip()
                                break

                if date_iso is None:
                    for fmt in fmts:
                        qd = QDate.fromString(tail, fmt)
                        if qd and qd.isValid():
                            date_iso = qd.toString(Qt.ISODate)
                            base = left.strip()
                            break

                if date_iso is None:
                    from PySide6.QtCore import QTime
                    qt = QTime.fromString(tail, "HH:mm")
                    if qt.isValid():
                        time_str = qt.toString("HH:mm")
                        base = left.strip()

            except Exception as e:
                logger.error(f"Erro ao fazer parsing de data/hora: {e}", exc_info=True)

        return base, date_iso, time_str

    ext = os.path.splitext(path)[1].lower()
    if ext == ".xlsx":
        try:
            from openpyxl import load_workbook

        except Exception as e:
            logger.error(f"openpyxl não está disponível: {e}", exc_info=True)
            QMessageBox.critical(app, get_text("Erro"), get_text("openpyxl não está disponível."))
            return

        try:
            wb = load_workbook(path, read_only=True)
            def populate_from_sheet(name, lst, completed=False):
                if name in wb.sheetnames:
                    sheet = wb[name]
                    lst.clear()
                    for row in sheet.iter_rows(min_row=1, max_col=1, values_only=True):
                        val = row[0]
                        if val and str(val).strip():
                            raw_text = str(val).strip()
                            text, date_iso, time_str = _parse_text_date_time(raw_text)
                            item = QListWidgetItem(raw_text)
                            item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                            item.setCheckState(Qt.Checked if completed else Qt.Unchecked)
                            item.setData(Qt.UserRole, {"text": text, "date": date_iso, "time": time_str})
                            tooltip_lines = []
                            if date_iso:
                                try:
                                    from PySide6.QtCore import QDate
                                    qd = QDate.fromString(date_iso, Qt.ISODate)
                                    if qd.isValid():
                                        tooltip_lines.append(f"{get_text('Data') or 'Data'}: {qd.toString(app.date_input.displayFormat())}")

                                except Exception as e:
                                    logger.error(f"Erro ao definir tooltip de data: {e}", exc_info=True)

                            if time_str:
                                tooltip_lines.append(f"{get_text('Horário') or 'Horário'}: {time_str}")

                            if tooltip_lines:
                                item.setToolTip("\n".join(tooltip_lines))

                            try:
                                app.insert_task_into_quadrant_list(lst, item)

                            except Exception as e:
                                logger.error(f"Erro ao inserir tarefa na lista do quadrante: {e}", exc_info=True)
                                lst.addItem(item)

            populate_from_sheet("quadrant1", app.quadrant1_list, completed=False)
            populate_from_sheet("quadrant1_completed", app.quadrant1_completed_list, completed=True)
            populate_from_sheet("quadrant2", app.quadrant2_list, completed=False)
            populate_from_sheet("quadrant2_completed", app.quadrant2_completed_list, completed=True)
            populate_from_sheet("quadrant3", app.quadrant3_list, completed=False)
            populate_from_sheet("quadrant3_completed", app.quadrant3_completed_list, completed=True)
            populate_from_sheet("quadrant4", app.quadrant4_list, completed=False)
            populate_from_sheet("quadrant4_completed", app.quadrant4_completed_list, completed=True)

            app.save_tasks()
            try:
                if hasattr(app, "calendar_pane") and app.calendar_pane:
                    app.calendar_pane.calendar_panel.update_task_list()

            except Exception as e:
                logger.error(f"Erro ao atualizar lista de tarefas no calendário: {e}", exc_info=True)

            QMessageBox.information(app, get_text("Abrir"), get_text("Arquivo importado com sucesso."))

        except Exception as e:
            logger.error(f"Erro ao importar arquivo XLSX: {e}", exc_info=True)
            QMessageBox.critical(app, get_text("Erro"), f"{get_text('Erro') or 'Erro'}: {e}")

    elif ext == ".pdf":
        try:
            from PyPDF2 import PdfReader

        except Exception as e:
            logger.error(f"PyPDF2 não está disponível: {e}", exc_info=True)
            QMessageBox.critical(app, get_text("Erro"), get_text("PyPDF2 não está disponível para ler PDF."))
            return

        try:
            reader = PdfReader(path)
            text = ""
            for page in reader.pages:
                try:
                    page_text = page.extract_text() or ""
                    text += page_text + "\n"

                except Exception as e:
                    logger.error(f"Erro ao extrair texto da página do PDF: {e}", exc_info=True)

            import unicodedata, re
            def normalize(s: str) -> str:
                s2 = unicodedata.normalize("NFKD", s)
                s2 = s2.encode("ASCII", "ignore").decode("ASCII")
                s2 = s2.lower()
                s2 = re.sub(r'\s+', ' ', s2).strip()
                return s2

            title_map = {
                normalize("1º Quadrante - Importante e Urgente"): "quadrant1",
                normalize("Concluídas 1º Quadrante"): "quadrant1_completed",
                normalize("2º Quadrante - Importante, mas Não Urgente"): "quadrant2",
                normalize("Concluídas 2º Quadrante"): "quadrant2_completed",
                normalize("3º Quadrante - Não Importante, mas Urgente"): "quadrant3",
                normalize("Concluídas 3º Quadrante"): "quadrant3_completed",
                normalize("4º Quadrante - Não Importante e Não Urgente"): "quadrant4",
                normalize("Concluídas 4º Quadrante"): "quadrant4_completed",
            }

            segments = {k: [] for k in title_map.values()}
            current_key = None
            for raw_line in text.splitlines():
                line = raw_line.strip()
                if not line:
                    continue

                n = normalize(line)
                if n in title_map:
                    current_key = title_map[n]
                    continue

                if current_key:
                    cleaned = re.sub(r'^[\-\u2013\u2014\u2022\u2023\•\*\•\s]+', '', line).strip()
                    if cleaned:
                        segments[current_key].append(cleaned)

            if not any(segments.values()):
                lower = text.lower()
                keys = ["quadrant1", "quadrant1_completed", "quadrant2", "quadrant2_completed",
                        "quadrant3", "quadrant3_completed", "quadrant4", "quadrant4_completed"]

                found_any = False
                for i, key in enumerate(keys):
                    start = lower.find(key + ":")
                    if start != -1:
                        found_any = True
                        end = len(lower)
                        for k in keys[i+1:]:
                            j = lower.find(k + ":", start+1)
                            if j != -1:
                                end = j
                                break

                        segment_text = text[start+len(key)+1:end].strip()
                        for line in segment_text.splitlines():
                            line = line.strip()
                            if line:
                                cleaned = re.sub(r'^[\-\u2013\u2014\u2022\u2023\•\*\s]+', '', line).strip()
                                if cleaned:
                                    segments[key].append(cleaned)

                if not found_any:
                    QMessageBox.warning(app, get_text("Abrir"), get_text("PDF não está no formato compatível."))
                    return

            def populate_from_list(key, lst, completed=False):
                lst.clear()
                items = segments.get(key, [])
                for it in items:
                    raw_text = it.strip()
                    text_only, date_iso, time_str = _parse_text_date_time(raw_text)
                    item = QListWidgetItem(raw_text)  # mantém exibição
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    item.setCheckState(Qt.Checked if completed else Qt.Unchecked)
                    item.setData(Qt.UserRole, {"text": text_only, "date": date_iso, "time": time_str})
                    tooltip_lines = []
                    if date_iso:
                        try:
                            from PySide6.QtCore import QDate
                            qd = QDate.fromString(date_iso, Qt.ISODate)
                            if qd.isValid():
                                tooltip_lines.append(f"{get_text('Data') or 'Data'}: {qd.toString(app.date_input.displayFormat())}")

                        except Exception as e:
                            logger.error(f"Erro ao definir tooltip de data no PDF: {e}", exc_info=True)

                    if time_str:
                        tooltip_lines.append(f"{get_text('Horário') or 'Horário'}: {time_str}")

                    if tooltip_lines:
                        item.setToolTip("\n".join(tooltip_lines))

                    try:
                        app.insert_task_into_quadrant_list(lst, item)

                    except Exception as e:
                        logger.error(f"Erro ao inserir tarefa na lista do quadrante (PDF): {e}", exc_info=True)
                        lst.addItem(item)

            populate_from_list("quadrant1", app.quadrant1_list, False)
            populate_from_list("quadrant1_completed", app.quadrant1_completed_list, True)
            populate_from_list("quadrant2", app.quadrant2_list, False)
            populate_from_list("quadrant2_completed", app.quadrant2_completed_list, True)
            populate_from_list("quadrant3", app.quadrant3_list, False)
            populate_from_list("quadrant3_completed", app.quadrant3_completed_list, True)
            populate_from_list("quadrant4", app.quadrant4_list, False)
            populate_from_list("quadrant4_completed", app.quadrant4_completed_list, True)

            app.save_tasks()
            try:
                if hasattr(app, "calendar_pane") and app.calendar_pane:
                    app.calendar_pane.calendar_panel.update_task_list()

            except Exception as e:
                logger.error(f"Erro ao atualizar lista de tarefas no calendário (PDF): {e}", exc_info=True)

            QMessageBox.information(app, get_text("Abrir"), get_text("PDF importado com sucesso."))

        except Exception as e:
            logger.error(f"Erro ao importar arquivo PDF: {e}", exc_info=True)
            QMessageBox.critical(app, get_text("Erro"), f"{get_text('Erro') or 'Erro'}: {e}")

    else:
        QMessageBox.warning(app, get_text("Abrir"), get_text("Formato de arquivo não suportado."))

def salvar_como(app):
    path, filt = QFileDialog.getSaveFileName(app, get_text("Salvar"), os.path.expanduser("~"), "JSON (*.json);;Excel (*.xlsx);;PDF (*.pdf)")
    if not path:
        return

    def _qenum_to_int(v):
        try:
            return int(v)

        except Exception:
            try:
                return int(getattr(v, "value"))

            except Exception:
                try:
                    return int(v.value())

                except Exception:
                    return None

    ext = os.path.splitext(path)[1].lower()
    if ext == ".xlsx":
        try:
            from openpyxl import Workbook

        except Exception as e:
            logger.error(f"openpyxl não está disponível para salvar XLSX: {e}", exc_info=True)
            QMessageBox.critical(app, get_text("Erro"), get_text("openpyxl não está disponível para salvar XLSX."))
            return

        try:
            wb = Workbook()
            def write_sheet(name, lst):
                if name in wb.sheetnames:
                    ws = wb[name]

                else:
                    ws = wb.create_sheet(title=name)

                headers = [
                    "text",
                    "date",
                    "time",
                    "file_path",
                    "description",
                    "priority",
                ]
                for col_index, h in enumerate(headers, start=1):
                    ws.cell(row=1, column=col_index, value=h)

                row = 2
                for i in range(lst.count()):
                    item = lst.item(i)
                    if item and (item.flags() & Qt.ItemIsSelectable):
                        data = item.data(Qt.UserRole) or {}
                        text_val = data.get("text", item.text())
                        date_iso = data.get("date")
                        time_str = data.get("time")
                        file_path = data.get("file_path")
                        description = data.get("description")
                        priority = data.get("priority") if data.get("priority") is not None else None

                        values = [
                            text_val,
                            date_iso,
                            time_str,
                            file_path,
                            description,
                            priority,
                        ]

                        for col_index, v in enumerate(values, start=1):
                            ws.cell(row=row, column=col_index, value=v)

                        row += 1

            if "Sheet" in wb.sheetnames and len(wb.sheetnames) == 1:
                ws_default = wb["Sheet"]
                wb.remove(ws_default)

            write_sheet("quadrant1", app.quadrant1_list)
            write_sheet("quadrant1_completed", app.quadrant1_completed_list)
            write_sheet("quadrant2", app.quadrant2_list)
            write_sheet("quadrant2_completed", app.quadrant2_completed_list)
            write_sheet("quadrant3", app.quadrant3_list)
            write_sheet("quadrant3_completed", app.quadrant3_completed_list)
            write_sheet("quadrant4", app.quadrant4_list)
            write_sheet("quadrant4_completed", app.quadrant4_completed_list)

            wb.save(path)
            QMessageBox.information(app, get_text("Salvar"), get_text("Arquivo salvo com sucesso."))

        except Exception as e:
            logger.error(f"Erro ao salvar arquivo XLSX: {e}", exc_info=True)
            QMessageBox.critical(app, get_text("Erro"), f"{get_text('Erro') or 'Erro'}: {e}")

    elif ext == ".pdf":
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas

        except Exception as e:
            logger.error(f"reportlab não está disponível para salvar PDF: {e}", exc_info=True)
            QMessageBox.critical(app, get_text("Erro"), get_text("reportlab não está disponível para salvar PDF."))
            return

        try:
            c = canvas.Canvas(path, pagesize=A4)
            width, height = A4
            from reportlab.lib.units import cm
            left_margin = 1 * cm
            right_margin = 1 * cm
            top_margin = 1 * cm
            bottom_margin = 1 * cm
            y = height - top_margin
            c.setFont("Helvetica-Bold", 14)
            c.drawString(left_margin, y, "EISENHOWER ORGANIZER")
            y -= 30
            c.setFont("Helvetica-Bold", 12)
            sections = [
                ("1º Quadrante - Importante e Urgente", app.quadrant1_list),
                ("Concluídas 1º Quadrante", app.quadrant1_completed_list),
                ("2º Quadrante - Importante, mas Não Urgente", app.quadrant2_list),
                ("Concluídas 2º Quadrante", app.quadrant2_completed_list),
                ("3º Quadrante - Não Importante, mas Urgente", app.quadrant3_list),
                ("Concluídas 3º Quadrante", app.quadrant3_completed_list),
                ("4º Quadrante - Não Importante e Não Urgente", app.quadrant4_list),
                ("Concluídas 4º Quadrante", app.quadrant4_completed_list),
            ]
            c.setFont("Helvetica", 10)
            from reportlab.lib.utils import simpleSplit
            from reportlab.pdfbase.pdfmetrics import stringWidth

            def _draw_wrapped(text, indent, current_y, font_name="Helvetica", font_size=10):
                if text is None:
                    return current_y

                c.setFont(font_name, font_size)

                max_width = width - left_margin - right_margin - indent
                if max_width <= 0:
                    max_width = width - left_margin - right_margin

                raw_lines = simpleSplit(text or "", font_name, font_size, max_width)

                lines = []
                for ln in raw_lines:
                    if stringWidth(ln, font_name, font_size) <= max_width:
                        lines.append(ln)

                    else:
                        cur = ""
                        for ch in ln:
                            if stringWidth(cur + ch, font_name, font_size) <= max_width:
                                cur += ch

                            else:
                                if cur:
                                    lines.append(cur)

                                cur = ch

                        if cur:
                            lines.append(cur)

                y_local = current_y
                for ln in lines:
                    if y_local < (bottom_margin + font_size + 4):
                        c.showPage()
                        y_local = height - top_margin
                        c.setFont(font_name, font_size)

                    c.drawString(left_margin + indent, y_local, ln)
                    y_local -= (font_size + 2)

                return y_local

            def _format_item_line(item, data):
                text_val = data.get("text", item.text())
                date_iso = data.get("date")
                time_str = data.get("time")
                date_display = None
                if date_iso:
                    try:
                        from PySide6.QtCore import QDate
                        qd = QDate.fromString(date_iso, Qt.ISODate)
                        if qd.isValid() and hasattr(app, "date_input") and app.date_input is not None:
                            date_display = qd.toString(app.date_input.displayFormat())

                        else:
                            date_display = date_iso

                    except Exception:
                        date_display = date_iso

                parts = []
                parts.append(text_val)
                tail = []
                if date_display:
                    tail.append(date_display)

                if time_str:
                    tail.append(time_str)

                if tail:
                    parts.append(" — " + " ".join(tail))

                return "".join(parts)

            for title, lst in sections:
                if y < (bottom_margin + 40):
                    c.showPage()
                    y = height - top_margin
                    c.setFont("Helvetica", 10)

                c.setFont("Helvetica-Bold", 11)
                c.drawString(left_margin, y, title)
                y -= 16
                c.setFont("Helvetica", 10)
                if lst.count() == 0:
                    c.drawString(left_margin + 10, y, "-")
                    y -= 12

                else:
                    for i in range(lst.count()):
                        item = lst.item(i)
                        if item and (item.flags() & Qt.ItemIsSelectable):
                            data = item.data(Qt.UserRole) or {}

                            main_line = _format_item_line(item, data)
                            y = _draw_wrapped(f"- {main_line}", 10, y, font_name="Helvetica", font_size=10)

                            extra_order = []
                            if data.get("priority") is not None:
                                extra_order.append(("Prioridade", str(data.get("priority"))))

                            if data.get("description"):
                                extra_order.append(("Descrição", data.get("description")))

                            if data.get("file_path"):
                                extra_order.append(("Arquivo", data.get("file_path")))

                            for label, val in extra_order:
                                y = _draw_wrapped(f"{label}: {val}", 20, y, font_name="Helvetica", font_size=9)

                            if y < (bottom_margin + 40):
                                c.showPage()
                                y = height - top_margin
                                c.setFont("Helvetica", 10)

                y -= 8

            c.save()
            QMessageBox.information(app, get_text("Salvar"), get_text("PDF salvo com sucesso."))

        except Exception as e:
            logger.error(f"Erro ao salvar arquivo PDF: {e}", exc_info=True)
            QMessageBox.critical(app, get_text("Erro"), f"{get_text('Erro') or 'Erro'}: {e}")

    elif ext == ".json":
        try:
            import json as _json

            def list_to_full_entries(lst):
                entries = []
                for i in range(lst.count()):
                    item = lst.item(i)
                    if item and (item.flags() & Qt.ItemIsSelectable):
                        data = item.data(Qt.UserRole) or {}
                        entry = {
                            "display_text": item.text(),
                            "text": data.get("text", item.text()),
                            "date": data.get("date"),
                            "time": data.get("time"),
                            "check_state": _qenum_to_int(item.checkState()),
                            "flags": _qenum_to_int(item.flags()),
                            "priority": data.get("priority"),
                            "description": data.get("description"),
                            "file_path": data.get("file_path"),
                            "tooltip": item.toolTip(),
                            "raw_data": data,
                        }
                        entries.append(entry)

                return entries

            full = {
                "meta": {
                    "date_display_format": getattr(app, "date_input", None).displayFormat() if hasattr(app, "date_input") and app.date_input is not None else None,
                    "language": getattr(getattr(app, "gerenciador_traducao", None), "obter_idioma_atual", lambda: None)(),
                },
                "quadrant1": list_to_full_entries(app.quadrant1_list),
                "quadrant1_completed": list_to_full_entries(app.quadrant1_completed_list),
                "quadrant2": list_to_full_entries(app.quadrant2_list),
                "quadrant2_completed": list_to_full_entries(app.quadrant2_completed_list),
                "quadrant3": list_to_full_entries(app.quadrant3_list),
                "quadrant3_completed": list_to_full_entries(app.quadrant3_completed_list),
                "quadrant4": list_to_full_entries(app.quadrant4_list),
                "quadrant4_completed": list_to_full_entries(app.quadrant4_completed_list),
            }

            with open(path, "w", encoding="utf-8") as f:
                _json.dump(full, f, ensure_ascii=False, indent=2)

            QMessageBox.information(app, get_text("Salvar"), get_text("Arquivo salvo com sucesso."))

        except Exception as e:
            logger.error(f"Erro ao salvar arquivo JSON: {e}", exc_info=True)
            QMessageBox.critical(app, get_text("Erro"), f"{get_text('Erro') or 'Erro'}: {e}")

    else:
        QMessageBox.warning(app, get_text("Salvar"), get_text("Extensão não suportada."))
