from calendar import monthrange
from datetime import date, timedelta


def to_arabic_ordinal(n: int) -> str:
    ordinals = {
        1: "الأول",
        2: "الثاني",
        3: "الثالث",
        4: "الرابع",
        5: "الخامس",
        6: "السادس",
        7: "السابع",
        8: "الثامن",
        9: "التاسع",
        10: "العاشر",
        11: "الحادي عشر",
        12: "الثاني عشر",
    }

    return ordinals.get(n, str(n))


def get_arabic_month(x: int):
    arabic_months = [
        "يناير",
        "فبراير",
        "مارس",
        "أبريل",
        "مايو",
        "يونيو",
        "يوليو",
        "أغسطس",
        "سبتمبر",
        "أكتوبر",
        "نوفمبر",
        "ديسمبر",
    ]

    return arabic_months[x - 1]


def get_weeks(year: int, month: int):
    days_in_month = monthrange(year, month)[1]

    first_day = date(year, month, 1)

    weeks = []

    current_week = []
    current_date = first_day

    while current_date.month == month:
        current_week.append(current_date.day)

        # Saturday == 5
        if current_date.weekday() == 5:
            weeks.append(current_week)
            current_week = []

        current_date += timedelta(days=1)

    if current_week:
        weeks.append(current_week)

    return weeks
