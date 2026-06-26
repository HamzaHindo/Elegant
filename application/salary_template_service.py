"""
Salary Template Service - Business logic for generating salary sheets.
"""

from domain.salary_template import SalaryTemplate
from infrastructure.salaries_template_writer import SalariesTemplateWriter


class SalaryTemplateService:
    """Service for generating salary templates."""

    def __init__(self, writer: SalariesTemplateWriter):
        """
        Initialize the salary template service.

        Args:
            writer: SalariesTemplateWriter instance
        """
        self.writer = writer

    def generate(
        self,
        month: int,
        year: int,
        employees,
        stylists,
        attendance_file_path: str,
        borrows_file_path: str,
        use_month_folder: bool = False,
    ):
        """
        Generate a salary sheet.

        Args:
            month: Month number (1-12)
            year: Year number
            employees: List of Employee objects
            stylists: List of Stylist objects
            attendance_file_path: Path to the attendance Excel file
            use_month_folder: If True, saves to a month folder
        """
        template = SalaryTemplate(
            month=month,
            year=year,
            employees=employees,
            stylists=stylists,
            attendance_file_path=attendance_file_path,
            borrows_file_path=borrows_file_path,
        )

        self.writer.write(template, use_month_folder=use_month_folder)
