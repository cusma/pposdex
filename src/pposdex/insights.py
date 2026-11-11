"""
PPoS Dex insights: views derived from the published data, for the docs

Run `python -m pposdex.insights` to save them in `./docs/images/insights`.
"""

import math
import statistics
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import partial
from itertools import pairwise
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.axis import Axis
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.figure import Figure
from matplotlib.ticker import (
    FuncFormatter,
    LogLocator,
    NullFormatter,
    PercentFormatter,
)

from pposdex import cli, networks
from pposdex import ppos_dex_data as pposdex
from pposdex.plots import (
    NO_DATA,
    Format,
    Line,
    TimeseriesChart,
    TimeseriesPanel,
    Value,
    count,
    date_axis,
    decimal,
    has_data,
    no_data_periods,
    percent,
    plot_timeseries,
    series,
    timestamp,
)
from pposdex.ppos_dex_data import (
    Metric,
    PPoSDexData,
    effective_validators,
    equal_stake_validators,
    online_accounts,
)
from pposdex.theme import Theme, output, title

INSIGHTS_DIR = Path("./docs/images/insights")
MICROALGO_GENESIS_SUPPLY = pposdex.MICROALGO_TOTAL_SUPPLY
MICROALGOS_PER_ALGO = 10**6

YEAR = timedelta(days=365)
# How far from one year ago a data point can be, to compare with the latest
YEAR_TOLERANCE = timedelta(days=15)
# Monthly changes beyond this are shown with the strongest color
MAX_CHANGE = 0.2
# Smaller yearly changes round to zero: shown as no change
NO_CHANGE = 0.0005


def total_accounts(data: PPoSDexData) -> float:
    """Accounts holding at least the threshold"""
    return data["accounts"]


def circulating_algo(data: PPoSDexData) -> float:
    supply = data["algo_dynamics"] * MICROALGO_GENESIS_SUPPLY
    return supply / MICROALGOS_PER_ALGO


def online_algo(data: PPoSDexData) -> float:
    return circulating_algo(data) * data["ppos_online_stake"]


def effective_holders(data: PPoSDexData) -> float:
    """Equal holders with the same HHI as all the accounts"""
    hhi = data.get("algo_hhi")
    return 1 / hhi if hhi else math.nan


def billions(value: float) -> str:
    return f"{value / 10**9:.2f}B"


@dataclass(frozen=True)
class Indicator:
    # A published metric, or a value derived from the data point
    key: Metric | Value
    label: str
    # Whether a higher value means more decentralization
    higher_is_better: bool
    fmt: Format = decimal

    def value(self, data: PPoSDexData) -> float:
        return Line(self.key, self.label).value(data)


# Absolute numbers: they grow with the network, ratios can hide that
ABSOLUTE = (
    Indicator(online_accounts, "Online Accounts", True, count),
    Indicator(online_algo, "Online Stake", True, billions),
    Indicator(effective_validators, "Effective Validators", True, count),
)
# What the network grows with: holders and supply
CONTEXT = (
    Indicator(total_accounts, "Accounts", True, count),
    Indicator(circulating_algo, "Circulating Supply", True, billions),
)
INDICATORS = (
    Indicator("ppos_dex_v3_liveness", "PPoS Dex V3", True, count),
    Indicator("ppos_dex_v3_liveness_operators", "PPoS Dex V3 Operators", True, count),
    Indicator("ppos_dex_v2", "PPoS Dex V2", True),
    Indicator("ppos_dex", "PPoS Dex V1", True),
    Indicator("algo_dynamics", "ALGO Supply", True, percent),
    Indicator("ppos_gini", "Gini Index", False),
    Indicator("ppos_hhi", "HHI", False),
    Indicator("ppos_theil_l", "Theil L Index", False),
    Indicator("ppos_theil_t", "Theil T Index", False),
    Indicator("algo_hhi", "ALGO HHI", False),
)
HEATMAP = (*ABSOLUTE, *CONTEXT, *INDICATORS)

