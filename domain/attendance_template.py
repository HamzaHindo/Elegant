from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .employee import Employee, Stylist


@dataclass
class AttendanceTemplate:
    month: int
    year: int
    employees: list[Employee]
    stylists: list[Stylist]
    days: list[date]
