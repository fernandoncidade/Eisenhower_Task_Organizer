from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget, QAbstractItemView
from PySide6.QtGui import QDrag
from source.utils.LogManager import LogManager

logger = LogManager.get_logger()


class TaskListWidget(QListWidget):
    def __init__(self, app, is_completed: bool, parent=None):
        super().__init__(parent)
        self._app = app
        self._is_completed = bool(is_completed)

        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.CopyAction)
        self.setDragDropMode(QAbstractItemView.DragDrop)

    def startDrag(self, supportedActions):
        try:
            if not self.selectedItems():
                return

            mime = self.model().mimeData(self.selectedIndexes())
            if mime is None:
                return

            drag = QDrag(self)
            drag.setMimeData(mime)

            drag.exec(Qt.CopyAction)

        except Exception as e:
            logger.error(f"Erro no startDrag do TaskListWidget: {e}", exc_info=True)

    def dropEvent(self, event):
        try:
            source = event.source()
            if not isinstance(source, QListWidget):
                return super().dropEvent(event)

            if source is self:
                event.ignore()
                return

            dragged_items = source.selectedItems()
            if not dragged_items:
                event.ignore()
                return

            item = dragged_items[0]
            if not (item.flags() & Qt.ItemIsSelectable):
                event.ignore()
                return

            new_state = Qt.Checked if self._is_completed else Qt.Unchecked

            source.blockSignals(True)
            self.blockSignals(True)
            try:
                self._app.move_item_between_lists(item, source, self, new_state)

            finally:
                source.blockSignals(False)
                self.blockSignals(False)

            try:
                self._app.save_tasks()

            except Exception as e:
                logger.error(f"Erro ao salvar tarefas após drag-and-drop: {e}", exc_info=True)

            try:
                if hasattr(self._app, "calendar_pane") and self._app.calendar_pane:
                    self._app.calendar_pane.calendar_panel.update_task_list()

            except Exception as e:
                logger.error(f"Erro ao atualizar calendário após drag-and-drop: {e}", exc_info=True)

            event.setDropAction(Qt.CopyAction)
            event.accept()

        except Exception as e:
            logger.error(f"Erro no dropEvent do TaskListWidget: {e}", exc_info=True)
            event.ignore()
