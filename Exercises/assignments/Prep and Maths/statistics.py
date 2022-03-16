# STATISTICS #
import math

# DO NOT MODIFY CONSTANTS
MEASURES_SAMPLE = [
    10.1, 10.2, 9.9, 10.1, 11.3, 14.2, 12.3, 12.3, 12.3, 12.1, 12.3, 11.9, 10.2,
    10.1, 9.8, 8.9, 9.7, 9.8, 9.8, 10.2, 10.3, 10.5, 12.3, 10.1, 8.9, 9.8, 10.5,
    10.1, 10.6, 10.7, 10.0, 9.9, 13.0, 13.1, 13.0, 13.2, 14.0
]


def median_and_means(measures):
    """
    To get an accurate summary of a set of measure, this function computes the
    following value and returns them in a tuple:
        - median
        - mean (average)
        - mean of the values between the first quartile and third quartile

    E.g., median_and_means([1,2,3,4,5,6,7,8,9]) is (5, 5, 5)

    Note: if measures is an empty list, your function should return the object None.

    :param measures: list of measures
    :return: tuple (med, mean, mean_50) where med is the median of the values
    in measures, mean is the mean and mean_50 the mean of the 50% of value in
    the middle of the range.
    :rtype: tuple
    """

    # Edge case
    if not measures:
        return None

    sorted_measures = sorted(measures)
    measures_count = len(measures)

    if measures_count % 2 == 0:
        median = (sorted_measures[measures_count // 2 - 1] +
                  sorted_measures[measures_count // 2]) / 2
    else:
        median = sorted_measures[measures_count // 2]
    average = sum(measures) / measures_count
    quart_1 = int(math.ceil(measures_count / 4))
    quart_3 = int(math.floor(3 * measures_count / 4))
    middle = sorted_measures[quart_1:quart_3]
    average_middle = sum(middle) / len(middle)
    return (median, average, average_middle)
