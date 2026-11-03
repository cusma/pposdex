import pytest


@pytest.fixture(scope="session")
def small_equal_distribution() -> list[float]:
    return [0.20] * 5


@pytest.fixture(scope="session")
def large_equal_distribution() -> list[float]:
    return [0.01] * 100


@pytest.fixture(scope="session")
def inequal_distribution() -> list[float]:
    return [0.15] * 6 + [0.01] * 10


@pytest.fixture(scope="session")
def very_inequal_distribution() -> list[float]:
    return [0.80] + [0.02] * 5 + [0.01] * 10


@pytest.fixture(scope="session")
def low_end_inequal_distribution() -> list[float]:
    return [1.0] + [1000.0] * 99


@pytest.fixture(scope="session")
def high_end_inequal_distribution() -> list[float]:
    return [1.0] * 99 + [1000.0]
