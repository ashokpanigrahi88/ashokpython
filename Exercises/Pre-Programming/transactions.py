# TRANSACTIONS ANALYSIS #
#
import datetime
#
# DO NOT MODIFY CONSTANTS
TRANSACTION_LOG_SAMPLE_1 = [{
    'name': 'SKIL',
    'nature': 'buy',
    'quantity': 11,
    'unit-price': 442,
    'time': datetime.time(8, 22, 52, 0)
},
                            {
                                'name': 'DOAA',
                                'nature': 'sell',
                                'quantity': 43,
                                'unit-price': 122,
                                'time': datetime.time(7, 1, 10, 0)
                            },
                            {
                                'name': 'DOAA',
                                'nature': 'sell',
                                'quantity': 2,
                                'unit-price': 119,
                                'time': datetime.time(8, 3, 0, 0)
                            },
                            {
                                'name': 'DOAA',
                                'nature': 'sell',
                                'quantity': 10,
                                'unit-price': 118,
                                'time': datetime.time(8, 3, 41, 0)
                            },
                            {
                                'name': 'DOAA',
                                'nature': 'sell',
                                'quantity': 20,
                                'unit-price': 116,
                                'time': datetime.time(10, 8, 21, 0)
                            },
                            {
                                'name': 'DOAA',
                                'nature': 'sell',
                                'quantity': 11,
                                'unit-price': 113,
                                'time': datetime.time(11, 44, 14, 0)
                            },
                            {
                                'name': 'SKIL',
                                'nature': 'sell',
                                'quantity': 8,
                                'unit-price': 450,
                                'time': datetime.time(11, 22, 22, 0)
                            },
                            {
                                'name': 'SKIL',
                                'nature': 'sell',
                                'quantity': 3,
                                'unit-price': 451,
                                'time': datetime.time(11, 56, 0, 0)
                            }]


def summarize_transaction_log(transaction_log):
    """
    This function summarizes a transaction log. It should return a dictionary
    with the following fields:
    - total-volume (the total amount of money exchanged)
    - volume-per-hour (a list of amount of money exchanged per hour)
    - total-number-of-transactions
    - number-of-transaction-per-hour (also a list)

    The hour breakdowns should include one entry for each hour of the day.

    E.g., if summarize_transaction_log(TRANSACTION_LOG_SAMPLE_1) is summary
    then summary['total-number-of-transactions'] is 8
    and summary['number-of-transaction-per-hour']
    is [ …, 0, 1, 3, 0, 1, 3, 0, …]

    :param transaction_log: log of transactions. See sample.
    :return: summary as described above.
    :rtype: dict
    """

    th = {x: 0 for x in range(24)}
    hours = []
    totaltrans = 0
    totalvolume = 0
    volumeph = th.copy()
    volume = 0
    for trans in transaction_log:
        totaltrans += 1
        volume = trans['quantity'] * trans['unit-price']
        totalvolume += volume
        hour = trans['time'].hour
        if hour not in hours:
            hours.append(trans['time'].hour)
        if hour not in th.keys():
            th[hour] = 1
        else:
            th[hour] += 1
        if hour not in volumeph.keys():
            volumeph[hour] = 1
        else:
            volumeph[hour] += volume
    print(totaltrans, totalvolume, th, hours, volumeph)
    l_ret = {'total-volume': totalvolume,
    'volume-per-hour': [x for x in volumeph.values()], 
    'total-number-of-transactions': totaltrans,
    'number-of-transaction-per-hour': [x for x in th.values()]}
    return l_ret


summarize_transaction_log([])

summarize_transaction_log([{'name': 'NAME', 'nature': 'buy', 'quantity': 1, 'unit-price': 1, 'time': datetime.time(0, 0, 0, 1)}])
summarize_transaction_log([{'name': 'NAME', 'nature': 'buy', 'quantity': 4, 'unit-price': 5, 'time': datetime.time(12, 33, 25)}, {'name': 'NAME', 'nature': 'buy', 'quantity': 1, 'unit-price': 6, 'time': datetime.time(13, 33, 25)}])
summarize_transaction_log([{'name': 'SKIL', 'nature': 'buy', 'quantity': 11, 'unit-price': 442, 'time': datetime.time(8, 22, 52)}, {'name': 'DOAA', 'nature': 'sell', 'quantity': 43, 'unit-price': 122, 'time': datetime.time(7, 1, 10)}, {'name': 'DOAA', 'nature': 'sell', 'quantity': 2, 'unit-price': 119, 'time': datetime.time(8, 3)}, {'name': 'DOAA', 'nature': 'sell', 'quantity': 10, 'unit-price': 118, 'time': datetime.time(8, 3, 41)}, {'name': 'DOAA', 'nature': 'sell', 'quantity': 20, 'unit-price': 116, 'time': datetime.time(10, 8, 21)}, {'name': 'DOAA', 'nature': 'sell', 'quantity': 11, 'unit-price': 113, 'time': datetime.time(11, 44, 14)}, {'name': 'SKIL', 'nature': 'sell', 'quantity': 8, 'unit-price': 450, 'time': datetime.time(11, 22, 22)}, {'name': 'SKIL', 'nature': 'sell', 'quantity': 3, 'unit-price': 451, 'time': datetime.time(11, 56)}])
