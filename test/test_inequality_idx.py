import math
import pytest

import src.inequality_idx as idx


def test_scalar_product() -> None:
    with pytest.raises(AssertionError):
        idx.scalar_product([1, 1], [1, 1, 1])

    assert idx.scalar_product([1, 0], [0, 1]) == 0
    assert idx.scalar_product([1, 2], [2, 1]) == 4


class TestGiniIndex:
    def test_equality(
        self,
        small_equal_distribution: list[float],
        large_equal_distribution: list[float],
    ) -> None:
        gi_1 = idx.gini(small_equal_distribution)
        gi_2 = idx.gini(large_equal_distribution)
        assert math.isclose(gi_1, 0, abs_tol=1e-15)
        assert math.isclose(gi_2, 0, abs_tol=1e-15)

    def test_inequality(
        self,
        inequal_distribution: list[float],
        very_inequal_distribution: list[float],
    ) -> None:
        gi_1 = idx.gini(inequal_distribution)
        gi_2 = idx.gini(very_inequal_distribution)
        assert gi_1 < gi_2
        print(f"Gini - Low Inequality: {gi_1}")
        print(f"Gini - High Inequality: {gi_2}")

    def test_value(self) -> None:
        assert idx.gini(list(range(1, 5))) == 0.25


class TestGeneralizedEntropy:
    def test_equality(
        self,
        small_equal_distribution: list[float],
        large_equal_distribution: list[float],
    ) -> None:
        ge_1 = idx.generalized_entropy(small_equal_distribution, 2)
        ge_2 = idx.generalized_entropy(large_equal_distribution, 3)
        assert math.isclose(ge_1, 0, abs_tol=1e-15)
        assert math.isclose(ge_2, 0, abs_tol=1e-15)

    def test_inequality(
        self,
        inequal_distribution: list[float],
        very_inequal_distribution: list[float],
    ) -> None:
        ge_1 = idx.generalized_entropy(inequal_distribution, 2)
        ge_2 = idx.generalized_entropy(very_inequal_distribution, 2)
        assert ge_1 < ge_2

    def test_sensitivity(
        self,
        low_end_inequal_distribution: list[float],
        high_end_inequal_distribution: list[float],
    ) -> None:
        small_alpha = 2
        large_alpha = 20

        ge_1 = idx.generalized_entropy(low_end_inequal_distribution, small_alpha)
        ge_2 = idx.generalized_entropy(low_end_inequal_distribution, large_alpha)
        assert ge_1 > ge_2
        print(f"GE - Low End Inequality, Small Alpha: {ge_1}")
        print(f"GE - Low End Inequality, Large Alpha: {ge_2}")

        ge_1 = idx.generalized_entropy(high_end_inequal_distribution, small_alpha)
        ge_2 = idx.generalized_entropy(high_end_inequal_distribution, large_alpha)
        assert ge_1 < ge_2
        print(f"GE - High End Inequality, Small Alpha: {ge_1}")
        print(f"GE - High End Inequality, Large Alpha: {ge_2}")


class TestTheil:
    def test_equality(
        self,
        small_equal_distribution: list[float],
        large_equal_distribution: list[float],
    ) -> None:
        tl_1 = idx.theil_l(small_equal_distribution)
        tl_2 = idx.theil_l(large_equal_distribution)
        assert math.isclose(tl_1, 0, abs_tol=1e-15)
        assert math.isclose(tl_2, 0, abs_tol=1e-15)

        tt_1 = idx.theil_t(small_equal_distribution)
        tt_2 = idx.theil_t(large_equal_distribution)
        assert math.isclose(tt_1, 0, abs_tol=1e-15)
        assert math.isclose(tt_2, 0, abs_tol=1e-15)

    def test_inequality(
        self,
        inequal_distribution: list[float],
        very_inequal_distribution: list[float],
    ) -> None:
        tl_1 = idx.theil_l(inequal_distribution)
        tl_2 = idx.theil_l(very_inequal_distribution)
        assert tl_1 < tl_2

        tt_1 = idx.theil_t(inequal_distribution)
        tt_2 = idx.theil_t(very_inequal_distribution)
        assert tt_1 < tt_2

    def test_sensitivity(
        self,
        low_end_inequal_distribution: list[float],
        high_end_inequal_distribution: list[float],
    ) -> None:
        tl = idx.theil_l(low_end_inequal_distribution)
        tt = idx.theil_t(low_end_inequal_distribution)
        assert tl > tt
        print(f"TL - Low End Inequality: {tl}")
        print(f"TT - Low End Inequality: {tt}")

        tl = idx.theil_l(high_end_inequal_distribution)
        tt = idx.theil_t(high_end_inequal_distribution)
        assert tl < tt
        print(f"TL - High End Inequality: {tl}")
        print(f"TT - High End Inequality: {tt}")


class TestHHI:
    def test_equality(
        self,
        small_equal_distribution: list[float],
        large_equal_distribution: list[float],
    ) -> None:
        hhi_1 = idx.herfindahl_hirschman(small_equal_distribution)
        hhi_2 = idx.herfindahl_hirschman(large_equal_distribution)
        assert hhi_1 > hhi_2
        assert math.isclose(hhi_1, 0.20, abs_tol=1e-10)
        assert math.isclose(hhi_2, 0.01, abs_tol=1e-10)
        print(f"HHI - Small Equal Distribution: {hhi_1}")
        print(f"HHI - Large Equal Distribution: {hhi_2}")

    def test_inequality(
        self,
        inequal_distribution: list[float],
        very_inequal_distribution: list[float],
    ) -> None:
        hhi_1 = idx.herfindahl_hirschman(inequal_distribution)
        hhi_2 = idx.herfindahl_hirschman(very_inequal_distribution)
        assert hhi_1 < hhi_2
        assert math.isclose(hhi_1, 0.136, abs_tol=1e-10)
        assert math.isclose(hhi_2, 0.643, abs_tol=1e-10)
        print(f"HHI - Low Inequality: {hhi_1}")
        print(f"HHI - High Inequality: {hhi_2}")
