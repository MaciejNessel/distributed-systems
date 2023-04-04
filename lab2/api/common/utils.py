import calendar
from datetime import datetime, timedelta


def get_last_weekend_dates():
    current_date = datetime.today().strftime("%Y-%m-%d")
    last_weekend = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")
    return last_weekend, current_date


def get_last_decade():
    current_date = (datetime.today() - timedelta(days=7)).strftime("%Y-%m-%d")
    last_weekend = (datetime.today() - timedelta(days=365 * 10 + 7)).strftime("%Y-%m-%d")
    return last_weekend, current_date


def validate_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    today = datetime.now().date()
    return date_obj <= today


def get_month_name(id: int):
    if 0 < id < 13:
        return calendar.month_name[id]
    else:
        return None