TIMESERIES = (
    TimeseriesChart(
        name="effective_validators",
        title="Effective Validators",
        panels=(
            TimeseriesPanel(
                "Online accounts, and how many equal-stake validators "
                "their stake is worth (log scale)",
                (
                    Line(online_accounts, "Online Accounts"),
                    Line(effective_validators, "Entropy Equivalent"),
                    Line(equal_stake_validators, "HHI Equivalent"),
                ),
                fmt=count,
                log=True,
            ),
        ),
    ),
    TimeseriesChart(
        name="online_stake",
        title="Online Stake",
        panels=(
            TimeseriesPanel(
                "ALGO in circulation, and online for consensus",
                (
                    Line(circulating_algo, "Circulating Supply"),
                    Line(online_algo, "Online Stake"),
                ),
                fmt=billions,
            ),
        ),
    ),
    TimeseriesChart(
        name="effective_holders",
        title="Effective Holders",
        panels=(
            TimeseriesPanel(
                f"How many equal holders the ALGO of the accounts holding at least "
                f"{cli.DEFAULT_ALGO_THRESHOLD:,} ALGO is worth (HHI equivalent)",
                (Line(effective_holders, "Effective Holders"),),
                fmt=count,
            ),
        ),
    ),
)


def change(old: float, new: float, higher_is_better: bool) -> float:
    """Relative change, positive when towards more decentralization"""
    relative = (new - old) / old
    return relative if higher_is_better else -relative


def year_ago(ppos_dex_data: list[PPoSDexData]) -> PPoSDexData | None:
    """The data point about one year before the latest one"""
    target = timestamp(ppos_dex_data[-1]) - YEAR
    past = min(ppos_dex_data, key=lambda d: abs(timestamp(d) - target))
    return past if abs(timestamp(past) - target) <= YEAR_TOLERANCE else None


def year_change(
    ppos_dex_data: list[PPoSDexData], value: Value, higher_is_better: bool = True
) -> float | None:
    """Change of the latest value since about one year before"""
    past = year_ago(ppos_dex_data)
    if past is None:
        return None
    old, new = value(past), value(ppos_dex_data[-1])
    if math.isnan(old) or math.isnan(new) or not old:
        return None
    return change(old, new, higher_is_better)


def month(date: datetime) -> datetime:
    return datetime(date.year, date.month, 1)


def next_month(date: datetime) -> datetime:
    return month(month(date) + timedelta(days=32))


def with_data(
    indicators: tuple[Indicator, ...], ppos_dex_data: list[PPoSDexData]
) -> tuple[Indicator, ...]:
    """The indicators with some data, leaving out metrics not published yet"""
    return tuple(i for i in indicators if has_data(ppos_dex_data, i.value))


def monthly_changes(
    ppos_dex_data: list[PPoSDexData], indicators: tuple[Indicator, ...] = HEATMAP
) -> tuple[list[datetime], list[list[float]]]:
    """Months, and the change of each heatmap row monthly average per month"""
    first, last = month(timestamp(ppos_dex_data[0])), timestamp(ppos_dex_data[-1])
    months = [first]
    while next_month(months[-1]) <= last:
        months.append(next_month(months[-1]))
    by_month: dict[datetime, list[PPoSDexData]] = {m: [] for m in months}
    for data in ppos_dex_data:
        by_month[month(timestamp(data))].append(data)

    rows = []
    for indicator in indicators:
        averages = []
        for m in months:
            values = [indicator.value(d) for d in by_month[m]]
            values = [v for v in values if not math.isnan(v)]
            averages.append(sum(values) / len(values) if values else math.nan)
        rows.append(
            [math.nan]
            + [
                change(old, new, indicator.higher_is_better) if old else math.nan
                for old, new in pairwise(averages)
            ]
        )
    return months, rows


