from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import List

from .employee import Employee, Stylist


@dataclass
class AttendanceTemplate:
    month: int
    year: int
    employees: List[Employee]
    stylists: List[Stylist]
    days: List[date]
