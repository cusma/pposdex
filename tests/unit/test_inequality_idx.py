import math
from collections.abc import Callable

import pytest
from hypothesis import given
from hypothesis import strategies as st

from pposdex import inequality_idx as idx

type Index = Callable[[list[float]], float]

SMALL_EQUAL = (0.20,) * 5
LARGE_EQUAL = (0.01,) * 100
INEQUAL = (0.15,) * 6 + (0.01,) * 10
VERY_INEQUAL = (0.80,) + (0.02,) * 5 + (0.01,) * 10
# A single small stake among large ones, and a single large stake among small ones
LOW_END_INEQUAL = (1.0,) + (1000.0,) * 99
HIGH_END_INEQUAL = (1.0,) * 99 + (1000.0,)

EQUAL_DISTRIBUTIONS = pytest.mark.parametrize(
    "distribution", [SMALL_EQUAL, LARGE_EQUAL], ids=["small", "large"]
)


def ge(alpha: float) -> Index:
    return lambda distribution: idx.generalized_entropy(distribution, alpha)


ZERO_ON_EQUALITY = pytest.mark.parametrize(
    "index",
    [idx.gini, ge(2), ge(3), idx.theil_l, idx.theil_t],
    ids=["gini", "ge2", "ge3", "theil_l", "theil_t"],
)
INDEXES = pytest.mark.parametrize(
    "index",
    [idx.gini, ge(2), idx.theil_l, idx.theil_t, idx.herfindahl_hirschman],
    ids=["gini", "ge2", "theil_l", "theil_t", "hhi"],
)

# Microalgo balances, exact as floats up to 2**53
stake = st.integers(min_value=1, max_value=10**15).map(float)
stakes = st.lists(stake, min_size=1, max_size=200)


class TestScalarProduct:
    @pytest.mark.parametrize(
        ("vector_1", "vector_2", "expected"),
        [([1, 0], [0, 1], 0), ([1, 2], [2, 1], 4)],
    )
    def test_value(
        self, vector_1: list[float], vector_2: list[float], expected: float
    ) -> None:
        assert idx.scalar_product(vector_1, vector_2) == expected

    def test_different_lengths(self) -> None:
        with pytest.raises(ValueError, match="longer"):
            idx.scalar_product([1, 1], [1, 1, 1])


class TestExamples:
    @ZERO_ON_EQUALITY
    @EQUAL_DISTRIBUTIONS
    def test_zero_on_equality(
        self, index: Index, distribution: tuple[float, ...]
    ) -> None:
        assert index(list(distribution)) == pytest.approx(0, abs=1e-15)

    @INDEXES
    def test_grows_with_inequality(self, index: Index) -> None:
        assert index(list(INEQUAL)) < index(list(VERY_INEQUAL))

    def test_gini_value(self) -> None:
        assert idx.gini([1, 2, 3, 4]) == 0.25

    @pytest.mark.parametrize(
        ("distribution", "expected"),
        [
            (SMALL_EQUAL, 0.20),
            (LARGE_EQUAL, 0.01),
            (INEQUAL, 0.136),
            (VERY_INEQUAL, 0.643),
        ],
        ids=["small_equal", "large_equal", "inequal", "very_inequal"],
    )
    def test_hhi_value(self, distribution: tuple[float, ...], expected: float) -> None:
        assert idx.herfindahl_hirschman(list(distribution)) == pytest.approx(expected)

    def test_ge_sensitivity(self) -> None:
        # Small alpha weighs small stakes, large alpha weighs large stakes
        low_end, high_end = list(LOW_END_INEQUAL), list(HIGH_END_INEQUAL)
        assert ge(2)(low_end) > ge(20)(low_end)
        assert ge(2)(high_end) < ge(20)(high_end)

    def test_theil_sensitivity(self) -> None:
        # Theil L weighs small stakes, Theil T weighs large stakes
        low_end, high_end = list(LOW_END_INEQUAL), list(HIGH_END_INEQUAL)
        assert idx.theil_l(low_end) > idx.theil_t(low_end)
        assert idx.theil_l(high_end) < idx.theil_t(high_end)


