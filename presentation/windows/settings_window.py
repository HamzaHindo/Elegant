import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from domain.employee import Employee
from domain.revenue_template import Stylist
from infrastructure.config_manager import ConfigManager


class SettingsWindow:
    def __init__(self, parent, config_manager: ConfigManager):
        self.parent = parent
        self.config_manager = config_manager

        # Create top-level window
        self.window = tk.Toplevel(parent)
        self.window.title("Settings")
        self.window.geometry("700x600")
        self.window.transient(parent)
        self.window.grab_set()

        self._build_ui()
        self._load_data()

    def _build_ui(self):
        # Main frame with padding
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Output Directory Section
        dir_frame = ttk.LabelFrame(main_frame, text="Output Directory", padding="5")
        dir_frame.pack(fill=tk.X, pady=(0, 10))

        self.dir_input = ttk.Entry(dir_frame, state="readonly")
        self.dir_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.browse_btn = ttk.Button(
            dir_frame, text="Browse...", command=self._browse_directory
        )
        self.browse_btn.pack(side=tk.RIGHT)

        # Employees Section
        employees_frame = ttk.LabelFrame(main_frame, text="Employees", padding="5")
        employees_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Employees table
        employees_table_frame = ttk.Frame(employees_frame)
        employees_table_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbars for employees table
        employees_scroll_y = ttk.Scrollbar(employees_table_frame, orient=tk.VERTICAL)
        employees_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        employees_scroll_x = ttk.Scrollbar(employees_table_frame, orient=tk.HORIZONTAL)
        employees_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.employees_table = ttk.Treeview(
            employees_table_frame,
            columns=("name", "working_hours", "daily_rate"),
            show="headings",
            yscrollcommand=employees_scroll_y.set,
            xscrollcommand=employees_scroll_x.set,
            height=6,
        )

        employees_scroll_y.config(command=self.employees_table.yview)
        employees_scroll_x.config(command=self.employees_table.xview)

        self.employees_table.heading("name", text="Name")
        self.employees_table.heading("working_hours", text="Working Hours")
        self.employees_table.heading("daily_rate", text="Daily Rate")

        self.employees_table.column("name", width=200)
        self.employees_table.column("working_hours", width=100)
        self.employees_table.column("daily_rate", width=100)

        self.employees_table.pack(fill=tk.BOTH, expand=True)

        # Buttons for employees
        employees_btn_frame = ttk.Frame(employees_frame)
        employees_btn_frame.pack(fill=tk.X, pady=(5, 0))

        self.add_employee_btn = ttk.Button(
            employees_btn_frame, text="Add Employee", command=self._add_employee
        )
        self.add_employee_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.edit_employee_btn = ttk.Button(
            employees_btn_frame, text="Edit Selected", command=self._edit_employee
        )
        self.edit_employee_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.remove_employee_btn = ttk.Button(
            employees_btn_frame, text="Remove Selected", command=self._remove_employee
        )
        self.remove_employee_btn.pack(side=tk.LEFT)

        # Stylists Section
        stylists_frame = ttk.LabelFrame(main_frame, text="Stylists", padding="5")
        stylists_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Stylists table
        stylists_table_frame = ttk.Frame(stylists_frame)
        stylists_table_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbars for stylists table
        stylists_scroll_y = ttk.Scrollbar(stylists_table_frame, orient=tk.VERTICAL)
        stylists_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        stylists_scroll_x = ttk.Scrollbar(stylists_table_frame, orient=tk.HORIZONTAL)
        stylists_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.stylists_table = ttk.Treeview(
            stylists_table_frame,
            columns=("name", "daily_target", "daily_rate", "working_hours"),
            show="headings",
            yscrollcommand=stylists_scroll_y.set,
            xscrollcommand=stylists_scroll_x.set,
            height=6,
        )

        stylists_scroll_y.config(command=self.stylists_table.yview)
        stylists_scroll_x.config(command=self.stylists_table.xview)

        self.stylists_table.heading("name", text="Name")
        self.stylists_table.heading("daily_target", text="Daily Target")
        self.stylists_table.heading("daily_rate", text="Daily Rate")
        self.stylists_table.heading("working_hours", text="Working Hours")

        self.stylists_table.column("name", width=150)
        self.stylists_table.column("daily_target", width=100)
        self.stylists_table.column("daily_rate", width=100)
        self.stylists_table.column("working_hours", width=100)

        self.stylists_table.pack(fill=tk.BOTH, expand=True)

        # Buttons for stylists
        stylists_btn_frame = ttk.Frame(stylists_frame)
        stylists_btn_frame.pack(fill=tk.X, pady=(5, 0))

        self.add_stylist_btn = ttk.Button(
            stylists_btn_frame, text="Add Stylist", command=self._add_stylist
        )
        self.add_stylist_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.edit_stylist_btn = ttk.Button(
            stylists_btn_frame, text="Edit Selected", command=self._edit_stylist
        )
        self.edit_stylist_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.remove_stylist_btn = ttk.Button(
            stylists_btn_frame, text="Remove Selected", command=self._remove_stylist
        )
        self.remove_stylist_btn.pack(side=tk.LEFT)

        # Save / Cancel buttons
        actions_frame = ttk.Frame(main_frame)
        actions_frame.pack(fill=tk.X)

        self.save_btn = ttk.Button(
            actions_frame, text="Save", command=self._save_settings
        )
        self.save_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.cancel_btn = ttk.Button(
            actions_frame, text="Cancel", command=self.window.destroy
        )
        self.cancel_btn.pack(side=tk.LEFT)

    def _load_data(self):
        config = self.config_manager.load()

        # Load output directory
        output_dir = config.get("output_directory", "./output")
        self.dir_input.config(state="normal")
        self.dir_input.delete(0, tk.END)
        self.dir_input.insert(0, output_dir)
        self.dir_input.config(state="readonly")

        # Load employees
        employees = config.get("employees", [])
        for emp in employees:
            self.employees_table.insert(
                "",
                tk.END,
                values=(
                    emp.get("name", ""),
                    emp.get("working_hours", ""),
                    emp.get("daily_rate", ""),
                ),
            )

        # Load stylists
        stylists = config.get("stylists", [])
        for s in stylists:
            self.stylists_table.insert(
                "",
                tk.END,
                values=(
                    s.get("name", ""),
                    s.get("daily_target", ""),
                    s.get("daily_rate", ""),
                    s.get("working_hours", ""),
                ),
            )

    def _browse_directory(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.dir_input.config(state="normal")
            self.dir_input.delete(0, tk.END)
            self.dir_input.insert(0, directory)
            self.dir_input.config(state="readonly")

    def _add_employee(self):
        dialog = EmployeeDialog(self.window, "Add Employee")
        if dialog.result:
            name, working_hours, daily_rate = dialog.result
            self.employees_table.insert(
                "", tk.END, values=(name, working_hours, daily_rate)
            )

    def _edit_employee(self):
        selected = self.employees_table.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an employee to edit.")
            return

        item = selected[0]
        values = self.employees_table.item(item, "values")

        dialog = EmployeeDialog(
            self.window,
            "Edit Employee",
            initial_values=(values[0], values[1], values[2]),
        )
        if dialog.result:
            name, working_hours, daily_rate = dialog.result
            self.employees_table.item(item, values=(name, working_hours, daily_rate))

    def _remove_employee(self):
        selected = self.employees_table.selection()
        if not selected:
            messagebox.showwarning(
                "No Selection", "Please select an employee to remove."
            )
            return

        for item in selected:
            self.employees_table.delete(item)

    def _add_stylist(self):
        dialog = StylistDialog(self.window, "Add Stylist")
        if dialog.result:
            name, daily_target, daily_rate, working_hours = dialog.result
            self.stylists_table.insert(
                "", tk.END, values=(name, daily_target, daily_rate, working_hours)
            )

    def _edit_stylist(self):
        selected = self.stylists_table.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a stylist to edit.")
            return

        item = selected[0]
        values = self.stylists_table.item(item, "values")

        dialog = StylistDialog(
            self.window,
            "Edit Stylist",
            initial_values=(values[0], values[1], values[2], values[3]),
        )
        if dialog.result:
            name, daily_target, daily_rate, working_hours = dialog.result
            self.stylists_table.item(
                item, values=(name, daily_target, daily_rate, working_hours)
            )

    def _remove_stylist(self):
        selected = self.stylists_table.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a stylist to remove.")
            return

        for item in selected:
            self.stylists_table.delete(item)

    def _save_settings(self):
        output_dir = self.dir_input.get().strip()
        if not output_dir:
            messagebox.showwarning(
                "Validation Error", "Output directory is required."
            )
            return

        # Collect employees
        employees = []
        for item in self.employees_table.get_children():
            values = self.employees_table.item(item, "values")
            name = values[0].strip()
            hours_str = values[1]
            rate_str = values[2]

            if not name:
                messagebox.showwarning(
                    "Validation Error", "All employees must have a name."
                )
                return

            try:
                hours = int(hours_str)
            except ValueError:
                messagebox.showwarning(
                    "Validation Error",
                    f"Invalid working hours for employee '{name}'.",
                )
                return

            try:
                rate = int(rate_str)
            except ValueError:
                messagebox.showwarning(
                    "Validation Error", f"Invalid daily rate for employee '{name}'."
                )
                return

            employees.append(Employee(name=name, working_hours=hours, daily_rate=rate))

        # Collect stylists
        stylists = []
        for item in self.stylists_table.get_children():
            values = self.stylists_table.item(item, "values")
            name = values[0].strip()
            target_str = values[1]
            rate_str = values[2]
            hours_str = values[3]

            if not name:
                messagebox.showwarning(
                    "Validation Error", "All stylists must have a name."
                )
                return

            try:
                target = int(target_str)
            except ValueError:
                messagebox.showwarning(
                    "Validation Error", f"Invalid daily target for stylist '{name}'."
                )
                return

            try:
                rate = int(rate_str)
            except ValueError:
                messagebox.showwarning(
                    "Validation Error", f"Invalid daily rate for stylist '{name}'."
                )
                return

            try:
                hours = int(hours_str)
            except ValueError:
                messagebox.showwarning(
                    "Validation Error", f"Invalid working hours for stylist '{name}'."
                )
                return

            stylists.append(
                Stylist(
                    name=name, daily_target=target, daily_rate=rate, working_hours=hours
                )
            )

        self.config_manager.set_output_directory(output_dir)
        self.config_manager.set_employees(employees)
        self.config_manager.set_stylists(stylists)

        messagebox.showinfo("Success", "Settings saved successfully.")
        self.window.destroy()


class EmployeeDialog:
    def __init__(self, parent, title, initial_values=None):
        self.result = None

        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("350x150")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Create form
        form_frame = ttk.Frame(self.dialog, padding="10")
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Working Hours:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.hours_entry = ttk.Entry(form_frame, width=30)
        self.hours_entry.grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Daily Rate:").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.rate_entry = ttk.Entry(form_frame, width=30)
        self.rate_entry.grid(row=2, column=1, pady=5)

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="OK", command=self._ok).pack(
            side=tk.LEFT, padx=(0, 5)
        )
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(
            side=tk.LEFT
        )

        # Load initial values if provided
        if initial_values:
            self.name_entry.insert(0, initial_values[0])
            self.hours_entry.insert(0, initial_values[1])
            self.rate_entry.insert(0, initial_values[2])
        else:
            self.hours_entry.insert(0, "8")
            self.rate_entry.insert(0, "0")

        self.name_entry.focus()

        # Wait for dialog to close
        self.dialog.wait_window()

    def _ok(self):
        name = self.name_entry.get().strip()
        hours = self.hours_entry.get().strip()
        rate = self.rate_entry.get().strip()

        if not name:
            messagebox.showwarning("Validation Error", "Name is required.")
            return

        try:
            int(hours)
        except ValueError:
            messagebox.showwarning("Validation Error", "Working hours must be a number.")
            return

        try:
            int(rate)
        except ValueError:
            messagebox.showwarning("Validation Error", "Daily rate must be a number.")
            return

        self.result = (name, hours, rate)
        self.dialog.destroy()


