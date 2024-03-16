import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, \
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QDialog, QFormLayout, QMessageBox


class AddContactDialog(QDialog):
    def __init__(self, parent=None):
        super(AddContactDialog, self).__init__(parent)
        self.setWindowTitle("Add Contact")
        layout = QFormLayout()
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()
        layout.addRow("Name:", self.name_input)
        layout.addRow("Phone:", self.phone_input)
        layout.addRow("Email:", self.email_input)
        layout.addRow("Address:", self.address_input)
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_contact)
        layout.addRow(self.add_button)
        self.setLayout(layout)

    def add_contact(self):
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        address = self.address_input.text().strip()

        if name and phone:
            contact_info = [name, phone, email, address]
            main_window.add_contact(contact_info)
            self.close()
        else:
            QMessageBox.warning(
                self, "Warning", "Name and phone number are required.")


class EditContactDialog(QDialog):
    def __init__(self, contact_info, parent=None):
        super(EditContactDialog, self).__init__(parent)
        self.setWindowTitle("Edit Contact")
        layout = QFormLayout()
        self.name_input = QLineEdit(contact_info[0])
        self.phone_input = QLineEdit(contact_info[1])
        self.email_input = QLineEdit(contact_info[2])
        self.address_input = QLineEdit(contact_info[3])
        layout.addRow("Name:", self.name_input)
        layout.addRow("Phone:", self.phone_input)
        layout.addRow("Email:", self.email_input)
        layout.addRow("Address:", self.address_input)
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_contact)
        layout.addRow(self.save_button)
        self.setLayout(layout)

    def save_contact(self):
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        address = self.address_input.text().strip()

        if name and phone:
            contact_info = [name, phone, email, address]
            main_window.edit_contact(contact_info)
            self.close()
        else:
            QMessageBox.warning(
                self, "Warning", "Name and phone number are required.")


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Contact Book")
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()
        self.contact_table = QTableWidget()
        self.contact_table.setColumnCount(4)
        self.contact_table.setHorizontalHeaderLabels(
            ["Name", "Phone", "Email", "Address"])
        self.layout.addWidget(self.contact_table)
        self.add_button = QPushButton("Add Contact")
        self.add_button.clicked.connect(self.open_add_contact_dialog)
        self.layout.addWidget(self.add_button)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)
        self.contacts = []
        self.load_contacts()

    def open_add_contact_dialog(self):
        dialog = AddContactDialog(self)
        dialog.exec_()

    def add_contact(self, contact_info):
        self.contacts.append(contact_info)
        self.display_contacts()
        self.save_contacts()

    def display_contacts(self):
        self.contact_table.setRowCount(len(self.contacts))
        for row, contact in enumerate(self.contacts):
            for col, value in enumerate(contact):
                self.contact_table.setItem(row, col, QTableWidgetItem(value))

    def open_edit_contact_dialog(self, row):
        if row < len(self.contacts):
            dialog = EditContactDialog(self.contacts[row], self)
            dialog.exec_()

    def edit_contact(self, contact_info):
        index = self.contact_table.currentRow()
        if index < len(self.contacts):
            self.contacts[index] = contact_info
            self.display_contacts()
            self.save_contacts()

    def load_contacts(self):
        try:
            with open('data.json', 'r') as file:
                self.contacts = json.load(file)
                self.display_contacts()
        except FileNotFoundError:
            pass

    def save_contacts(self):
        with open('data.json', 'w') as file:
            json.dump(self.contacts, file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
