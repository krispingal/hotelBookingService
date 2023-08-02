from datetime import date, timedelta, datetime


def parseDate(dateStr: str) -> date:
    return datetime.strptime(dateStr, '%m-%d-%Y').date()


def daterange(start_date: date, end_date: date):
    for n in range(int((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)