class StylistDialog:
    def __init__(self, parent, title, initial_values=None):
        self.result = None

        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("350x180")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Create form
        form_frame = ttk.Frame(self.dialog, padding="10")
        form_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Daily Target:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.target_entry = ttk.Entry(form_frame, width=30)
        self.target_entry.grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Daily Rate:").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.rate_entry = ttk.Entry(form_frame, width=30)
        self.rate_entry.grid(row=2, column=1, pady=5)

        ttk.Label(form_frame, text="Working Hours:").grid(
            row=3, column=0, sticky=tk.W, pady=5
        )
        self.hours_entry = ttk.Entry(form_frame, width=30)
        self.hours_entry.grid(row=3, column=1, pady=5)

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="OK", command=self._ok).pack(
            side=tk.LEFT, padx=(0, 5)
        )
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(
            side=tk.LEFT
        )

        # Load initial values if provided
        if initial_values:
            self.name_entry.insert(0, initial_values[0])
            self.target_entry.insert(0, initial_values[1])
            self.rate_entry.insert(0, initial_values[2])
            self.hours_entry.insert(0, initial_values[3])
        else:
            self.target_entry.insert(0, "1500")
            self.rate_entry.insert(0, "0")
            self.hours_entry.insert(0, "0")

        self.name_entry.focus()

        # Wait for dialog to close
        self.dialog.wait_window()

    def _ok(self):
        name = self.name_entry.get().strip()
        target = self.target_entry.get().strip()
        rate = self.rate_entry.get().strip()
        hours = self.hours_entry.get().strip()

        if not name:
            messagebox.showwarning("Validation Error", "Name is required.")
            return

        try:
            int(target)
        except ValueError:
            messagebox.showwarning("Validation Error", "Daily target must be a number.")
            return

        try:
            int(rate)
        except ValueError:
            messagebox.showwarning("Validation Error", "Daily rate must be a number.")
            return

        try:
            int(hours)
        except ValueError:
            messagebox.showwarning("Validation Error", "Working hours must be a number.")
            return

        self.result = (name, target, rate, hours)
        self.dialog.destroy()
