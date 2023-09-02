"""
Inequality Indexes
"""

import math


def scalar_product(vector_1: list[float], vector_2: list[float]) -> float:
    """
    Scalar Product

    Args:
        vector_1: First vector of the scalar product
        vector_2: Second vector of the scalar product

    Returns:
        Scalar product (vector_1 * vector_2)
    """
    assert len(vector_1) == len(vector_2)
    return sum(i[0] * i[1] for i in zip(vector_1, vector_2))


def gini(distribution: list[float]) -> float:
    """
    Gini's Index

    Args:
        distribution: Wealth distribution of the population

    Returns:
        Gini's Index (G), inequality of wealth distribution
            0 <= G < 1,
            G = 0, perfect equality
    """
    assert distribution
    n = len(distribution)
    distribution.sort()
    num = scalar_product(list(range(1, n + 1)), distribution)
    den = sum(distribution)
    return (2 / n) * (num / den) - (n + 1) / n


def generalized_entropy(distribution: list[float], alpha: float) -> float:
    """
    Genralized Entropy Index

    Args:
        distribution: Wealth distribution of the population
        alpha: Inequality weight. For large alpha the index is especially
            sensitive to the existence of large incomes, whereas for small
            alpha the index is especially sensitive to the existence of
            small incomes

    Returns:
        Generalized Entropy Index (GE), inequality of wealth
            distribution with inequality weight alpha
            0 <= GE(aplha) < +inf,
            GE(alpha) = 0, perfect equality,
            alpha != 0, 1
    """
    assert distribution
    assert alpha != 0 and alpha != 1
    n = len(distribution)
    mean_amount = sum(distribution) / n
    epsilon: float = 0
    for amount in distribution:
        epsilon += (amount / mean_amount) ** alpha - 1
    return epsilon / (n * alpha * (alpha - 1))


def theil_l(distribution: list[float]) -> float:
    """
    Theil's L Index is sensitive to differences at the lower end of the
    distribution (small incomes).

    Args:
        distribution: Wealth distribution of the population

    Returns:
        Theil's L Index (TL), inequality of wealth distribution
            0 <= TL < +inf
            TL = 0, perfect equality
    """
    assert distribution
    n = len(distribution)
    mean_amount = sum(distribution) / n
    epsilon: float = 0
    for amount in distribution:
        epsilon += math.log(amount / mean_amount)
    return -epsilon / n


def theil_t(distribution: list[float]) -> float:
    """
    Theil's T Index is more sensitive to differences at the top of the
    distribution (large incomes).

    Args:
        distribution: Wealth distribution of the population

    Returns:
        Theil's T Index (TT), inequality of wealth distribution
            0 <= TT < +inf
            TT = 0, perfect equality
    """
    assert distribution
    n = len(distribution)
    mean_amount = sum(distribution) / n
    epsilon: float = 0
    for amount in distribution:
        epsilon += (amount / mean_amount) * math.log(amount / mean_amount)
    return epsilon / n


def herfindahl_hirschman(distribution: list[float]) -> float:
    """
    Herfindahl–Hirschman Index

    Args:
        distribution: Wealth distribution in the market

    Returns:
        Herfindahl–Hirschman Index (HHI), market concentration degree
            0 <= HHI < 1,
            HHI = 0, perfectly competitive
    """
    assert distribution
    market_size = sum(distribution)
    market_shares = [share / market_size for share in distribution]
    return sum([share**2 for share in market_shares])
