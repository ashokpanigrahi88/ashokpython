"""A set of numpy exercises"""
import numpy as np
from numpy import linalg as lin
import matplotlib.pyplot as plt


def zero_insert(x):
    """
    Write a function that takes in a vector and returns a new vector where
    every element is separated by 4 consecutive zeros.

    Example:
    [4, 2, 1] --> [4, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1]

    :param x: input vector
    :type x: numpy.array
    :return: input vector with elements separated by 4 zeros
    :rtype: numpy.array
    """

    output = []
    output1 = []
    if x == []:
        return(x)
    for item in range(len(x)):
        if item < len(x)-1:
            y = np.append(x[item], np.zeros(4, dtype='int32'))
            output.append(y)
        else:
            output1 = np.array(output).flatten()
            output1 = list(output1)
            output1.append(x[item])
    
    return(np.array(output1))


def return_closest(x, val):
    """
    Write a function that takes in a vector and returns the value contained in
    the vector that is closest to a given value.
    If two values are equidistant from val, return the one that comes first in
    the vector.

    Example:
    ([3, 4, 5], 2) --> 3

    :param x: input vector
    :type x: numpy.array of int/float
    :param val: input value
    :type val: int | float
    :return: value from x closest to val
    :rtype: int | float
    :raise ValueError:
    """

    return(min(x,key=lambda y : abs(y-val))) 


def cauchy(x, y):
    """
    Write a function that takes in two vectors and returns the associated Cauchy
    matrix with entries a_ij = 1/(x_i-y_j).

    Example:
    ([1, 2], [3, 4]) --> [[-1/2, -1/3], [-1, -1/2]]

    Note: the function should raise an error of type ValueError if there is a
    pair (i,j) such that x_i=y_j

    :param x: input vector
    :type x: numpy.array of int/float
    :param y: input vector
    :type y: numpy.array of int/float
    :return: Cauchy matrix with entries 1/(x_i-y_j)
    :rtype: numpy.array of float
    :raise ValueError:
    """
    if 0 in x or 0 in y:
        raise ValueError
        
    lenx = len(x)
    leny = len(y)
        
    xm = np.repeat(x, leny) #the i'th row is s_i
    ym = np.tile(y, lenx)
    diff = xm-ym
    if 0 in diff:
        raise ValueError
    cauchym = (1.0/(xm-ym)).reshape([lenx,leny]);
    return(cauchym)


def most_similar(x, v_list):
    """
    Write a function that takes in a vector x and a list of vectors and finds,
    in the list, the index of the vector that is most similar to x using
    cosine similarity.

    Example:
    ([1, 1], [[1, 0.9], [-1, 1]]) --> 0 (corresponding to [1,0.9])

    :param x: input vector
    :type x: numpy.array of int/float
    :param v_list: list of vectors
    :type v_list: list of numpy.array
    :return: index of element in list that is closest to x in cosine-sim
    :rtype: int
    """

    prevcosine = 0
    ind = 0 
    for v in v_list:
        dot_product = np.dot(x,v)
        cosine = dot_product/(lin.norm(x)*lin.norm(v))
        if prevcosine < cosine:
            prevcosine = cosine
            ret = ind 
        ind += 1 
    return(ret)

def gradient_descent(x_0, learning_rate, tol):
    """
    Write a function that does gradient descent with a fixed learning_rate
    on function f with gradient g and stops when the update has magnitude
    under a given tolerance level (i.e. when |xk-x(k-1)| < tol).
    Return a tuple with the position, the value of f at that position and the
    magnitude of the last update.
    h(x) = (x-1)^2 + exp(-x^2/2)
    f(x) = log(h(x))
    g(x) = (2(x-1) - x exp(-x^2/2)) / h(x)

    Example:
    (1.0, 0.1, 1e-3) --> approximately (1.2807, -0.6555, 0.0008)

    :param x_0: initial point
    :type x_0: float
    :param learning_rate: fixed learning_rate
    :type learning_rate: float
    :param tol: tolerance for the magnitude of the update
    :type tol: float
    :return: the position, the value at that position and the latest update
    :rtype: tuple of three float
    """
    def h_of_x(x):
        return(((x-1)**2 + np.exp((-x**2)/2)))
    
    def f_of_x(x):
        return(np.log(h_of_x(x)))
    
    def g_of_x(x):
        return((2*(x-1) - x * np.exp(-x**2/2))/ h_of_x(x))
        
    x = np.linspace(-4,4,400)
    plt.axis('equal')
    plt.plot(x,f_of_x(x), ls='-')
    for i in range(210):
        x_0 += learning_rate     
        plt.plot(x_0,g_of_x(x_0), ls='-',marker='o', markersize='8')
    return((x_0,g_of_x(x_0)))
