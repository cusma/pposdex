"""
PPoS Dex plots
"""

import math
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import partial
from itertools import pairwise
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter, NullFormatter, PercentFormatter

from pposdex.ppos_dex_data import (
    Metric,
    PPoSDexData,
    effective_validators,
    equal_stake_validators,
    online_accounts,
)
from pposdex.theme import Theme, output, title

TIMESERIES_DIR = Path("./docs/images/timeseries")
SNAPSHOT_DIR = Path("./docs/images/snapshot")

# Longer periods without data are shaded, and their lines broken
NO_DATA = timedelta(days=30)
# Minimum vertical distance between line end labels, as a fraction of the axes
LABEL_GAP = 0.14
# Line end labels take the figure width on the right of this fraction
LABELS_LEFT = 0.8

type Format = Callable[[float], str]
type Value = Callable[[PPoSDexData], float]


def percent(value: float) -> str:
    return f"{value:.1%}" if value < 0.1 else f"{value:.0%}"


def decimal(value: float) -> str:
    return f"{value:.3g}"


def count(value: float) -> str:
    return f"{value:,.0f}"


@dataclass(frozen=True)
class Line:
    # A published metric, or a value derived from the data point
    key: Metric | Value
    label: str

    def value(self, data: PPoSDexData) -> float:
        if callable(self.key):
            return self.key(data)
        # Missing data points are plotted as gaps
        return data.get(self.key, math.nan)


@dataclass(frozen=True)
class TimeseriesPanel:
    subtitle: str
    lines: tuple[Line, ...]
    y_max: float | None = None
    fmt: Format = decimal
    log: bool = False


@dataclass(frozen=True)
class TimeseriesChart:
    name: str
    title: str
    panels: tuple[TimeseriesPanel, ...]


@dataclass(frozen=True)
class Bar:
    label: str
    # A published metric, or a value derived from the data point
    key: Metric | Value
    x_max: Callable[[PPoSDexData], float]
    fmt: Format = decimal
    # Other keys the bar needs, it is not drawn if any of them is missing
    requires: tuple[Metric, ...] = ()

    def value(self, data: PPoSDexData) -> float:
        return Line(self.key, self.label).value(data)


@dataclass(frozen=True)
class SnapshotChart:
    name: str
    title: str
    subtitle: str
    bars: tuple[Bar, ...]


def _x_max_unit(_: PPoSDexData) -> float:
    return 1


def _x_max_theil(data: PPoSDexData) -> float:
    return round(max(data["ppos_theil_l"], data["ppos_theil_t"])) + 1


EQUALITY = "0 = complete equality"
DECENTRALIZATION = "1 = perfect decentralization"

TIMESERIES = (
    TimeseriesChart(
        name="algo_dynamics",
        title="ALGO Dynamics",
        panels=(
            TimeseriesPanel(
                subtitle="100% = full circulation or complete participation",
                lines=(
                    Line("algo_dynamics", "ALGO Supply"),
                    Line("ppos_online_stake", "ALGO Participation in PPoS"),
                ),
                y_max=1,
                fmt=percent,
            ),
        ),
    ),
    TimeseriesChart(
        name="algo_inequality",
        title="ALGO Inequality",
        panels=(TimeseriesPanel(EQUALITY, (Line("algo_hhi", "HHI"),)),),
    ),
    TimeseriesChart(
        name="ppos_inequality_b",
        title="Validators Stake Inequality (Bounded)",
        panels=(
            TimeseriesPanel(
                EQUALITY,
                (Line("ppos_gini", "Gini Index"), Line("ppos_hhi", "HHI")),
                y_max=1,
            ),
        ),
    ),
    TimeseriesChart(
        name="ppos_inequality_unb",
        title="Validators Stake Inequality (Unbounded)",
        panels=(
            TimeseriesPanel(
                EQUALITY,
                (
                    Line("ppos_theil_l", "Theil L Index"),
                    Line("ppos_theil_t", "Theil T Index"),
                ),
            ),
        ),
    ),
    TimeseriesChart(
        name="ppos_dex",
        title="PPoS Dex",
        panels=(
            TimeseriesPanel(DECENTRALIZATION, (Line("ppos_dex", "PPoS Dex V1"),)),
            TimeseriesPanel(DECENTRALIZATION, (Line("ppos_dex_v2", "PPoS Dex V2"),)),
            TimeseriesPanel(
                "Fewest online accounts holding more than 20% of the online stake",
                (
                    Line("ppos_dex_v3", "PPoS Dex V3"),
                    Line("ppos_dex_v3_operators", "V3 Operators"),
                ),
                fmt=count,
            ),
        ),
    ),
)