def _colormap(colors: tuple[str, ...], name: str) -> LinearSegmentedColormap:
    return LinearSegmentedColormap.from_list(name, list(colors))


def _count_axis(axis: Axis) -> None:
    axis.set_major_locator(LogLocator(subs=(1, 2, 5)))
    axis.set_major_formatter(FuncFormatter(lambda v, _: count(v)))
    axis.set_minor_formatter(NullFormatter())


# Share of the online accounts the effective validators amount to
EVENNESS = (0.02, 0.05, 0.1, 0.2, 0.5, 1)


def weekly(
    ppos_dex_data: list[PPoSDexData], x: Value, y: Value
) -> tuple[list[datetime], list[float], list[float]]:
    """Weekly medians of two values, broken where data is missing

    Medians drop the one-day dips of the online accounts.
    """
    weeks: dict[tuple[int, int], list[PPoSDexData]] = {}
    for data in ppos_dex_data:
        week = timestamp(data).isocalendar()
        weeks.setdefault((week.year, week.week), []).append(data)
    dates: list[datetime] = []
    xs: list[float] = []
    ys: list[float] = []
    for week_data in weeks.values():
        # The latest point is labelled with the latest data date
        date = timestamp(week_data[-1])
        if dates and date - dates[-1] > NO_DATA:
            dates.append(dates[-1] + (date - dates[-1]) / 2)
            xs.append(math.nan)
            ys.append(math.nan)
        dates.append(date)
        xs.append(statistics.median(x(d) for d in week_data))
        ys.append(statistics.median(y(d) for d in week_data))
    return dates, xs, ys


def trajectory_figure(ppos_dex_data: list[PPoSDexData], theme: Theme) -> Figure:
    fig, ax = plt.subplots(figsize=(9, 6), layout="constrained")
    title(fig, "Decentralization Trajectory", theme)
    ax.set_title(
        "Weekly medians: more validators to the right, more evenly staked "
        "upwards (log scales)"
    )
    dates, x, y = weekly(ppos_dex_data, online_accounts, effective_validators)
    times = [float(t) for t in mdates.date2num(dates)]
    points = list(zip(x, y, strict=True))
    cmap = _colormap(theme.sequential, "time")
    path = LineCollection(
        [[a, b] for a, b in pairwise(points)],
        cmap=cmap,
        linewidths=1.6,
        capstyle="round",
    )
    path.set_array(times[:-1])
    ax.add_collection(path)
    ax.set_xscale("log")
    ax.set_yscale("log")
    finite = [(a, b) for a, b in points if not (math.isnan(a) or math.isnan(b))]
    x_min, x_max = min(a for a, _ in finite) / 1.4, max(a for a, _ in finite) * 1.4
    y_min, y_max = min(b for _, b in finite) / 1.4, max(b for _, b in finite) * 1.4
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.grid(True, axis="both", which="major")
    _count_axis(ax.xaxis)
    _count_axis(ax.yaxis)
    ax.set_xlabel("Online accounts")
    ax.set_ylabel("Effective validators, entropy equivalent")
    ax.text(
        1,
        -0.1,
        "Dashed: effective validators as a share of the online accounts",
        transform=ax.transAxes,
        ha="right",
        color=theme.muted,
        fontsize=8,
    )

    # Guides where the effective validators are a share of the online accounts
    for share in EVENNESS:
        if share * x_max < y_min or share * x_min > y_max:
            continue
        ax.plot(
            [x_min, x_max],
            [share * x_min, share * x_max],
            color=theme.grid,
            linewidth=1,
            linestyle=(0, (4, 3)),
            zorder=0,
        )
        # Labelled where the guide leaves the plot, on the right or at the top
        x_label = min(x_max, y_max / share)
        ax.annotate(
            f"{share:.0%}",
            (x_label, share * x_label),
            xytext=(-4, -4),
            textcoords="offset points",
            ha="right",
            va="top",
            color=theme.muted,
            fontsize=8,
        )

    # The first day of every year with data, and the latest one
    years: dict[int, int] = {}
    for i, date in enumerate(dates):
        if not math.isnan(y[i]):
            years.setdefault(date.year, i)
    marks = [*years.values(), len(dates) - 1]
    for n, i in enumerate(marks):
        latest = n == len(marks) - 1
        ax.plot(
            [x[i]],
            [y[i]],
            "o",
            markersize=8 if latest else 6,
            color=cmap((times[i] - times[0]) / (times[-1] - times[0])),
            markeredgecolor=theme.ink if latest else "none",
            zorder=3,
        )
        ax.annotate(
            f"{dates[i]:%-d %b %Y}" if latest else str(dates[i].year),
            (x[i], y[i]),
            xytext=(8, 6),
            textcoords="offset points",
            fontweight="bold" if latest else "normal",
            color=theme.ink if latest else theme.ink_secondary,
            fontsize=9,
        )
    return fig


