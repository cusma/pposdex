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

    Raises:
        ValueError: if the vectors have different lengths
    """
    return sum(x_1 * x_2 for x_1, x_2 in zip(vector_1, vector_2, strict=True))


def _check_not_empty(distribution: list[float]) -> None:
    if not distribution:
        raise ValueError("Distribution must not be empty")


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
    _check_not_empty(distribution)
    n = len(distribution)
    distribution = sorted(distribution)
    num = scalar_product(list(range(1, n + 1)), distribution)
    den = sum(distribution)
    return (2 / n) * (num / den) - (n + 1) / n


def generalized_entropy(distribution: list[float], alpha: float) -> float:
    """
    Generalized Entropy Index

    Args:
        distribution: Wealth distribution of the population
        alpha: Inequality weight. For large alpha the index is especially
            sensitive to the existence of large incomes, whereas for small
            alpha the index is especially sensitive to the existence of
            small incomes

    Returns:
        Generalized Entropy Index (GE), inequality of wealth
            distribution with inequality weight alpha
            0 <= GE(alpha) < +inf,
            GE(alpha) = 0, perfect equality,
            alpha != 0, 1
    """
    _check_not_empty(distribution)
    if alpha in {0, 1}:
        raise ValueError("Alpha must be different from 0 and 1")
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
    _check_not_empty(distribution)
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
    _check_not_empty(distribution)
    n = len(distribution)
    mean_amount = sum(distribution) / n
    epsilon: float = 0
    for amount in distribution:
        epsilon += (amount / mean_amount) * math.log(amount / mean_amount)
    return epsilon / n


def herfindahl_hirschman(distribution: list[float]) -> float:
    """
    Herfindahl-Hirschman Index

    Args:
        distribution: Wealth distribution in the market

    Returns:
        Herfindahl-Hirschman Index (HHI), market concentration degree
            0 <= HHI < 1,
            HHI = 0, perfectly competitive
    """
    _check_not_empty(distribution)
    market_size = sum(distribution)
    return sum((share / market_size) ** 2 for share in distribution)