SNAPSHOTS = (
    SnapshotChart(
        name="algo_dynamics",
        title="ALGO Dynamics",
        subtitle="100% = full circulation",
        bars=(Bar("ALGO Supply", "algo_dynamics", _x_max_unit, percent),),
    ),
    SnapshotChart(
        name="ppos_inequality",
        title="Validators Stake Inequality",
        subtitle=EQUALITY,
        bars=(
            Bar("Gini Index", "ppos_gini", _x_max_unit),
            Bar("HHI", "ppos_hhi", _x_max_unit),
            # Theil indexes are unbounded: shown only together, on the same scale
            Bar(
                "Theil L Index",
                "ppos_theil_l",
                _x_max_theil,
                requires=("ppos_theil_t",),
            ),
            Bar(
                "Theil T Index",
                "ppos_theil_t",
                _x_max_theil,
                requires=("ppos_theil_l",),
            ),
        ),
    ),
    SnapshotChart(
        name="ppos_dex",
        title="PPoS Dex",
        subtitle=DECENTRALIZATION,
        bars=(
            Bar("PPoS Dex v1", "ppos_dex", _x_max_unit),
            Bar("PPoS Dex v2", "ppos_dex_v2", _x_max_unit),
        ),
    ),
    SnapshotChart(
        name="validators",
        title="Validators",
        subtitle=(
            "Online accounts, the equal-stake validators they are worth, and the "
            "fewest holding more than 20% of the online stake"
        ),
        bars=(
            Bar("Online Accounts", online_accounts, online_accounts, count),
            Bar("Entropy Equivalent", effective_validators, online_accounts, count),
            Bar("HHI Equivalent", equal_stake_validators, online_accounts, count),
            Bar("PPoS Dex V3", "ppos_dex_v3", online_accounts, count),
            Bar(
                "PPoS Dex V3 Operators", "ppos_dex_v3_operators", online_accounts, count
            ),
        ),
    ),
)


def timestamp(data: PPoSDexData) -> datetime:
    return datetime.fromisoformat(data["timestamp"])


def no_data_periods(dates: list[datetime]) -> list[tuple[datetime, datetime]]:
    return [(a, b) for a, b in pairwise(dates) if b - a > NO_DATA]


def series(
    ppos_dex_data: list[PPoSDexData], line: Line
) -> tuple[list[datetime], list[float]]:
    """Dates and values of a metric, broken where data is missing"""
    dates: list[datetime] = []
    values: list[float] = []
    for data in ppos_dex_data:
        date = timestamp(data)
        if dates and date - dates[-1] > NO_DATA:
            dates.append(dates[-1] + (date - dates[-1]) / 2)
            values.append(math.nan)
        dates.append(date)
        values.append(line.value(data))
    return dates, values


def dodge(positions: list[float], gap: float) -> list[float]:
    """Spread positions at least `gap` apart, keeping their order"""
    order = sorted(range(len(positions)), key=lambda i: positions[i])
    spread = list(positions)
    for previous, current in pairwise(order):
        spread[current] = max(spread[current], spread[previous] + gap)
    return spread


def shade_no_data(ax: Axes, dates: list[datetime], theme: Theme) -> None:
    for start, end in no_data_periods(dates):
        x0, x1 = mdates.date2num(start), mdates.date2num(end)
        ax.axvspan(x0, x1, color=theme.track, linewidth=0, zorder=0)
        ax.text(
            (x0 + x1) / 2,
            0.5,
            "No data",
            transform=ax.get_xaxis_transform(),
            ha="center",
            va="center",
            color=theme.muted,
            fontsize=9,
        )


def label_line_ends(
    ax: Axes, ends: list[tuple[str, float, str]], fmt: Format, theme: Theme
) -> None:
    """Name each line, with its latest value, next to where it ends"""
    # Data to axes fraction, through the axis scale (linear or log)
    to_axes = ax.transScale + ax.transLimits
    points = [float(to_axes.transform((0, value))[1]) for _, value, _ in ends]
    for (label, value, color), y in zip(ends, dodge(points, LABEL_GAP), strict=True):
        ax.plot(
            [1.015, 1.04],
            [y, y],
            transform=ax.transAxes,
            color=color,
            linewidth=3,
            clip_on=False,
        )
        ax.text(
            1.05,
            y,
            fmt(value),
            transform=ax.transAxes,
            va="bottom",
            fontweight="bold",
            fontsize=11,
            color=theme.ink,
        )
        ax.text(
            1.05,
            y,
            label,
            transform=ax.transAxes,
            va="top",
            fontsize=9,
            color=theme.ink_secondary,
        )


