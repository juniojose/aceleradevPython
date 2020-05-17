from datetime import datetime
from math import trunc

records = [
    {'source': '48-996355555', 'destination': '48-666666666',
     'end': 1564610974, 'start': 1564610674},
    {'source': '41-885633788', 'destination': '41-886383097',
     'end': 1564506121, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-886383097',
     'end': 1564630198, 'start': 1564629838},
    {'source': '48-999999999', 'destination': '41-885633788',
     'end': 1564697158, 'start': 1564696258},
    {'source': '41-833333333', 'destination': '41-885633788',
     'end': 1564707276, 'start': 1564704317},
    {'source': '41-886383097', 'destination': '48-996384099',
     'end': 1564505621, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '48-996383697',
     'end': 1564505721, 'start': 1564504821},
    {'source': '41-885633788', 'destination': '48-996384099',
     'end': 1564505721, 'start': 1564504821},
    {'source': '48-996355555', 'destination': '48-996383697',
     'end': 1564505821, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '41-886383097',
     'end': 1564610750, 'start': 1564610150},
    {'source': '48-996383697', 'destination': '41-885633788',
     'end': 1564505021, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-885633788',
     'end': 1564627800, 'start': 1564626000}
]


def calculate_tax(call_start, call_end):
    # Calls are sorted by source line number;
    # The call duration each is defined in unfractionated minutes;
    # The total call time is multiplied by the rate according
    #  to each period (day / night).
    #
    # Parameters:
    #
    # call_start: call start timestamp.
    # fim_ligacao: call end timestamp.
    #
    # Constants:
    #
    # PERMANENT_CHARGE: fixed charges are used to pay the connection cost.
    # DAILY_CONNECTION_RATE: The charge applies to each completed
    #  60-second cycle and there is no fractional charge.
    #
    # NIGHT_CONNECTION_RATE: At night (22h | 6h) tax is zero.

    PERMANENT_CHARGE = 0.36
    DAILY_CONNECTION_RATE = 0.09
    NIGHT_CONNECTION_RATE = 0

    call_start_date = datetime.fromtimestamp(call_start)
    call_end_date = datetime.fromtimestamp(call_end)

    # Checks if call start is between 6h (inclusive) and 22h
    if 6 <= call_start_date.hour < 22:
        # Check if call end date exceeded 22h
        if call_end_date.hour > 22:
            # Set the call end time to 22h to calculate the tax will pay
            call_end_date = datetime(
                call_end_date.year,
                call_end_date.month,
                call_end_date.day, 22)

        tax = DAILY_CONNECTION_RATE

    # Checks if call end is between 22h (inclusive) and 6h
    elif call_end_date.hour >= 22 or call_end_date.hour < 6:
        tax = NIGHT_CONNECTION_RATE

    # Set the call start time to 6h to calculate the tax will pay
    else:
        call_start_date = datetime(
            call_start_date.year,
            call_start_date.month,
            call_start_date.day, 6)

    total_minutes = (call_end_date - call_start_date).seconds / 60
    total_minutes = trunc(total_minutes)

    call_total_cost = (total_minutes * tax) + PERMANENT_CHARGE

    return call_total_cost


def classify_by_phone_number(records):
    # Sorts calls by number and generates a report with payable total
    # Parameter records: a dictionary list with calls data
    #
    # Phone numbers groups by call rate calculations
    results = {}
    # List with phone numbers and total to pay
    report = []

    # Calculates the tax on each call and totals amount to be paid
    for record in records:
        if record['source'] not in results:
            results[record['source']] = calculate_tax(
                record['start'], record['end'])
        else:
            results[record['source']] += calculate_tax(
                record['start'], record['end'])

    results = sorted(results.items(), key=lambda value: value[1], reverse=True)

    # Phone bill dictionary list with total to be paid
    for result in results:
        report.append({'source': result[0], 'total': round(result[1], 2)})

    return report
