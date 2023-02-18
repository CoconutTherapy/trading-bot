from dateutil.relativedelta import relativedelta


def add_months(source_date, months):
    return source_date + relativedelta(months=months)