def heatmap_figure(ppos_dex_data: list[PPoSDexData], theme: Theme) -> Figure:
    absolute = with_data(ABSOLUTE, ppos_dex_data)
    context = with_data(CONTEXT, ppos_dex_data)
    indicators = (*absolute, *context, *with_data(INDICATORS, ppos_dex_data))
    months, rows = monthly_changes(ppos_dex_data, indicators)
    fig, ax = plt.subplots(
        figsize=(9, 1.8 + 0.34 * len(indicators)), layout="constrained"
    )
    title(fig, "Monthly Change", theme)
    ax.set_title(
        "Change of each monthly average, towards more (blue) or less (red) "
        "decentralization"
    )
    # Months without a change stay empty
    mesh = ax.pcolormesh(
        mdates.date2num([*months, next_month(months[-1])]),
        range(len(indicators) + 1),
        rows,
        cmap=_colormap(theme.diverging, "change"),
        norm=TwoSlopeNorm(0, -MAX_CHANGE, MAX_CHANGE),
        edgecolors="none",
    )
    for start, end in no_data_periods([timestamp(d) for d in ppos_dex_data]):
        ax.axvspan(
            mdates.date2num(start),
            mdates.date2num(end),
            color=theme.track,
            linewidth=0,
            zorder=0,
        )
    # Separate the absolute numbers from the ratios and indexes
    for row in (len(absolute), len(absolute) + len(context)):
        ax.axhline(row, color=theme.baseline, linewidth=0.8)
    ax.set_yticks(
        [row + 0.5 for row in range(len(indicators))],
        [i.label for i in indicators],
        fontsize=9,
    )
    ax.invert_yaxis()
    ax.grid(False)
    ax.tick_params(axis="y", length=0)
    date_axis(ax)
    bar = fig.colorbar(
        mesh, ax=ax, orientation="horizontal", shrink=0.5, aspect=40, pad=0.02
    )
    bar.outline.set_visible(False)
    bar.ax.xaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    bar.ax.tick_params(length=0, labelsize=8)
    bar.set_label(
        f"Less decentralized  ←   change, ±{MAX_CHANGE:.0%} or more   →  "
        "More decentralized",
        fontsize=8,
        color=theme.muted,
    )
    return fig


