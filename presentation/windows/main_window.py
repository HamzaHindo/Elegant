from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from application.attendance_template_service import AttendanceTemplateService
from application.revenue_template_service import RevenueTemplateService
from application.salary_template_service import SalaryTemplateService
from infrastructure.attendance_template_writer import AttendanceTemplateWriter
from infrastructure.config_manager import ConfigManager
from infrastructure.revenue_template_writer import RevenueTemplateWriter
from infrastructure.salaries_template_writer import SalariesTemplateWriter
from presentation.windows.settings_window import SettingsWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Elegant Barbershop")
        self.setMinimumSize(400, 200)

        self.config_manager = ConfigManager()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Title
        layout.addWidget(QLabel("Monthly Reports Generator"))

        # Year and Month inputs
        inputs_layout = QHBoxLayout()

        inputs_layout.addWidget(QLabel("Year:"))
        self.year_spin = QSpinBox()
        self.year_spin.setRange(2000, 2100)
        self.year_spin.setValue(2026)
        inputs_layout.addWidget(self.year_spin)

        inputs_layout.addWidget(QLabel("Month:"))
        self.month_spin = QSpinBox()
        self.month_spin.setRange(1, 12)
        self.month_spin.setValue(1)
        inputs_layout.addWidget(self.month_spin)

        layout.addLayout(inputs_layout)

        # Generate all button (main button)
        self.generate_all_btn = QPushButton(
            "Generate All Reports (Attendance + Revenue + Salaries)"
        )
        self.generate_all_btn.clicked.connect(self._on_generate_all)
        self.generate_all_btn.setStyleSheet(
            "QPushButton { font-weight: bold; padding: 10px; }"
        )
        layout.addWidget(self.generate_all_btn)

        # Individual generate buttons (in a horizontal layout)
        individual_buttons_layout = QHBoxLayout()

        self.generate_attendance_btn = QPushButton("Attendance Only")
        self.generate_attendance_btn.clicked.connect(self._on_generate_attendance)
        individual_buttons_layout.addWidget(self.generate_attendance_btn)

        self.generate_revenue_btn = QPushButton("Revenue Only")
        self.generate_revenue_btn.clicked.connect(self._on_generate_revenue)
        individual_buttons_layout.addWidget(self.generate_revenue_btn)

        self.generate_salaries_btn = QPushButton("Salaries Only")
        self.generate_salaries_btn.clicked.connect(self._on_generate_salaries)
        individual_buttons_layout.addWidget(self.generate_salaries_btn)

        layout.addLayout(individual_buttons_layout)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # Settings button
        self.settings_btn = QPushButton("Settings")
        self.settings_btn.clicked.connect(self._open_settings)
        layout.addWidget(self.settings_btn)

        central_widget.setLayout(layout)

    def _on_generate_all(self):
        """Generate all three reports (Attendance, Revenue, Salaries) in a month folder."""
        year = self.year_spin.value()
        month = self.month_spin.value()

        try:
            employees = self.config_manager.get_employees()
            stylists = self.config_manager.get_stylists()
            payment_methods = self.config_manager.get_payment_methods()

            if not employees:
                QMessageBox.warning(
                    self,
                    "No Employees",
                    "No employees found. Please add employees in Settings.",
                )
                return

            if not stylists:
                QMessageBox.warning(
                    self,
                    "No Stylists",
                    "No stylists found. Please add stylists in Settings.",
                )
                return

            output_dir = self.config_manager.get_output_directory()

            self.status_label.setText("Generating reports...")

            # Prepare month folder
            import calendar
            from datetime import date

            from domain.attendance_template import AttendanceTemplate
            from domain.revenue_template import RevenueTemplate
            from domain.salary_template import SalaryTemplate
            from infrastructure.file_manager import FileManager
            from utils.calendar_utils import get_arabic_month

            file_manager = FileManager(output_dir)
            month_folder = file_manager.prepare_month_folder_for_generation(year, month)

            # Generate days for the month
            num_days = calendar.monthrange(year, month)[1]
            days = [date(year, month, day) for day in range(1, num_days + 1)]

            # Generate Attendance
            attendance_writer = AttendanceTemplateWriter(output_directory=output_dir)
            attendance_template = AttendanceTemplate(
                month=month,
                year=year,
                employees=employees,
                days=days,
                stylists=stylists,
            )
            attendance_writer.write(attendance_template, use_month_folder=True)

            # Generate Revenue
            revenue_writer = RevenueTemplateWriter(output_directory=output_dir)
            revenue_template = RevenueTemplate(
                month=month,
                year=year,
                days=days,
                stylists=stylists,
                employees=employees,
                payment_methods=payment_methods,
            )
            revenue_writer.write(revenue_template, use_month_folder=True)

            # Generate Salaries (reads from attendance file in month folder)
            salaries_writer = SalariesTemplateWriter(output_directory=output_dir)

            # Construct attendance file path in month folder
            attendance_filename = f"Attendance_{month}_{year}.xlsx"
            revenue_filename = f"Revenue_{month}_{year}.xlsx"
            attendance_file_path = file_manager.get_month_folder_output_path(
                year, month, attendance_filename
            )
            revenue_file_path = file_manager.get_month_folder_output_path(
                year, month, revenue_filename
            )

            salary_template = SalaryTemplate(
                month=month,
                year=year,
                employees=employees,
                stylists=stylists,
                attendance_file_path=attendance_file_path,
                borrows_file_path=revenue_file_path,
            )
            salaries_writer.write(salary_template, use_month_folder=True)

            month_name = get_arabic_month(month)

            self.status_label.setText(
                f"✅ All reports generated successfully in folder: {month_name}/"
            )

            QMessageBox.information(
                self,
                "Success",
                f"All reports generated successfully!\n\n"
                f"Location: {month_folder}\n\n"
                f"Files:\n"
                f"• Attendance_{month}_{year}.xlsx\n"
                f"• Revenue_{month}_{year}.xlsx\n"
                f"• Salaries_{month}_{year}.xlsx",
            )
        except Exception as e:
            import traceback

            error_details = traceback.format_exc()
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to generate reports:\n{str(e)}\n\nDetails:\n{error_details}",
            )
            self.status_label.setText("Generation failed.")

    def _on_generate_attendance(self):
        year = self.year_spin.value()
        month = self.month_spin.value()

        try:
            employees = self.config_manager.get_employees()
            stylists = self.config_manager.get_stylists()
            attendance_filename = self.config_manager.get_filename("attendance")
            if not employees:
                QMessageBox.warning(
                    self,
                    "No Employees",
                    "No employees found. Please add employees in Settings.",
                )
                return

            output_dir = self.config_manager.get_output_directory()

            writer = AttendanceTemplateWriter(output_directory=output_dir)
            service = AttendanceTemplateService(writer=writer)

            service.generate(
                month=month, year=year, employees=employees, stylists=stylists
            )

            self.status_label.setText(
                f"Generated Attendance_{month}_{year}.xlsx successfully!"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate sheet:\n{str(e)}")
            self.status_label.setText("Generation failed.")

    def _on_generate_revenue(self):
        year = self.year_spin.value()
        month = self.month_spin.value()

        try:
            stylists = self.config_manager.get_stylists()
            employees = self.config_manager.get_employees()
            payment_methods = self.config_manager.get_payment_methods()

            if not stylists:
                QMessageBox.warning(
                    self,
                    "No Stylists",
                    "No stylists found. Please add stylists in Settings.",
                )
                return

            output_dir = self.config_manager.get_output_directory()

            writer = RevenueTemplateWriter(output_directory=output_dir)
            service = RevenueTemplateService(writer=writer)

            service.generate(
                month=month,
                year=year,
                stylists=stylists,
                employees=employees,
                payment_methods=payment_methods,
            )

            self.status_label.setText(
                f"Generated Revenue_{month}_{year}.xlsx successfully!"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate sheet:\n{str(e)}")
            self.status_label.setText("Generation failed.")

    def _on_generate_salaries(self):
        """Generate salaries sheet only."""
        year = self.year_spin.value()
        month = self.month_spin.value()

        try:
            employees = self.config_manager.get_employees()
            stylists = self.config_manager.get_stylists()

            if not employees:
                QMessageBox.warning(
                    self,
                    "No Employees",
                    "No employees found. Please add employees in Settings.",
                )
                return

            output_dir = self.config_manager.get_output_directory()

            # Ask user for attendance file path
            from PySide6.QtWidgets import QFileDialog

            attendance_file_path, _ = QFileDialog.getOpenFileName(
                self, "Select Attendance File", output_dir, "Excel Files (*.xlsx)"
            )

            if not attendance_file_path:
                self.status_label.setText("Salaries generation cancelled.")
                return

            writer = SalariesTemplateWriter(output_directory=output_dir)
            service = SalaryTemplateService(writer=writer)

            service.generate(
                month=month,
                year=year,
                employees=employees,
                stylists=stylists,
                attendance_file_path=attendance_file_path,
            )

            self.status_label.setText(
                f"Generated Salaries_{month}_{year}.xlsx successfully!"
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Failed to generate salaries:\n{str(e)}"
            )
            self.status_label.setText("Generation failed.")

    def _open_settings(self):
        settings_window = SettingsWindow(self.config_manager, parent=self)
        settings_window.exec()
