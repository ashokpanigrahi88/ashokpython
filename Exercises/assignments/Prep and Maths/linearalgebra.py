"""
This file contains a set of functions to practice your
linear algebra skills.

It needs to be completed with "vanilla" Python, without
help from any library.
"""


def gradient(w1, w2, x):
    """
    Given the following function f(x) = w1 * x1^2 + w2 * x2
    where x is a vector with coordinates [x1, x2]
    evaluate the gradient of the function at the point x

    :param w1: first coefficient
    :param w2: second coefficient
    :param x: a point represented by a tuple (x1, x2)
    :return: the two coordinates of gradient of f
    at point x
    :rtype: float, float
    """

    return 2 * w1 * x[0], w2


def metrics(u, v):
    """
    Given two vectors, evaluate the following metrics and return two arguments:
    - l1 Distance
    - l2 Distance

    If the two vectors have a different dimension,
    you should raise a ValueError

    :param u: first vector (list)
    :param v: second vector (list)
    :return: l1 distance, l2 distance
    :rtype: float, float
    :raise ValueError:
    """

    if len(u) != len(v):
        raise ValueError

    l1_dist = sum([abs(a - b) for a, b in zip(u, v)])
    l2_dist = sum([(a - b)**2 for a, b in zip(u, v)])**.5

    return l1_dist, l2_dist


def list_mul(u, v):
    """
    Given two vectors, calculate and return the following quantities:
    - element-wise sum
    - element-wise product
    - dot product

    If the two vectors have a different dimension,
    you should raise a ValueError

    :param u:first vector (list)
    :param v:second vector (list)
    :return:the three quantities above
    :rtype: list, list, float
    :raise ValueError:
    """

    if len(u) != len(v):
        raise ValueError

    elem_sum = [a + b for a, b in zip(u, v)]
    elem_prod = [a * b for a, b in zip(u, v)]
    dot_prod = sum(elem_prod)

    return elem_sum, elem_prod, dot_prod


def matrix_mul(A, B):
    """
    Given two matrices A and B represented as a list of list,
    implement a function to multiply them together (A * B)

    For example:
    A = [[1, 2, 3],
          [4, 5, 6]]
    is a matrix with twp rows and three columns.

    If the two matrices have incompatible dimensions,
    you should raise a ValueError

    :param A: first matrix (list of list)
    :param B: second matrix (list of list)
    :return: resulting matrix (list of list)
    :rtype: list(list)
    :raise ValueError:
    """

    if len(A[0]) != len(B):
        raise ValueError

    nrow = len(A)
    ncol = len(B[0])

    mat_prod = []
    for i in range(nrow):
        mat = []
        for j in range(ncol):
            mat.append(sum([a * b for a, b in zip(A[i], [row[j] for row in B])]))

        mat_prod.append(mat)

    return mat_prod