def _tile(
    ax: Axes, ppos_dex_data: list[PPoSDexData], indicator: Indicator, theme: Theme
) -> None:
    dates, values = series(ppos_dex_data, Line(indicator.key, ""))
    ax.plot(mdates.date2num(dates), values, color=theme.series[0], linewidth=1.2)
    ax.set_title(indicator.label, fontsize=9, pad=22)
    if not indicator.higher_is_better:
        ax.invert_yaxis()
    ax.tick_params(axis="y", labelsize=7)
    if indicator.fmt is percent:
        ax.yaxis.set_major_formatter(PercentFormatter(1))
    elif indicator.fmt is not decimal:
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: indicator.fmt(v)))
    ax.locator_params(axis="y", nbins=3)
    value = indicator.value(ppos_dex_data[-1])
    ax.annotate(
        "—" if math.isnan(value) else indicator.fmt(value),
        (0, 1),
        xycoords="axes fraction",
        xytext=(0, 4),
        textcoords="offset points",
        fontsize=13,
        fontweight="bold",
        color=theme.ink,
    )
    delta = year_change(ppos_dex_data, indicator.value, indicator.higher_is_better)
    if delta is None:
        text, color = "no data a year ago", theme.muted
    elif abs(delta) < NO_CHANGE:
        text, color = "● no change", theme.muted
    else:
        arrow = "▲" if delta >= 0 else "▼"
        better = "more" if delta >= 0 else "less"
        text = f"{arrow} {percent(abs(delta))} {better} decentralized"
        color = theme.good if delta >= 0 else theme.bad
    ax.annotate(
        text,
        (1, 1),
        xycoords="axes fraction",
        xytext=(0, 4),
        textcoords="offset points",
        ha="right",
        fontsize=8,
        color=color,
    )
    date_axis(ax)
    ax.tick_params(axis="x", labelsize=7)


def glance_figure(ppos_dex_data: list[PPoSDexData], theme: Theme) -> Figure:
    # The absolute numbers on a row of their own, the indicators in two columns
    absolute = with_data(ABSOLUTE, ppos_dex_data)
    indicators = with_data(INDICATORS, ppos_dex_data)
    rows = 1 + math.ceil(len(indicators) / 2)
    fig = plt.figure(figsize=(9, 1.2 + 1.9 * rows), layout="constrained")
    grid = fig.add_gridspec(rows, 6)
    title(fig, "At a Glance", theme)
    fig.text(
        0.01,
        1 - 0.55 / fig.get_figheight(),
        f"Latest data {timestamp(ppos_dex_data[-1]):%-d %b %Y}, and change in one "
        "year. Inverted axes for inequality: up always means more decentralized",
        color=theme.ink_secondary,
        fontsize=9,
    )
    top = 1 - 0.75 / fig.get_figheight()
    fig.get_layout_engine().set(rect=(0, 0, 1, top))  # type: ignore[union-attr,call-arg]
    cells = [grid[0, 2 * i : 2 * i + 2] for i in range(len(absolute))] + [
        grid[1 + i // 2, 3 * (i % 2) : 3 * (i % 2) + 3] for i in range(len(indicators))
    ]
    first: Axes | None = None
    for cell, indicator in zip(cells, (*absolute, *indicators), strict=True):
        ax = fig.add_subplot(cell, sharex=first)
        first = first or ax
        _tile(ax, ppos_dex_data, indicator, theme)
    return fig


type Figures = Callable[[list[PPoSDexData], Theme], Figure]

FIGURES: tuple[tuple[str, Figures], ...] = (
    ("trajectory", trajectory_figure),
    ("monthly_change", heatmap_figure),
    ("at_a_glance", glance_figure),
)


def render(ppos_dex_data: list[PPoSDexData], save: bool = False) -> None:
    # Published data comes newest first, plot it in chronological order
    chronological = ppos_dex_data[::-1]
    for chart in TIMESERIES:
        plot_timeseries(chart, chronological, save, INSIGHTS_DIR)
    for name, figure in FIGURES:
        output(partial(figure, chronological), INSIGHTS_DIR / name, save)


def main() -> None:  # pragma: no cover
    ppos_dex_data = pposdex.get_ppos_dex_data(
        indexer_client=networks.get_indexer_client(networks.MAINNET),
        publisher_address=cli.DEFAULT_PUBLISHER,
        start_block=cli.DEFAULT_START_BLOCK,
        end_block=None,
        algo_threshold=cli.DEFAULT_ALGO_THRESHOLD,
    )
    render(ppos_dex_data, save=True)


if __name__ == "__main__":
    main()
