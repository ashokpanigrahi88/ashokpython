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
    l_registration = registration
    for key, value in l_registration.items():
        if company != key:
            if plate in [x for v in l_registration.values() for x in v]:
                try:
                    l_registration[key].remove(plate)
                except ValueError:
                    a = 0

    for key, value in l_registration.items():
        if company == key:
            if plate not in [x for v in l_registration.values() for x in v]:
                l_registration[key].append(plate)

    return l_registration


register_car({'Stark Industries': ['IRNMN']}, 'Stark Industries', 'JARVIS')
register_car({'Stark Industries': ['IRNMN']}, 'Wayne Enterprises', 'IMBTMN')
register_car({'X': []}, 'X', 'A')
register_car({'X': [], 'Y': ['A']}, 'X', 'A')
register_car({'Stark Industries': ['IRNMN']}, 'Stark Industries', 'JARVIS')


def occupancy(parking_data, cutoff_time=None):
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

    l_entry = parking_data[0]
    l_exit = parking_data[1]
    l_time = cutoff_time
    l_entered = {}
    l_plates = list([])

    if l_time is None:
        l_time = datetime.datetime.now()
    for entry in l_entry:
        print(entry)
        for i in entry:
            print(i)
            l_entrytime = entry[0]
            l_plate = entry[1]
            if l_plate not in l_entered:
                l_entered[l_plate] = [l_entrytime]
                print(l_entered)

    for exits in l_exit:
        print(exit)
        for i in exits:
            print("exit {}".format(i))
            l_exittime = exits[0]
            l_plate = exits[1]
        if l_plate not in l_entered:
            l_entered[l_plate] = [l_exittime]
        else:
            l_entered[l_plate].append(l_exittime)

    for key, value in l_entered.items():
        print(key)
        for index,val in enumerate(value):
            if index % 2 == 0:
                l_entry = value[index]
                try:
                    l_exit = value[index+1]
                except IndexError:
                    l_exit = datetime.datetime.now()
                print(l_entry, l_exit)
    if l_exit != [] and l_exit >= l_time:
        l_plates.append(key)

    return l_plates


data = ([(datetime.datetime(2017, 12, 12,  7, 13, 44, 0), 'LR10GHT')], [])
cutoff_time = datetime.datetime(2000, 1, 3, 12, 0)
occupancy(data, cutoff_time)
data = ([(datetime.datetime(2017, 12, 12,  7, 13, 44, 0), 'LR10GHT')], [])
cutoff_time = datetime.datetime(2000, 1, 3, 12, 0)
occupancy(data, cutoff_time)


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
    l_entry = parking_data[0]
    l_exit = parking_data[1]
    l_seconds = 0
    l_enttime = None
    l_exittime = None
    for l_company, l_plate in company_registration.items():
        if l_company != company:
            break  # do not continue
        l_plates = [x for x in l_plate]
        for plate in l_plates:
            for t in l_entry:
                l_ent = list(t)
                if plate in l_ent[1]:
                    l_enttime = l_ent[0]
                else:
                    l_enttime = None
            for e in l_exit:
                l_ex = list(e)
                if plate in l_ex:
                    l_exittime = l_ent[0]
                else:
                    l_exittime = None
        if (l_enttime is None or l_exittime is None):
            return l_seconds
        else:
            l_seconds = (l_exittime - l_enttime).seconds

    return l_seconds


parking_data = ([(datetime.datetime(2000, 1, 1, 12, 0), 'LR10GHT')],
[(datetime.datetime(2000, 1, 2, 12, 0), 'LR10GHT')])
start_time = datetime.datetime(2000, 1, 3, 12, 0)
end_time = datetime.datetime(2000, 1, 3, 12, 0)
company_registration = {'Shire Tobacco Inc.': ['LR10GHT']}
company_bill(parking_data, company_registration, 'Shire Tobacco Inc.', start_time, end_time)

parking_data = ([(datetime.datetime(2000, 1, 1, 12, 0), 'LR10GHT')],
    [(datetime.datetime(2000, 1, 2, 12, 0), 'LR10GHT')])
start_time = datetime.datetime(2000, 1, 3, 12, 0)
end_time = datetime.datetime(2000, 1, 3, 12, 0)
company_registration = {'Shire Tobacco Inc.': ['LR10GHT']}
company_bill(parking_data, company_registration, 'Shire Tobacco Inc.', start_time, end_time)

parking_data = ([(datetime.datetime(2000, 1, 1, 12, 0), 'LR10GHT')], [])
start_time = datetime.datetime(2000, 1, 3, 12, 0)
end_time = datetime.datetime(2000, 1, 3, 12, 0)
company_registration = {'Shire Tobacco Inc.': ['LR10GHT']}
company_bill(parking_data, company_registration, 'Shire Tobacco Inc.', start_time, end_time)

parking_data = ([(datetime.datetime(2000, 1, 1, 12, 0), 'LR10GHT'), (datetime.datetime(2000, 1, 2, 12, 0), 'LR10GHT'), (datetime.datetime(2000, 1, 3, 12, 0), 'LR10GHT')], [(datetime.datetime(2000, 1, 1, 12, 1), 'LR10GHT'), (datetime.datetime(2000, 1, 2, 12, 1), 'LR10GHT'), (datetime.datetime(2000, 1, 3, 12, 1), 'LR10GHT')])
start_time = datetime.datetime(2000, 1, 3, 12, 0)
end_time = datetime.datetime(2000, 1, 3, 12, 0)
company_registration = {'Shire Tobacco Inc.': ['LR10GHT']}
company_bill(parking_data, company_registration, 'Shire Tobacco Inc.', start_time, end_time)
