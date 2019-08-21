from datetime import datetime


def get_year():
    return datetime.now().year % 100


def get_month():
    return datetime.now().month


def get_day():
    return datetime.now().day


def get_date():
    return datetime.now().strftime('%Y-%m-%d')[2:]
