import math
"""
This file contains a set of functions to practice your
statistics skills.

It needs to be completed with "vanilla" Python, without
help from any library.
"""


def calculate_mean(data):
    """
    Return the mean of a python list

    If data is empty raise a ValueError

    :param data: a list of numbers
    :return: the mean of the list
    :rtype: float
    :raise ValueError:
    """

    if data == []:
        raise ValueError('Data is empty')
    l_mean = float(0)
    l_len = len(data)
    for i in range(l_len):
        l_mean += data[i]
    l_mean = l_mean/l_len

    return(l_mean)


calculate_mean([2])
calculate_mean([2, -2, 4, -4])
calculate_mean([2, 5, 6, 2, 9])
calculate_mean([4, 7, 2])
calculate_mean([9, 3, 6, -2, 3, 6, 19])
calculate_mean([12, 4, 3, 1])


def calculate_standard_deviation(data):
    """
    Return the standard deviation of a python list

    If data is empty raise a ValueError

    :param data: list of numbers
    :return: the standard deviation of the list
    :rtype: float
    :raise ValueError:
    """

    if data == []:
        raise ValueError('Data is empty')
    l_mean = float(0)
    l_stdmean = float(0)
    l_len = len(data)
    for i in range(l_len):
        l_mean += data[i]
    l_mean = l_mean/l_len
    l_starray = [(x-l_mean)**2 for x in data]
    for i in range(l_len):
        l_stdmean += l_starray[i]
    l_stdmean = l_stdmean/l_len
    l_stdmean = math.sqrt(l_stdmean)
    return(l_stdmean)


calculate_standard_deviation([2])
calculate_standard_deviation([2, -2, 4, -4])
calculate_standard_deviation([2, 5, 6, 2, 9])
calculate_standard_deviation([4, 7, 2])
calculate_standard_deviation([9, 3, 6, -2, 3, 6, 19])
calculate_standard_deviation([12, 4, 3, 1])

def cal_mean(p_measures):
    lmedian = float(0)
    llen = 0
    lmiddle = 0
    lmeasures = p_measures
    lmeasures.sort()
    llen = len(lmeasures)
    lmiddle = llen//2-1
    if (llen % 2) == 1:
        lmedian = lmeasures[lmiddle]
    else:
        lmedian = (lmeasures[lmiddle] + lmeasures[lmiddle+1])
    return lmeasures, llen, lmiddle, lmedian
        
def remove_outliers(data):
    """
    Given a list of numbers, find outliers and return a new
    list that contains all points except outliers
    We consider points lying outside 2 standard
    deviations from the mean.

    Make sure that you do not modify the original list!

    If data is empty raise a ValueError

    :param data: list of numbers
    :return: a new list without outliers
    :rtype: list
    :raise ValueError:
    """

    if data is []:
        raise ValueError
    
    if data == []:
        raise ValueError
        
    if len(data) == 0:
        return None
       
    l_mean = float(0)
    l_meanq = float(0)
    l_len = 0
    l_middle = 0
    l_q1med = 0
    l_q3mmed = 0
    l_qmid = 0
    l_measures = data.copy()
    l_len = len(l_measures)
    l_rangelow = 0
    l_rangehigh = 0
    l_multiplier = 3.0
    l_iqr = 0
    

    if len(l_measures) == 1:
        return data

    l_measures, l_len, l_middle, l_median = cal_mean(l_measures)

    for num in range(l_len):
        l_mean += l_measures[num]
    l_mean = l_mean/(l_len)
    l_q1 = l_measures[0:l_middle+1]
    l_q1, l_len, l_qmid, l_q1med = cal_mean(l_q1)
    l_q3 = l_measures[l_middle+1:]
    l_q3, l_len, l_qmid, l_q3med = cal_mean(l_q3)
    l_iqr = l_q3med-l_q1med
    l_rangelow = l_mean-(l_iqr*1.5)
    l_rangehigh = l_mean+(l_iqr*1.5)
    data = [x for x in data if x <= l_rangehigh]
    # data = [x for x in data if x  > (l_iqr*1.5)]

    return data


#remove_outliers([])
remove_outliers([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 100, 156])
remove_outliers([1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 200])
remove_outliers([30, -100, 200, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 300, 2, 2, 2, 2, 2])
remove_outliers([5, 5, 5, 5, 5, 5, 5, 5, 250, 300, 6, 6, 6])
remove_outliers([3, 3, 3, 3, 3, 3, 3, 3, 3, 350])
remove_outliers([0, 0, 0, 0, 0, 0, 0, 0, 2000])

