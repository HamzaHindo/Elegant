from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from domain.employee import Employee, Stylist


@dataclass
class RevenueTemplate:
    month: int
    year: int
    days: list[date]
    stylists: list[Stylist]
    employees: list[Employee]  # list of Employee objects
    payment_methods: list[str]
