import calendar
import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

from application.attendance_template_service import AttendanceTemplateService
from application.revenue_template_service import RevenueTemplateService
from application.salary_template_service import SalaryTemplateService
from domain.attendance_template import AttendanceTemplate
from domain.revenue_template import RevenueTemplate
from domain.salary_template import SalaryTemplate
from infrastructure.attendance_template_writer import AttendanceTemplateWriter
from infrastructure.config_manager import ConfigManager
from infrastructure.file_manager import FileManager
from infrastructure.revenue_template_writer import RevenueTemplateWriter
from infrastructure.salaries_template_writer import SalariesTemplateWriter
from presentation.windows.settings_window import SettingsWindow
from utils.calendar_utils import get_arabic_month


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Elegant Barbershop")
        self.root.geometry("500x350")
        self.root.resizable(False, False)

        self.config_manager = ConfigManager()

        self._build_ui()

    def _build_ui(self):
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(
            main_frame, text="Monthly Reports Generator", font=("Arial", 14, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 15))

        # Year and Month inputs
        ttk.Label(main_frame, text="Year:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.year_spin = tk.Spinbox(main_frame, from_=2000, to=2100, width=10)
        self.year_spin.delete(0, tk.END)
        self.year_spin.insert(0, "2026")
        self.year_spin.grid(row=1, column=1, sticky=tk.W, padx=5)

        ttk.Label(main_frame, text="Month:").grid(row=1, column=2, sticky=tk.W, padx=5)
        self.month_spin = tk.Spinbox(main_frame, from_=1, to=12, width=10)
        self.month_spin.delete(0, tk.END)
        self.month_spin.insert(0, "1")
        self.month_spin.grid(row=1, column=3, sticky=tk.W, padx=5)

        # Generate all button (main button)
        self.generate_all_btn = ttk.Button(
            main_frame,
            text="Generate All Reports (Attendance + Revenue + Salaries)",
            command=self._on_generate_all,
        )
        self.generate_all_btn.grid(
            row=2, column=0, columnspan=4, pady=(15, 10), sticky=(tk.W, tk.E)
        )

        # Individual generate buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=4, pady=5, sticky=(tk.W, tk.E))

        self.generate_attendance_btn = ttk.Button(
            button_frame, text="Attendance Only", command=self._on_generate_attendance
        )
        self.generate_attendance_btn.grid(row=0, column=0, padx=5, sticky=(tk.W, tk.E))

        self.generate_revenue_btn = ttk.Button(
            button_frame, text="Revenue Only", command=self._on_generate_revenue
        )
        self.generate_revenue_btn.grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))

        self.generate_salaries_btn = ttk.Button(
            button_frame, text="Salaries Only", command=self._on_generate_salaries
        )
        self.generate_salaries_btn.grid(row=0, column=2, padx=5, sticky=(tk.W, tk.E))

        # Configure button frame columns to expand equally
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)

        # Status label
        self.status_label = ttk.Label(main_frame, text="", foreground="green")
        self.status_label.grid(row=4, column=0, columnspan=4, pady=10)

        # Settings button
        self.settings_btn = ttk.Button(
            main_frame, text="Settings", command=self._open_settings
        )
        self.settings_btn.grid(row=5, column=0, columnspan=4, pady=(5, 0))

        # Configure main frame to expand
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.columnconfigure(3, weight=1)

    def _on_generate_all(self):
        """Generate all three reports (Attendance, Revenue, Salaries) in a month folder."""
        year = int(self.year_spin.get())
        month = int(self.month_spin.get())

        try:
            employees = self.config_manager.get_employees()
            stylists = self.config_manager.get_stylists()
            payment_methods = self.config_manager.get_payment_methods()

            if not employees:
                messagebox.showwarning(
                    "No Employees",
                    "No employees found. Please add employees in Settings.",
                )
                return

            if not stylists:
                messagebox.showwarning(
                    "No Stylists", "No stylists found. Please add stylists in Settings."
                )
                return

            output_dir = self.config_manager.get_output_directory()

            self.status_label.config(text="Generating reports...")
            self.root.update()

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

            self.status_label.config(
                text=f"✅ All reports generated successfully in folder: {month_name}/"
            )

            messagebox.showinfo(
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
            messagebox.showerror(
                "Error",
                f"Failed to generate reports:\n{str(e)}\n\nDetails:\n{error_details}",
            )
            self.status_label.config(text="Generation failed.", foreground="red")

    def _on_generate_attendance(self):
        year = int(self.year_spin.get())
        month = int(self.month_spin.get())

        try:
            employees = self.config_manager.get_employees()
            stylists = self.config_manager.get_stylists()

            if not employees:
                messagebox.showwarning(
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

            self.status_label.config(
                text=f"Generated Attendance_{month}_{year}.xlsx successfully!",
                foreground="green",
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate sheet:\n{str(e)}")
            self.status_label.config(text="Generation failed.", foreground="red")

    def _on_generate_revenue(self):
        year = int(self.year_spin.get())
        month = int(self.month_spin.get())

        try:
            stylists = self.config_manager.get_stylists()
            employees = self.config_manager.get_employees()
            payment_methods = self.config_manager.get_payment_methods()

            if not stylists:
                messagebox.showwarning(
                    "No Stylists", "No stylists found. Please add stylists in Settings."
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

            self.status_label.config(
                text=f"Generated Revenue_{month}_{year}.xlsx successfully!",
                foreground="green",
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate sheet:\n{str(e)}")
            self.status_label.config(text="Generation failed.", foreground="red")

    def _on_generate_salaries(self):
        """Generate salaries sheet only."""
        year = int(self.year_spin.get())
        month = int(self.month_spin.get())

        try:
            employees = self.config_manager.get_employees()
            stylists = self.config_manager.get_stylists()

            if not employees:
                messagebox.showwarning(
                    "No Employees",
                    "No employees found. Please add employees in Settings.",
                )
                return

            output_dir = self.config_manager.get_output_directory()

            # Ask user for attendance file path
            from tkinter import filedialog

            attendance_file_path = filedialog.askopenfilename(
                title="Select Attendance File",
                initialdir=output_dir,
                filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
            )

            if not attendance_file_path:
                self.status_label.config(
                    text="Salaries generation cancelled.", foreground="orange"
                )
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

            self.status_label.config(
                text=f"Generated Salaries_{month}_{year}.xlsx successfully!",
                foreground="green",
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate salaries:\n{str(e)}")
            self.status_label.config(text="Generation failed.", foreground="red")

    def _open_settings(self):
        settings_window = SettingsWindow(self.root, self.config_manager)
