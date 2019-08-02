import datetime


def get_year():
    return datetime.datetime.now().year % 100


def get_month():
    return datetime.datetime.now().month


def get_day():
    return datetime.datetime.now().day
