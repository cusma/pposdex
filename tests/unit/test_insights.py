import math
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pytest

from pposdex import insights, plots
from pposdex.insights import Indicator
from pposdex.ppos_dex_data import PPoSDexData

CHARTS = [
    "at_a_glance",
    "effective_holders",
    "effective_validators",
    "monthly_change",
    "online_stake",
    "trajectory",
]

GINI = Indicator("ppos_gini", "Gini", higher_is_better=False)
DEX = Indicator("ppos_dex", "Dex", higher_is_better=True)


@pytest.fixture
def data(make_data_point: Callable[..., PPoSDexData]) -> list[PPoSDexData]:
    # Newest first, as published: two years, with a long gap without data.
    # The accounts double in the last year, the online ones too
    days = [
        ("2026-11-03", 0.03, 200),
        ("2026-10-15", 0.03, 200),
        ("2025-11-01", 0.02, 100),
        ("2025-01-01", 0.02, 100),
        ("2023-09-01", 0.01, 100),
        ("2022-01-01", 0.01, 100),
    ]
    return [
        make_data_point(
            timestamp=f"{day} 00:00:00.000000",
            ppos_dex=dex,
            accounts=accounts,
            ppos_online_accounts=0.1,
        )
        for day, dex, accounts in days
    ]


def test_render(data: list[PPoSDexData], images: Path) -> None:
    insights.render(data, True)
    expected = sorted(f"{n}{s}.svg" for n in CHARTS for s in ("", ".dark"))
    assert sorted(p.name for p in (images / "insights").iterdir()) == expected
    assert not plt.get_fignums()


def test_render_short_history(
    data: list[PPoSDexData], images: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # No data a year before, and an odd number of tiles at a glance
    monkeypatch.setattr(insights, "INDICATORS", insights.INDICATORS[:3])
    insights.render(data[:2], True)
    assert (images / "insights" / "at_a_glance.svg").exists()


def test_show(
    data: list[PPoSDexData], images: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    shown: list[None] = []
    monkeypatch.setattr(plt, "show", lambda: shown.append(None))
    insights.render(data)
    assert len(shown) == len(CHARTS)
    assert not images.exists()


class TestDerivedMetrics:
    def test_online_accounts(self, make_data_point: Callable[..., PPoSDexData]) -> None:
        data = make_data_point(accounts=1000, ppos_online_accounts=0.1)
        assert insights.online_accounts(data) == pytest.approx(100)

    def test_effective_validators(
        self, make_data_point: Callable[..., PPoSDexData]
    ) -> None:
        # Equal stakes: Theil T is 0, all online accounts count
        equal = make_data_point(accounts=100, ppos_online_accounts=1, ppos_theil_t=0)
        assert insights.effective_validators(equal) == pytest.approx(100)
        unequal = make_data_point(
            accounts=100, ppos_online_accounts=1, ppos_theil_t=math.log(4)
        )
        assert insights.effective_validators(unequal) == pytest.approx(25)

    def test_equal_stake_validators(
        self, make_data_point: Callable[..., PPoSDexData]
    ) -> None:
        assert insights.equal_stake_validators(
            make_data_point(ppos_hhi=0.02)
        ) == pytest.approx(50)
        data = make_data_point()
        del data["ppos_hhi"]
        assert math.isnan(insights.equal_stake_validators(data))

    def test_effective_holders(
        self, make_data_point: Callable[..., PPoSDexData]
    ) -> None:
        assert insights.effective_holders(
            make_data_point(algo_hhi=0.0125)
        ) == pytest.approx(80)
        data = make_data_point()
        del data["algo_hhi"]
        assert math.isnan(insights.effective_holders(data))

    def test_algo(self, make_data_point: Callable[..., PPoSDexData]) -> None:
        data = make_data_point(algo_dynamics=0.5, ppos_online_stake=0.2)
        assert insights.circulating_algo(data) == pytest.approx(5 * 10**9)
        assert insights.online_algo(data) == pytest.approx(10**9)

    @pytest.mark.parametrize(
        ("value", "expected"),
        [(plots.count, "1,410"), (insights.billions, "0.00B")],
    )
    def test_formats(self, value: Callable[[float], str], expected: str) -> None:
        assert value(1410) == expected


@pytest.mark.parametrize(
    ("indicator", "expected"),
    [(DEX, 0.5), (GINI, -0.5)],
    ids=["higher_is_better", "lower_is_better"],
)
def test_change(indicator: Indicator, expected: float) -> None:
    assert insights.change(2, 3, indicator.higher_is_better) == expected


class TestYearChange:
    def test_change(self, data: list[PPoSDexData]) -> None:
        # 2025-11-01 is within the tolerance of a year before 2026-11-03
        assert insights.year_change(data[::-1], DEX.value) == pytest.approx(0.5)

    def test_towards_decentralization(self, data: list[PPoSDexData]) -> None:
        data[0]["ppos_gini"] = 0.6
        data[2]["ppos_gini"] = 0.4
        change = insights.year_change(data[::-1], GINI.value, higher_is_better=False)
        assert change == pytest.approx(-0.5)

    def test_no_data_a_year_before(self, data: list[PPoSDexData]) -> None:
        assert insights.year_change(data[:2][::-1], DEX.value) is None

    def test_missing_metric(self, data: list[PPoSDexData]) -> None:
        del data[2]["ppos_hhi"]
        hhi = Indicator("ppos_hhi", "HHI", higher_is_better=False)
        assert insights.year_change(data[::-1], hhi.value) is None


def test_weekly(make_data_point: Callable[..., PPoSDexData]) -> None:
    # Two days of one week, then one day after two months without data
    days = ["2026-01-05", "2026-01-07", "2026-03-09"]
    data = [
        make_data_point(timestamp=f"{day} 00:00:00.000000", accounts=accounts)
        for day, accounts in zip(days, (100, 300, 500), strict=True)
    ]
    dates, xs, ys = insights.weekly(
        data, insights.total_accounts, insights.total_accounts
    )
    assert xs[0] == ys[0] == 200
    assert math.isnan(xs[1])
    assert dates[0] == datetime(2026, 1, 7)
    assert dates[2] == datetime(2026, 3, 9)


def test_monthly_changes(data: list[PPoSDexData]) -> None:
    months, rows = insights.monthly_changes(data[::-1])
    assert months[0] == datetime(2022, 1, 1)
    assert months[-1] == datetime(2026, 11, 1)
    assert len(rows) == len(insights.HEATMAP)
    dex = rows[[i.key for i in insights.HEATMAP].index("ppos_dex")]
    # Changes need data in the month before
    assert math.isnan(dex[0])
    assert dex[months.index(datetime(2026, 11, 1))] == pytest.approx(0)
    assert math.isnan(dex[months.index(datetime(2025, 2, 1))])


@pytest.mark.parametrize(
    ("date", "expected"),
    [
        (datetime(2026, 1, 31), datetime(2026, 2, 1)),
        (datetime(2026, 12, 5), datetime(2027, 1, 1)),
    ],
)
def test_next_month(date: datetime, expected: datetime) -> None:
    assert insights.next_month(date) == expected
