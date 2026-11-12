import copy
import math
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pytest

from pposdex import plots
from pposdex.plots import Line, TimeseriesChart, TimeseriesPanel
from pposdex.ppos_dex_data import SCHEMA, PPoSDexData
from pposdex.theme import LIGHT, use

TIMESERIES = [
    "accounts_prt",
    "algo_dynamics",
    "algo_inequality",
    "ppos_dex",
    "ppos_dex_v3",
    "ppos_inequality_b",
    "ppos_inequality_unb",
]
SNAPSHOT = [
    "algo_dynamics",
    "ppos_dex",
    "ppos_dex_v3",
    "ppos_dex_v3_operators",
    "ppos_inequality",
    "validators",
]


def svgs(names: list[str]) -> list[str]:
    """Light and dark variants of the charts"""
    return sorted(f"{name}{suffix}.svg" for name in names for suffix in ("", ".dark"))


@pytest.fixture
def data(make_data_point: Callable[..., PPoSDexData]) -> list[PPoSDexData]:
    # Newest first, as published; the oldest predate the optional metrics
    old = make_data_point(timestamp="2021-01-01 00:00:00.000000")
    for key in ("algo_hhi", "ppos_hhi", "ppos_dex_v2"):
        del old[key]  # type: ignore[misc]
    return [
        make_data_point(timestamp=f"2026-11-0{day} 00:00:00.000000")
        for day in (3, 2, 1)
    ] + [old]


@pytest.mark.parametrize(
    ("plot", "kind", "expected"),
    [
        (plots.timeseries, "timeseries", TIMESERIES),
        (plots.snapshot, "snapshot", SNAPSHOT),
    ],
    ids=["timeseries", "snapshot"],
)
def test_save(
    plot: Callable[[list[PPoSDexData], bool], None],
    kind: str,
    expected: list[str],
    data: list[PPoSDexData],
    images: Path,
) -> None:
    original = copy.deepcopy(data)
    plot(data, True)
    assert sorted(p.name for p in (images / kind).iterdir()) == svgs(expected)
    assert data == original
    assert not plt.get_fignums()


def test_svg_keeps_text(data: list[PPoSDexData], images: Path) -> None:
    plots.snapshot(data, True)
    svg = (images / "snapshot" / "ppos_dex.svg").read_text()
    # Text is rendered by the browser, in the system font
    assert "PPoS Dex" in svg
    assert "system-ui" in svg


def test_snapshot_without_optional_metrics(
    data: list[PPoSDexData], images: Path
) -> None:
    plots.snapshot(data[-1:], True)
    assert sorted(p.name for p in (images / "snapshot").iterdir()) == svgs(SNAPSHOT)


