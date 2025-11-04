from PySide6.QtCore import Qt

def handle_item_checked(app, item, source_list, target_list):
    if not item.flags() & Qt.ItemIsSelectable:
        return

    try:
        source_list.blockSignals(True)
        target_list.blockSignals(True)

        if item.checkState() == Qt.Checked and source_list is not target_list:
            app.move_item_between_lists(item, source_list, target_list, Qt.Checked)

        elif item.checkState() == Qt.Unchecked and source_list is not target_list:
            app.move_item_between_lists(item, source_list, target_list, Qt.Unchecked)

    finally:
        source_list.blockSignals(False)
        target_list.blockSignals(False)

    app.save_tasks()
