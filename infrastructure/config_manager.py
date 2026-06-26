import os

import yaml

from domain.employee import Employee
from domain.revenue_template import Stylist


class ConfigManager:
    def __init__(self, config_path="configs/config.yaml"):
        self.config_path = config_path
        self._config = None

    def _ensure_config_exists(self):
        if not os.path.exists(self.config_path):
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            self._config = {
                "output_directory": "./output",
                "employees": [],
            }
            self.save()

    def load(self):
        self._ensure_config_exists()
        with open(self.config_path, "r", encoding="utf-8") as f:
            self._config = yaml.safe_load(f) or {}
        return self._config

    def save(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.dump(self._config, f, allow_unicode=True, sort_keys=False)

    def get_engine(self):
        if self._config is None:
            self.load()
        return self._config.get("engine", "./excel")

    def get_output_directory(self):
        if self._config is None:
            self.load()
        return self._config.get("output_directory", "./output")

    def set_output_directory(self, directory):
        if self._config is None:
            self.load()
        self._config["output_directory"] = directory
        self.save()

    def get_employees(self):
        if self._config is None:
            self.load()
        employees_data = self._config.get("employees", [])
        return [
            Employee(
                name=emp["name"],
                daily_rate=emp["daily_rate"],
                working_hours=emp["working_hours"],
            )
            for emp in employees_data
        ]

    def set_employees(self, employees):
        if self._config is None:
            self.load()
        self._config["employees"] = [
            {
                "name": emp.name,
                "daily_rate": emp.daily_rate,
                "working_hours": emp.working_hours,
            }
            for emp in employees
        ]
        self.save()

    def get_stylists(self):
        if self._config is None:
            self.load()
        stylists_data = self._config.get("stylists", [])
        return [
            Stylist(
                name=s["name"],
                daily_target=s["daily_target"],
                daily_rate=s["daily_rate"],
                working_hours=s["working_hours"],
            )
            for s in stylists_data
        ]

    def set_stylists(self, stylists):
        if self._config is None:
            self.load()
        self._config["stylists"] = [
            {
                "name": s.name,
                "daily_target": s.daily_target,
                "daily_rate": s.daily_rate,
                "working_hours": s.working_hours,
            }
            for s in stylists
        ]
        self.save()

    def get_payment_methods(self):
        if self._config is None:
            self.load()
        return self._config.get("payment_methods", ["فيزا", "كاش"])

    def set_payment_methods(self, payment_methods):
        if self._config is None:
            self.load()
        self._config["payment_methods"] = payment_methods
        self.save()
