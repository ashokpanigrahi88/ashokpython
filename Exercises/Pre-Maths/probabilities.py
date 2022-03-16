from scipy.special import comb
"""
This file contains a set of functions to practice your
probabilities skills.

It needs to be completed with "vanilla" Python, without
help from any library -- except for the bin_dist function.
"""


def head_tails(p, n):
    """
    Given a coin that have probability p of giving a heads
    in each toss independently, what is the probability of
    having n heads consecutively in a row?

    :param p: probability of a head
    :param n: number of heads in a row (int)
    :return: probability of having n heads in a row
    :rtype: float
    """

    return  p**n

head_tails(0.5,1)


def bin_dist(n, p, x):
    """
    Given n number of trials, p the probability of success,
    what is the probability of having x successes?

    Your function should raise a ValueError if x is higher
    than n.

    If you need to compute combinations, you can import the
    function "comb" from the package "scipy.special"

    :param n: number of trials (int)
    :param p: probability of success
    :param x: number of successes (int)
    :return: probability of having x successes
    :rtype: float
    :raise ValueError: if x > n
    """


    if x > n:
       #  raise ValueError('value error')
       return ValueError
        
    return comb(n, x, exact=True) * (p ** x) * ((1 - p) ** (n - x))


bin_dist(10, .5, 6)
bin_dist(3, .7, 4)

def fact(x):
    """
    Return the factorial of x.
    Your function should raise a ValueError
    if x is negative

    :param x: a number (int)
    :return: the factorial of x
    :rtype: float
    :raise ValueError:
    """

    if x < 0:
        raise ValueError('x is negative')
    lfact = 1
    for i in range(1, x+1):
        lfact = lfact*i

    return float(lfact)


def bin_cdf(n, p, x):
    """
    Given n number of trials, p the probability of successes,
    what is the probability of having less than or equal to x successes?

    Your function should raise a ValueError if x is higher
    than n.

    :param n: number of trials (int)
    :param p: probability of success
    :param x: number of successes (int)
    :return: probability of having less than or
    equal to x successes
    :rtype: float
    :raise ValueError: if x > n
    """
    if x > n:
     return ValueError
     
    if p == 0:
        return 0

    q = 1 - p
    l_outcomes = (fact(n)/(fact(x)*fact(n-x))) 
    l_probability = (p**n)
    return l_outcomes/l_probability

bin_cdf(3, 1, 1)
bin_cdf(3, 0 ,1)
bin_cdf(3, 0.7, 2)
bin_cdf(3, 0.7, 4)
bin_cdf(4, 0.2, 3)
bin_cdf(4, 0.4, 2)
bin_cdf(4, 0.8, 3)
bin_cdf(5, 0.2, 2)
bin_cdf(5, 0.2, 3)
bin_cdf(5, 0.4, 2)
bin_cdf(5, 0.4, 3)
bin_cdf(5, 0.8, 3)
bin_cdf(5, 0.2, 2)
bin_cdf(6, 0.2, 3)
bin_cdf(6, 0.4, 2)
bin_cdf(6, 0.4, 3)
bin_cdf(6, 0.8, 3)

