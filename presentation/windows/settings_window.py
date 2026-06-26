from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from domain.employee import Employee
from domain.revenue_template import Stylist
from infrastructure.config_manager import ConfigManager


class SettingsWindow(QDialog):
    def __init__(self, config_manager: ConfigManager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.setWindowTitle("Settings")
        self.setMinimumSize(600, 400)

        self._build_ui()
        self._load_data()

    def _build_ui(self):
        layout = QVBoxLayout()

        # Output Directory Section
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(QLabel("Output Directory:"))
        self.dir_input = QLineEdit()
        self.dir_input.setReadOnly(True)
        dir_layout.addWidget(self.dir_input)

        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self._browse_directory)
        dir_layout.addWidget(self.browse_btn)

        layout.addLayout(dir_layout)

        # Employees Section
        layout.addWidget(QLabel("Employees:"))

        self.employees_table = QTableWidget()
        self.employees_table.setColumnCount(3)
        self.employees_table.setHorizontalHeaderLabels(
            ["Name", "Working Hours", "Daily Rate"]
        )
        self.employees_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.employees_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.employees_table)

        # Buttons for employees
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Employee")
        self.add_btn.clicked.connect(self._add_employee)
        btn_layout.addWidget(self.add_btn)

        self.remove_btn = QPushButton("Remove Selected")
        self.remove_btn.clicked.connect(self._remove_employee)
        btn_layout.addWidget(self.remove_btn)

        layout.addLayout(btn_layout)

        # Stylists Section
        layout.addWidget(QLabel("Stylists:"))

        self.stylists_table = QTableWidget()
        self.stylists_table.setColumnCount(4)
        self.stylists_table.setHorizontalHeaderLabels(
            ["Name", "Daily Target", "Daily Rate", "Working Hours"]
        )
        self.stylists_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.stylists_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.stylists_table)

        # Buttons for stylists
        stylist_btn_layout = QHBoxLayout()
        self.add_stylist_btn = QPushButton("Add Stylist")
        self.add_stylist_btn.clicked.connect(self._add_stylist)
        stylist_btn_layout.addWidget(self.add_stylist_btn)

        self.remove_stylist_btn = QPushButton("Remove Selected")
        self.remove_stylist_btn.clicked.connect(self._remove_stylist)
        stylist_btn_layout.addWidget(self.remove_stylist_btn)

        layout.addLayout(stylist_btn_layout)

        # Save / Cancel
        actions_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self._save_settings)
        actions_layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        actions_layout.addWidget(self.cancel_btn)

        layout.addLayout(actions_layout)

        self.setLayout(layout)

    def _load_data(self):
        config = self.config_manager.load()
        self.dir_input.setText(config.get("output_directory", "./output"))

        employees = config.get("employees", [])
        self.employees_table.setRowCount(len(employees))
        for i, emp in enumerate(employees):
            self.employees_table.setItem(i, 0, QTableWidgetItem(emp.get("name", "")))
            self.employees_table.setItem(
                i, 1, QTableWidgetItem(str(emp.get("working_hours", "")))
            )
            self.employees_table.setItem(
                i, 2, QTableWidgetItem(str(emp.get("daily_rate", "")))
            )

        stylists = config.get("stylists", [])
        self.stylists_table.setRowCount(len(stylists))
        for i, s in enumerate(stylists):
            self.stylists_table.setItem(i, 0, QTableWidgetItem(s.get("name", "")))
            self.stylists_table.setItem(
                i, 1, QTableWidgetItem(str(s.get("daily_target", "")))
            )
            self.stylists_table.setItem(
                i, 2, QTableWidgetItem(str(s.get("daily_rate", "")))
            )
            self.stylists_table.setItem(
                i, 3, QTableWidgetItem(str(s.get("working_hours", "")))
            )

    def _browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.dir_input.setText(directory)

    def _add_employee(self):
        row = self.employees_table.rowCount()
        self.employees_table.insertRow(row)
        self.employees_table.setItem(row, 0, QTableWidgetItem(""))
        self.employees_table.setItem(row, 1, QTableWidgetItem("8"))
        self.employees_table.setItem(row, 2, QTableWidgetItem("0"))

    def _remove_employee(self):
        selected = self.employees_table.selectedIndexes()
        if not selected:
            return
        rows = sorted(set(index.row() for index in selected), reverse=True)
        for row in rows:
            self.employees_table.removeRow(row)

    def _add_stylist(self):
        row = self.stylists_table.rowCount()
        self.stylists_table.insertRow(row)
        self.stylists_table.setItem(row, 0, QTableWidgetItem(""))
        self.stylists_table.setItem(row, 1, QTableWidgetItem("1500"))
        self.stylists_table.setItem(row, 2, QTableWidgetItem("0"))
        self.stylists_table.setItem(row, 3, QTableWidgetItem("0"))

    def _remove_stylist(self):
        selected = self.stylists_table.selectedIndexes()
        if not selected:
            return
        rows = sorted(set(index.row() for index in selected), reverse=True)
        for row in rows:
            self.stylists_table.removeRow(row)

    def _save_settings(self):
        output_dir = self.dir_input.text().strip()
        if not output_dir:
            QMessageBox.warning(
                self, "Validation Error", "Output directory is required."
            )
            return

        employees = []
        for row in range(self.employees_table.rowCount()):
            name_item = self.employees_table.item(row, 0)
            hours_item = self.employees_table.item(row, 1)
            rate_item = self.employees_table.item(row, 2)

            name = name_item.text().strip() if name_item else ""
            hours_str = hours_item.text().strip() if hours_item else ""
            rate_str = rate_item.text().strip() if rate_item else ""

            if not name:
                QMessageBox.warning(
                    self,
                    "Validation Error",
                    f"Employee name is required at row {row + 1}.",
                )
                return

            try:
                hours = int(hours_str)
            except ValueError:
                QMessageBox.warning(
                    self, "Validation Error", f"Invalid working hours at row {row + 1}."
                )
                return

            try:
                rate = int(rate_str)
            except ValueError:
                QMessageBox.warning(
                    self, "Validation Error", f"Invalid daily rate at row {row + 1}."
                )
                return

            employees.append(Employee(name=name, working_hours=hours, daily_rate=rate))

        stylists = []
        for row in range(self.stylists_table.rowCount()):
            name_item = self.stylists_table.item(row, 0)
            target_item = self.stylists_table.item(row, 1)
            rate_item = self.stylists_table.item(row, 2)
            hours_item = self.stylists_table.item(row, 3)

            name = name_item.text().strip() if name_item else ""
            target_str = target_item.text().strip() if target_item else ""
            rate_str = rate_item.text().strip() if rate_item else ""
            hours_str = hours_item.text().strip() if hours_item else ""

            if not name:
                QMessageBox.warning(
                    self,
                    "Validation Error",
                    f"Stylist name is required at row {row + 1}.",
                )
                return

            try:
                target = int(target_str)
            except ValueError:
                QMessageBox.warning(
                    self, "Validation Error", f"Invalid daily target at row {row + 1}."
                )
                return

            try:
                rate = int(rate_str)
            except ValueError:
                QMessageBox.warning(
                    self, "Validation Error", f"Invalid daily rate at row {row + 1}."
                )
                return

            try:
                hours = int(hours_str)
            except ValueError:
                QMessageBox.warning(
                    self, "Validation Error", f"Invalid working hours at row {row + 1}."
                )
                return

            stylists.append(Stylist(name=name, daily_target=target, daily_rate=rate, working_hours=hours))

        self.config_manager.set_output_directory(output_dir)
        self.config_manager.set_employees(employees)
        self.config_manager.set_stylists(stylists)

        QMessageBox.information(self, "Success", "Settings saved successfully.")
        self.accept()
