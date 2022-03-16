# TRANSACTIONS ANALYSIS #
import datetime

# DO NOT MODIFY CONSTANTS
TRANSACTION_LOG_SAMPLE_1 = [
    {
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
    },
]


def volume(transaction_log):
    """
    :param transaction_log:
    :return:
    :rtype:
    """
    return sum([t['quantity'] * t['unit-price'] for t in transaction_log])


def split_per_hour(transaction_log):
    """
    :param transaction_log:
    :return:
    :rtype:
    """
    hour_marks = [(datetime.time(h, 0, 0, 0), datetime.time(h, 59, 59, 999999))
                  for h in range(0, 24)]
    split = []
    for (low, high) in hour_marks:
        split.append([t for t in transaction_log if low <= t['time'] <= high])
    return split


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

    split_log = split_per_hour(transaction_log)
    split_volume = [volume(log) for log in split_log]
    split_number = [len(log) for log in split_log]
    result = {
        'total-volume': volume(transaction_log),
        'volume-per-hour': split_volume,
        'total-number-of-transactions': len(transaction_log),
        'number-of-transaction-per-hour': split_number
    }
    return result
