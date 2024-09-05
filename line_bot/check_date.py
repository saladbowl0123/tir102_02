import datetime

SEPS = ['-', '/', '.']
OLDEST = datetime.date(year=1995, month=6, day=16)

def find_sep(date_str):
    # check for delimiters '-', '/', '.'
    for sep in SEPS:
        if sep in date_str:
            return sep

def split_into_ymd(date_str, sep):
    # should return list of 3 ints: year, month, date
    return list(map(int, date_str.split(sep=sep)))

def check_date(date_str):
    try:
        sep = find_sep(date_str)
        year, month, day = split_into_ymd(date_str, sep)
        date = datetime.date(year=year, month=month, day=day)
    except:
        return None

    return date

def is_in_range(date):
    # oldest entry dated 1995-06-16: https://apod.nasa.gov/apod/ap950616.html
    return date >= OLDEST

def today():
    return datetime.date.today()
