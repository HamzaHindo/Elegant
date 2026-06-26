import calendar
from datetime import date

from domain.revenue_template import RevenueTemplate
from infrastructure.revenue_template_writer import RevenueTemplateWriter


class RevenueTemplateService:
    def __init__(self, writer: RevenueTemplateWriter):
        self.writer = writer

    def _generate_days(self, year, month):
        num_days = calendar.monthrange(year, month)[1]
        return [date(year, month, day) for day in range(1, num_days + 1)]

    def generate(self, month, year, stylists, employees, payment_methods):
        days = self._generate_days(year, month)

        template = RevenueTemplate(
            month=month,
            year=year,
            days=days,
            stylists=stylists,
            employees=employees,
            payment_methods=payment_methods,
        )

        self.writer.write(template)
