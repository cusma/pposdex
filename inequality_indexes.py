
import math


def scalar_product(vector_1, vector_2):
    """Scalar Product

    Args:
        vector_1 (list):
        vector_2 (list):

    Returns:
        (float): scalar product (vector_1 * vector_2)
    """
    if len(vector_1) != len(vector_2):
        return 0
    return sum(i[0] * i[1] for i in zip(vector_1, vector_2))


def gini_index(distribution):
    """Gini's Index

    Args:
        distribution (list): wealth distribution of the population

    Returns:
        (float): Gini's Index (G), inequality of wealth distribution
            0 <= G < 1,
            G = 0, perfect equality
    """
    n = len(distribution)
    distribution.sort()
    elements = [i for i in range(1, n + 1)]
    numerator = scalar_product(elements, distribution)
    denominator = sum(distribution)
    return (2 / n) * (numerator / denominator) - (n + 1) / n


def generalized_entropy_index(distribution, alpha):
    """Genralized Entropy Index

    Args:
        distribution (list): wealth distribution of the population
        alpha (float): inequality weight, for large alpha the index is
            especially sensitive to the existence of large incomes,
            whereas for small alpha the index is especially sensitive to the
            existence of small incomes

    Returns:
        (float): Generalized Entropy Index (GE), inequality of wealth
            distribution with inequality weight alpha
            0 <= GE(aplha) < +inf,
            GE(alpha) = 0, perfect equality
    """
    n = len(distribution)
    mean_amount = sum(distribution) / n
    epsilon = 0
    for amount in distribution:
        epsilon += (amount / mean_amount) ** alpha - 1
    return epsilon / (n * alpha * (alpha - 1))


def theil_l_index(distribution):
    """Theil's L Index is sensitive to differences at the lower end of the
    distribution (small incomes).

    Args:
        distribution (list): wealth distribution of the population

    Returns:
        (float): Theil's L Index (TL), inequality of wealth distribution
            0 <= TL < +inf
            TL = 0, perfect equality
    """
    n = len(distribution)
    mean_amount = sum(distribution) / n
    epsilon = 0
    for amount in distribution:
        epsilon += math.log(amount / mean_amount)
    return - epsilon / n


def theil_t_index(distribution):
    """Theil's T Index is more sensitive to differences at the top of the
    distribution (large incomes).

    Args:
        distribution (list): wealth distribution of the population

    Returns:
        (float): Theil's T Index (TT), inequality of wealth distribution
            0 <= TT < +inf
            TT = 0, perfect equality
    """
    n = len(distribution)
    mean_amount = sum(distribution) / n
    epsilon = 0
    for amount in distribution:
        epsilon += (amount / mean_amount) * math.log(amount / mean_amount)
    return epsilon / n