@pytest.mark.parametrize(
    ("plot", "charts"),
    [(plots.timeseries, len(TIMESERIES)), (plots.snapshot, len(SNAPSHOT))],
    ids=["timeseries", "snapshot"],
)
def test_show(
    plot: Callable[[list[PPoSDexData], bool], None],
    charts: int,
    data: list[PPoSDexData],
    images: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    shown: list[None] = []
    monkeypatch.setattr(plt, "show", lambda: shown.append(None))
    plot(data, False)
    assert len(shown) == charts
    assert not images.exists()


@pytest.mark.parametrize(
    ("value", "expected"),
    [(0.0096, "1.0%"), (0.2, "20%"), (1, "100%")],
)
def test_percent(value: float, expected: str) -> None:
    assert plots.percent(value) == expected


def test_line_value(make_data_point: Callable[..., PPoSDexData]) -> None:
    data = make_data_point()
    del data["ppos_hhi"]
    assert Line("ppos_gini", "").value(data) == 0.9
    assert math.isnan(Line("ppos_hhi", "").value(data))
    assert Line(lambda d: 2 * d["ppos_gini"], "").value(data) == 1.8


class TestSeries:
    def test_breaks_where_data_is_missing(self, data: list[PPoSDexData]) -> None:
        dates, values = plots.series(data[::-1], Line("ppos_gini", ""))
        # A gap point between 2021 and 2026, then the three days
        assert len(dates) == len(values) == 5
        assert math.isnan(values[1])
        assert dates[0] < dates[1] < dates[2]

    def test_no_data_periods(self) -> None:
        dates = [datetime(2026, 1, d) for d in (1, 2)] + [datetime(2026, 3, 1)]
        assert plots.no_data_periods(dates) == [(dates[1], dates[2])]


@pytest.mark.parametrize(
    ("positions", "expected"),
    [
        ([0.5], [0.5]),
        ([0.1, 0.9], [0.1, 0.9]),
        ([0.5, 0.52], [0.5, 0.6]),
        ([0.52, 0.5, 0.51], [0.7, 0.5, 0.6]),
    ],
)
def test_dodge(positions: list[float], expected: list[float]) -> None:
    assert plots.dodge(positions, 0.1) == pytest.approx(expected)


@pytest.mark.parametrize(
    "value",
    [lambda d: d["accounts"], lambda _: math.nan],
    ids=["values", "no_values"],
)
def test_log_panel(
    value: Callable[[PPoSDexData], float], data: list[PPoSDexData], images: Path
) -> None:
    panel = TimeseriesPanel("", (Line(value, ""),), fmt=str, log=True)
    plots.plot_timeseries(TimeseriesChart("log", "Log", (panel,)), data, True, images)
    assert (images / "log.svg").exists()


def test_snap_subtitle(make_data_point: Callable[..., PPoSDexData]) -> None:
    data = make_data_point(accounts=147633)
    assert plots.snap_subtitle(data) == (
        "3 Nov 2026  ·  147,633 accounts holding more than 1,000 ALGO"
    )


class TestPanelsWithData:
    def test_metrics_not_published_yet_are_left_out(
        self, data: list[PPoSDexData]
    ) -> None:
        chart = next(c for c in plots.TIMESERIES if c.name == "ppos_dex_v3")
        data[0]["ppos_dex_v3_liveness"] = 7
        with use(LIGHT):
            accounts = plots.timeseries_figure(chart, data[::-1], LIGHT)
            data[0]["ppos_dex_v3_liveness_operators"] = 2
            operators = plots.timeseries_figure(chart, data[::-1], LIGHT)
        assert (len(accounts.axes), len(operators.axes)) == (1, 2)
        plt.close("all")

    def test_chart_starts_with_its_first_data(self, data: list[PPoSDexData]) -> None:
        chart = next(c for c in plots.TIMESERIES if c.name == "ppos_dex_v3")
        # Published since 2 Nov 2026, the oldest data point is from 2021
        data[0]["ppos_dex_v3_liveness"] = 7
        data[1]["ppos_dex_v3_liveness"] = 7
        with use(LIGHT):
            fig = plots.timeseries_figure(chart, data[::-1], LIGHT)
        start = mdates.num2date(fig.axes[0].get_xlim()[0]).replace(tzinfo=None)
        assert start > datetime(2026, 10, 1)
        plt.close("all")

    def test_chart_without_data_keeps_its_panels(self, data: list[PPoSDexData]) -> None:
        panel = TimeseriesPanel("", (Line(lambda _: math.nan, ""),))
        with use(LIGHT):
            fig = plots.timeseries_figure(
                TimeseriesChart("empty", "Empty", (panel,)), data, LIGHT
            )
        assert len(fig.axes) == 1
        plt.close("all")


def test_v3_snapshot_shows_the_published_coefficients(
    make_data_point: Callable[..., PPoSDexData],
) -> None:
    # Published by 4.0.0, the liveness coefficient alone
    legacy = make_data_point(ppos_dex_v3_liveness=7, ppos_dex_v3_liveness_operators=2)
    coefficients = {key: 7 for key in SCHEMA if key.startswith("ppos_dex_v3")}
    for name in ("ppos_dex_v3", "ppos_dex_v3_operators"):
        chart = next(c for c in plots.SNAPSHOTS if c.name == name)
        with use(LIGHT):
            figures = [
                plots.snapshot_figure(chart, data, LIGHT)
                for data in (make_data_point(), legacy, make_data_point(**coefficients))
            ]
        # Each bar is a track and its fill: one chart by account, one by operator
        assert [len(fig.axes[0].patches) for fig in figures] == [0, 2, 8]
        plt.close("all")


class TestStakes:
    @staticmethod
    def figure_texts(amounts: list[int]) -> tuple[int, list[str]]:
        online = [
            {"address": f"ACCOUNT{i}", "amount": amount, "status": "Online"}
            for i, amount in enumerate(amounts)
        ]
        with use(LIGHT):
            fig = plots.stakes_figure(online, 1000, datetime(2026, 11, 11), LIGHT)
        account_axes = fig.axes[0]
        boxes = len(account_axes.patches)
        texts = [t.get_text() for t in account_axes.texts]
        plt.close(fig)
        return boxes, texts

    def test_small_validators_are_drawn_together(self) -> None:
        boxes, texts = self.figure_texts([10_000] * 9 + [1] * 50)
        assert boxes == 10
        assert texts == ["Gray: 50 accounts under 0.1% each, together 0%"]

    def test_no_box_for_small_validators_when_none(self) -> None:
        boxes, texts = self.figure_texts([1] * 20)
        assert boxes == 20
        assert texts == []

    def test_save(self, images: Path) -> None:
        plots.stakes([{"address": "A", "amount": 1, "status": "Online"}], 1000, True)
        assert sorted(p.name for p in (images / "snapshot").iterdir()) == svgs(
            ["stakes"]
        )