def _value_axis(ax: Axes, panel: TimeseriesPanel, values: list[float]) -> None:
    if panel.log:
        ax.set_yscale("log")
        ax.yaxis.set_minor_formatter(NullFormatter())
        finite = [v for v in values if v > 0]
        if finite:
            ax.set_ylim(min(finite) / 1.5, max(finite) * 1.5)
    else:
        ax.set_ylim(0, panel.y_max)
        if panel.y_max is None:
            ax.set_ylim(0, ax.get_ylim()[1] * 1.05)
    if panel.fmt is percent:
        ax.yaxis.set_major_formatter(PercentFormatter(1))
    elif panel.fmt is not decimal:
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: panel.fmt(v)))


def date_axis(ax: Axes) -> None:
    locator = mdates.AutoDateLocator(minticks=4, maxticks=8)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))


def has_data(ppos_dex_data: list[PPoSDexData], value: Value) -> bool:
    """Whether any data point has the value, like metrics added later"""
    return any(not math.isnan(value(data)) for data in ppos_dex_data)


def timeseries_figure(
    chart: TimeseriesChart, ppos_dex_data: list[PPoSDexData], theme: Theme
) -> Figure:
    # Panels of metrics not published yet are left out
    panels = [
        panel
        for panel in chart.panels
        if any(has_data(ppos_dex_data, line.value) for line in panel.lines)
    ] or list(chart.panels)
    fig, axes = plt.subplots(
        len(panels),
        1,
        sharex=True,
        squeeze=False,
        figsize=(9, 1.2 + 3.2 * len(panels)),
        layout="constrained",
    )
    title(fig, chart.title, theme)
    dates = [timestamp(d) for d in ppos_dex_data]
    for ax, panel in zip(axes[:, 0], panels, strict=True):
        ax.set_title(panel.subtitle)
        shade_no_data(ax, dates, theme)
        ends: list[tuple[str, float, str]] = []
        values: list[float] = []
        for line, color in zip(panel.lines, theme.series, strict=False):
            x, y = series(ppos_dex_data, line)
            ax.plot(x, y, color=color)
            values += y
            last = next((v for v in reversed(y) if not math.isnan(v)), None)
            if last is not None:
                ends.append((line.label, last, color))
        _value_axis(ax, panel, values)
        date_axis(ax)
        label_line_ends(ax, ends, panel.fmt, theme)
    # Room for the line end labels
    fig.get_layout_engine().set(rect=(0, 0, LABELS_LEFT, 1))  # type: ignore[union-attr,call-arg]
    return fig


def plot_timeseries(
    chart: TimeseriesChart,
    ppos_dex_data: list[PPoSDexData],
    save: bool = False,
    directory: Path = TIMESERIES_DIR,
) -> None:
    figure = partial(timeseries_figure, chart, ppos_dex_data)
    output(figure, directory / chart.name, save)


def snap_subtitle(data: PPoSDexData) -> str:
    date = f"{timestamp(data):%-d %b %Y}"
    return (
        f"{date}  ·  {data['accounts']:,} accounts holding "
        f"at least {data['algo_threshold']:,} ALGO"
    )


def snapshot_figure(chart: SnapshotChart, data: PPoSDexData, theme: Theme) -> Figure:
    bars = [
        bar
        for bar in chart.bars
        if not math.isnan(bar.value(data))
        and all(data.get(key) is not None for key in bar.requires)
    ]
    fig, ax = plt.subplots(figsize=(9, 1.5 + 0.8 * len(bars)), layout="constrained")
    title(fig, chart.title, theme)
    ax.set_title(f"{chart.subtitle}\n{snap_subtitle(data)}", linespacing=1.6)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(len(bars) - 0.4, -0.9)
    for row, bar in enumerate(bars):
        value = bar.value(data)
        x_max = bar.x_max(data)
        ax.barh(row, 1, height=0.22, color=theme.track)
        ax.barh(row, value / x_max, height=0.22, color=theme.series[0])
        ax.text(0, row - 0.24, bar.label, va="bottom", color=theme.ink_secondary)
        ax.text(
            1,
            row - 0.24,
            bar.fmt(value),
            ha="right",
            va="bottom",
            fontweight="bold",
            fontsize=12,
        )
        ax.text(
            1,
            row + 0.16,
            f"of {bar.fmt(x_max)}",
            ha="right",
            va="top",
            color=theme.muted,
            fontsize=8,
        )
    return fig


def plot_snapshot(chart: SnapshotChart, data: PPoSDexData, save: bool = False) -> None:
    figure = partial(snapshot_figure, chart, data)
    output(figure, SNAPSHOT_DIR / chart.name, save)


def timeseries(ppos_dex_data: list[PPoSDexData], save: bool = False) -> None:
    # Published data comes newest first, plot it in chronological order
    chronological = ppos_dex_data[::-1]
    for chart in TIMESERIES:
        plot_timeseries(chart, chronological, save)


def snapshot(ppos_dex_data: list[PPoSDexData], save: bool = False) -> None:
    latest = ppos_dex_data[0]
    for chart in SNAPSHOTS:
        plot_snapshot(chart, latest, save)
