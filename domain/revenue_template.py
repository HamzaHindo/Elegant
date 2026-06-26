from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import List

from domain.employee import Employee, Stylist


@dataclass
class RevenueTemplate:
    month: int
    year: int
    days: List[date]
    stylists: List[Stylist]
    employees: List[Employee]  # list of Employee objects
    payment_methods: List[str]
