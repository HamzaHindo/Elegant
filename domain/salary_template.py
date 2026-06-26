"""
Salary Template Domain Model
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from domain.employee import Employee, Stylist


@dataclass
class SalaryTemplate:
    """Template for generating salary sheets."""

    month: int
    year: int
    employees: List[Employee]
    stylists: List[Stylist]
    attendance_file_path: (
        str  # Path to the attendance Excel file to read working days from
    )
    borrows_file_path: str
