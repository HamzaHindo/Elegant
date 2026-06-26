import calendar
from datetime import date

from domain.attendance_template import AttendanceTemplate
from infrastructure.attendance_template_writer import AttendanceTemplateWriter


class AttendanceTemplateService:
    def __init__(self, writer: AttendanceTemplateWriter):
        self.writer = writer

    def _generate_days(self, year, month):
        num_days = calendar.monthrange(year, month)[1]

        return [date(year, month, day) for day in range(1, num_days + 1)]

    def generate(self, month, stylists, year, employees):

        days = self._generate_days(year, month)

        template = AttendanceTemplate(
            month=month, year=year, employees=employees, days=days, stylists=stylists
        )

        self.writer.write(template)
