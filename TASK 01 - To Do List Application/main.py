import sys
import json
from PyQt5.QtWidgets import (
    QTableWidgetItem, QApplication, QMainWindow,
    QDialog, QListWidgetItem, QAbstractItemView, QStyle,
)
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon


class EditTaskWindow(QDialog):
    def __init__(self, title, status="Not Started", description="", new=False, parent=None):
        super(EditTaskWindow, self).__init__(parent)
        # load the UI from home.ui
        loadUi("edit.ui", self)
        self.setWindowTitle("Edit Task" if new == False else "Create new Task")
        self.setWindowIcon(QIcon("icon.png"))

        self.save_button.clicked.connect(self.save_task)
        # set the initial values of the title and description
        self.title_edit.setText(title)
        self.description_edit.setText(description)
        self.status_combo.setCurrentText(status)
        self.save_button.setIcon(
            QApplication.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.cancel_button.setIcon(
            QApplication.style().standardIcon(QStyle.SP_FileDialogBack))

    def save_task(self):
        self.accept()


class TaskWidgetItem(QListWidgetItem):
    def __init__(self, title, status, description):
        super().__init__()
        self.setText(title)
        self.status = status
        self.description = description


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # load the UI from home.ui
        loadUi("home.ui", self)
        self.setWindowTitle("To-Do Application")
        # Replace "icon.png" with your icon file path
        self.setWindowIcon(QIcon("icon.png"))

        self.task_table.setColumnCount(3)
        self.task_table.setHorizontalHeaderLabels(
            ["Title", "Status", "Description"])
        self.task_table.itemDoubleClicked.connect(self.edit_task)
        self.task_table.setEditTriggers(
            QAbstractItemView.NoEditTriggers)  # Disable editing
        self.task_table.setSelectionMode(
            QAbstractItemView.NoSelection)  # Disable selection

        self.btn_create.clicked.connect(self.create_task)
        self.btn_create.setIcon(QApplication.style(
        ).standardIcon(QStyle.SP_FileDialogNewFolder))
        self.btn_exit.setIcon(QApplication.style().standardIcon(
            QStyle.SP_DialogCancelButton))
        self.load_data()

    def create_task(self):
        self.edit_window = EditTaskWindow("", "", new=True)
        if self.edit_window.exec_() == QDialog.Accepted:
            title = self.edit_window.title_edit.text()
            status = self.edit_window.status_combo.currentText()
            description = self.edit_window.description_edit.toPlainText()
            row_position = self.task_table.rowCount()
            self.task_table.insertRow(row_position)
            self.task_table.setItem(row_position, 0, QTableWidgetItem(title))
            self.task_table.setItem(row_position, 1, QTableWidgetItem(status))
            self.task_table.setItem(
                row_position, 2, QTableWidgetItem(description))
            self.save_data()

    def edit_task(self, item):
        title = self.task_table.item(item.row(), 0).text()
        status = self.task_table.item(item.row(), 1).text()
        description = self.task_table.item(item.row(), 2).text()

        self.edit_window = EditTaskWindow(title, status, description)
        if self.edit_window.exec_() == QDialog.Accepted:
            self.task_table.item(item.row(), 0).setText(
                self.edit_window.title_edit.text())
            self.task_table.item(item.row(), 1).setText(
                self.edit_window.status_combo.currentText())
            self.task_table.item(item.row(), 2).setText(
                self.edit_window.description_edit.toPlainText())
            self.save_data()

    def save_data(self):
        data = []
        for row in range(self.task_table.rowCount()):
            title = self.task_table.item(row, 0).text()
            status = self.task_table.item(row, 1).text()
            description = self.task_table.item(row, 2).text()
            data.append({"title": title, "status": status,
                        "description": description})
        with open("data.json", "w") as json_file:
            json.dump(data, json_file)

    def load_data(self):
        try:
            with open("data.json", "r") as json_file:
                data = json.load(json_file)
            for item in data:
                row_position = self.task_table.rowCount()
                self.task_table.insertRow(row_position)
                self.task_table.setItem(
                    row_position, 0, QTableWidgetItem(item["title"]))
                self.task_table.setItem(
                    row_position, 1, QTableWidgetItem(item["status"]))
                self.task_table.setItem(
                    row_position, 2, QTableWidgetItem(item["description"]))
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