class TestInvalidInput:
    @pytest.mark.parametrize(
        "index",
        [idx.gini, idx.theil_l, idx.theil_t, idx.herfindahl_hirschman, ge(2)],
        ids=["gini", "theil_l", "theil_t", "hhi", "ge2"],
    )
    def test_empty_distribution(self, index: Index) -> None:
        with pytest.raises(ValueError, match="empty"):
            index([])

    @pytest.mark.parametrize("alpha", [0, 1])
    def test_ge_alpha(self, alpha: float) -> None:
        with pytest.raises(ValueError, match="Alpha"):
            idx.generalized_entropy([1.0, 2.0], alpha)

    def test_gini_does_not_sort_input(self) -> None:
        distribution = [3.0, 1.0, 2.0]
        idx.gini(distribution)
        assert distribution == [3.0, 1.0, 2.0]


class TestNakamoto:
    @pytest.mark.parametrize(
        ("distribution", "share", "expected"),
        [
            (LARGE_EQUAL[:10], 1 / 3, 4),
            (LARGE_EQUAL[:9], 1 / 3, 4),
            (INEQUAL, 1 / 3, 3),
            (INEQUAL, 1 / 2, 4),
            (VERY_INEQUAL, 1 / 3, 1),
            (VERY_INEQUAL, 0.9, 6),
        ],
    )
    def test_value(
        self, distribution: tuple[float, ...], share: float, expected: int
    ) -> None:
        assert idx.nakamoto_coefficient(list(distribution), share) == expected

    def test_default_share_is_a_third(self) -> None:
        assert idx.nakamoto_coefficient(list(INEQUAL)) == 3

    @pytest.mark.parametrize(
        ("distribution", "share", "match"),
        [
            ([], 1 / 3, "empty"),
            ([1.0, 2.0], 1, "Share"),
            ([1.0, 2.0], -0.1, "Share"),
            ([0.0, 0.0], 1 / 3, "wealth"),
        ],
    )
    def test_invalid(self, distribution: list[float], share: float, match: str) -> None:
        with pytest.raises(ValueError, match=match):
            idx.nakamoto_coefficient(distribution, share)


class TestProperties:
    @given(stakes)
    def test_gini_bounds(self, distribution: list[float]) -> None:
        n = len(distribution)
        assert -1e-12 <= idx.gini(distribution) <= 1 - 1 / n + 1e-12

    @given(stakes)
    def test_theil_bounds(self, distribution: list[float]) -> None:
        tolerance = 1e-9
        upper = math.log(len(distribution)) + tolerance
        assert idx.theil_l(distribution) >= -tolerance
        assert -tolerance <= idx.theil_t(distribution) <= upper

    @given(stakes)
    def test_hhi_bounds(self, distribution: list[float]) -> None:
        n = len(distribution)
        assert 1 / n - 1e-12 <= idx.herfindahl_hirschman(distribution) <= 1 + 1e-12

    @given(stake, st.integers(1, 200))
    def test_equal_stakes(self, value: float, n: int) -> None:
        distribution = [value] * n
        assert idx.gini(distribution) == pytest.approx(0, abs=1e-12)
        assert idx.theil_l(distribution) == pytest.approx(0, abs=1e-12)
        assert idx.theil_t(distribution) == pytest.approx(0, abs=1e-12)
        assert idx.herfindahl_hirschman(distribution) == pytest.approx(1 / n)

    @given(stakes, st.floats(0, 0.99))
    def test_nakamoto_bounds(self, distribution: list[float], share: float) -> None:
        assert 1 <= idx.nakamoto_coefficient(distribution, share) <= len(distribution)

    @given(stakes, st.floats(0, 0.98), st.floats(0, 0.01))
    def test_nakamoto_grows_with_share(
        self, distribution: list[float], share: float, more: float
    ) -> None:
        nakamoto = idx.nakamoto_coefficient
        assert nakamoto(distribution, share) <= nakamoto(distribution, share + more)

    @INDEXES
    @given(distribution=stakes, data=st.data())
    def test_permutation_invariance(
        self, index: Index, distribution: list[float], data: st.DataObject
    ) -> None:
        shuffled = data.draw(st.permutations(distribution))
        assert index(shuffled) == pytest.approx(index(distribution), abs=1e-9)

    @INDEXES
    @given(distribution=stakes, factor=st.integers(2, 1000))
    def test_scale_invariance(
        self, index: Index, distribution: list[float], factor: int
    ) -> None:
        scaled = [stake * factor for stake in distribution]
        assert index(scaled) == pytest.approx(index(distribution), abs=1e-9)
