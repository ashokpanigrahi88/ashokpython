# PARKING MANAGEMENT #
#
import datetime
#
# For insurance purposes, the management of an office building is required to
# maintain, at all time, an accurate list of all the vehicles in the dedicated
# parking. In addition, for billing the different companies, the office
# building management wants to record occupation of the parking at different
# times and automatically emit bills to each specific companies.
#
# You are tasked with completing the series of functions below that fill the
# need of the office building parking management. You are allowed (and
# encouraged) to create additional, intermediate functions.
#
# The main data structure that your suite of function handles is a record of
# entrances and exits. A sample is given below. It consist of a pair of lists
# of tuples. The first list gives the timestamps and license plate number of
# vehicles entering the parking, the second exiting.
#
# DO NOT MODIFY CONSTANTS
PARKING_DATA_SAMPLE = ([
    (datetime.datetime(2017, 12, 12, 7, 13, 44, 0), 'LR10GHT'),
    (datetime.datetime(2017, 12, 12, 7, 13, 48, 0), 'LC11FBF'),
    (datetime.datetime(2017, 12, 12, 7, 13, 59, 0), 'LR10ZPP'),
    (datetime.datetime(2017, 12, 12, 7, 15, 2, 0), 'LJ65OSN'),
    (datetime.datetime(2017, 12, 12, 7, 15, 22, 0), 'LA63EWH'),
    (datetime.datetime(2017, 12, 12, 13, 1, 42, 0), 'LC11FBF')
], [(datetime.datetime(2017, 12, 12, 12, 13, 1, 0), 'LC11FBF'),
    (datetime.datetime(2017, 12, 12, 16, 42, 10, 0), 'LR10ZPP'),
    (datetime.datetime(2017, 12, 12, 17, 2, 41, 0), 'LR10GHT'),
    (datetime.datetime(2017, 12, 12, 17, 2, 58, 0), 'LA63EWH'),
    (datetime.datetime(2017, 12, 12, 17, 4, 3, 0), 'LJ65OSN'),
    (datetime.datetime(2017, 12, 12, 17, 10, 21, 0), 'LC11FBF')])
#
# A secondary data structure includes billing information. It is a dictionary
# that maps company names to a list of registered license plates.
#
# DO NOT MODIFY CONSTANTS
COMPANY_REGISTRATIONS_SAMPLE = {
    'Shire Tobacco Inc.': ['LR10GHT', 'LA63EWH'],
    'Rohan Equestrian Equipments': [],
    'Moria Construction Hardware': ['LC11FBF', 'LS66XKE', 'LR10ZPP', 'LJ65OSN']
}


def _update_one_company(is_company, plate, plates):
    """
    This function update the plates depending
    on whether is_company is True or False.
    :param is_company:
    :param plate:
    :param plates:
    :return:
    :rtype:
    """

    has_plate = plate in plates

    if is_company and has_plate:
        return plates
    elif is_company and not has_plate:
        return plates + [plate]
    elif not is_company and has_plate:
        return [p for p in plates if p != plate]
    else:
        return plates


def register_car(registration, company, plate):
    """
    Registers a new car.

    NOTE: this function should not modify the registration dictionary that is
    given, instead it should create a new dictionary.
    NOTE: this function should not introduce duplicates in the registration
    system. Specifically, if a car is already registered with the given
    company it should return an identical registration information. If the car
    is registered with a different company it should remove the first
    registration.
    NOTE: if the company is not listed in the dictionary, it should not
    introduce it. Instead it should just return an identical registration.

    E.g., register_car({'Stark Industries': ['IRNMN']}, 'Stark Industries',
                       'JARVIS')
    is {'Stark Industries': ['IRNMN', 'JARVIS']}
    E.g., register_car({'Stark Industries': ['IRNMN']}, 'Wayne Enterprises',
                       'IMBTMN')
    is {'Stark Industries': ['IRNMN']}

    :param registration: preexisting registration information
    :param company: company to register the car for
    :param plate: license plate of the car to register
    :return: new registration information dictionary with added registration
    :rtype: dict
    """

    reg = {
        c: _update_one_company(c == company, plate, ps)
        for (c, ps) in registration.items()
    }
    return reg


def occupancy(parking_data, time=None):
    """
    Computes the occupancy of the parking at a given time. If no time is
    provided, check the current occupancy.

    E.g.,
    data = ([(datetime.datetime(2017, 12, 12,  7, 13, 44, 0), 'LR10GHT')], [])
    occupancy(data, time=datetime.datetime(2017, 12, 12,  7, 13, 45, 0))
    is ['LR10GHT']
    E.g.,
    data = ([(datetime.datetime(2017, 12, 12,  7, 13, 44, 0), 'LR10GHT')], [])
    occupancy(data, time=datetime.datetime(2017, 12, 12,  7, 13, 43, 0))
    is []

    :param parking_data: tuple of list of timestamped arrival and departure
    information including license plate. See sample above.
    :param time: time (as a datetime.datetime object) at which to check for
    occupancy. If no time is provided, use now.
    :return: list of cars present in the parking at the given time.
    :rtype: list
    """

    real_time = time
    if time is None:
        real_time = datetime.datetime.now()
    (arrivals, departures) = parking_data
    # NOTE: we cannot use sets because there can be several
    # arrivals/departures of the same car.
    arrived = [p for (t, p) in arrivals if t < real_time]
    left = [p for (t, p) in departures if t < real_time]
    for car in left:
        arrived.remove(car)
    return arrived


def bill_one_car(start, there, events, ending):
    """
    :param start:
    :param there:
    :param events:
    :param ending:
    :return:
    :rtype:
    """
    if not there and not events:
        return 0
    elif there and not events:
        return (ending - start).total_seconds()
    elif there and events:
        first_slice = (events[0] - start).total_seconds()
        rest = bill_one_car(events[0], False, events[1:], ending)
        return first_slice + rest
    else:
        return bill_one_car(events[0], True, events[1:], ending)


def company_bill(parking_data, company_registration, company, t_start, t_end):
    """
    Computes the total, cumulated time in seconds, ignoring milliseconds, that
    cars registred with a given company stayed in the parking during the
    interval between t_start and t_end.

    E.g.,
    parking_data = (
        [(datetime.datetime(2017, 12, 12,  7, 13, 44, 0), 'LR10GHT')],
        [(datetime.datetime(2017, 12, 12,  7, 13, 45, 0), 'LR10GHT')]
    )
    company_registration = {'Shire Tobacco Inc.': ['LR10GHT']}
    company_bill(parking_data, company_registration,
                 'Shire Tobacco Inc.', …, …)
    is 1

    :param parking_data: see sample above
    :param company_registration: see sample above
    :param company: name of the company to compute billing for
    :param t_start: start of the billing interval
    :param t_end: end of the billing interval
    :return: cumulated number of seconds of car park occupancy
    :rtype: float | int
    """

    registered_cars = company_registration.get(company)
    if registered_cars is None:
        return 0
    total = 0
    occupancy_at_t_start = occupancy(parking_data, t_start)
    for car in registered_cars:
        arrivals = [t for (t, p) in parking_data[0] if p == car]
        departures = [t for (t, p) in parking_data[1] if p == car]
        # This assumes the parking data is well formed (that departures and
        # arrivals alternate)
        events = sorted(arrivals + departures)
        total += bill_one_car(t_start, occupancy_at_t_start, events, t_end)
    return total
