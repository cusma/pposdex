"""
PPoS Dex plots
"""

import math
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

N_XTICKS = 10
XTICKS_ROTATION = 45
TIMESERIES_DIR = Path("./docs/images/timeseries")
SNAPSHOT_DIR = Path("./docs/images/snapshot")
SNAPSHOT_STYLE = "fivethirtyeight"


@dataclass(frozen=True)
class Line:
    key: str
    label: str


@dataclass(frozen=True)
class TimeseriesPanel:
    subtitle: str
    lines: tuple[Line, ...]
    y_max: float | None = None
    # Only plot data points where this key is set
    only_with: str | None = None


@dataclass(frozen=True)
class TimeseriesChart:
    name: str
    title: str
    panels: tuple[TimeseriesPanel, ...]


@dataclass(frozen=True)
class Bar:
    label: str
    key: str
    x_max: Callable[[dict], float]
    color: str | None = None
    # Other keys the bar needs, it is not drawn if any of them is missing
    requires: tuple[str, ...] = ()


@dataclass(frozen=True)
class SnapshotChart:
    name: str
    title: str
    bars: tuple[Bar, ...]


def _x_max_unit(_: dict) -> float:
    return 1


def _x_max_zoom(key: str) -> Callable[[dict], float]:
    # Zoom on small values, up to the unit
    return lambda data: min([1, 10 * data[key]])


def _x_max_theil(data: dict) -> float:
    return round(max(data["ppos_theil_l"], data["ppos_theil_t"])) + 1


EQUALITY = "(0 = complete equality)"
DECENTRALIZATION = "(1 = perfect decentralization)"

TIMESERIES = (
    TimeseriesChart(
        name="algo_dynamics",
        title="ALGO Dynamics",
        panels=(
            TimeseriesPanel(
                subtitle="(1 = full circulation or complete participation)",
                lines=(
                    Line("algo_dynamics", "ALGO Supply"),
                    Line("ppos_online_stake", "ALGO Participation in PPoS"),
                ),
                y_max=1,
            ),
        ),
    ),
    TimeseriesChart(
        name="accounts_prt",
        title="Accounts Participation in PPoS",
        panels=(
            TimeseriesPanel(
                subtitle="(1 = complete participation)",
                lines=(Line("ppos_online_accounts", "Accounts Participation"),),
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
                EQUALITY, (Line("ppos_gini", "Gini Index"), Line("ppos_hhi", "HHI"))
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
            TimeseriesPanel(
                DECENTRALIZATION,
                (Line("ppos_dex_v2", "PPoS Dex V2"),),
                only_with="ppos_dex_v2",
            ),
        ),
    ),
)

SNAPSHOTS = (
    SnapshotChart(
        name="algo_dynamics",
        title="ALGO Dynamics\n(1 = full circulation or complete participation)",
        bars=(
            Bar("ALGO Supply", "algo_dynamics", _x_max_unit),
            Bar("ALGO Participation", "ppos_online_stake", _x_max_unit),
        ),
    ),
    SnapshotChart(
        name="accounts_prt",
        title="Accounts Participation\n(1 = complete participation)",
        bars=(
            Bar(
                "Accounts Participation",
                "ppos_online_accounts",
                _x_max_zoom("ppos_online_accounts"),
            ),
        ),
    ),
    SnapshotChart(
        name="ppos_inequality",
        title=f"Validators Stake Inequality\n{EQUALITY}",
        bars=(
            Bar("Gini Index", "ppos_gini", _x_max_unit, color="g"),
            Bar("HHI", "ppos_hhi", _x_max_unit, color="g"),
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
        title=f"PPoS Dex\n{DECENTRALIZATION}",
        bars=(
            Bar("PPoS Dex v1", "ppos_dex", _x_max_zoom("ppos_dex")),
            Bar("PPoS Dex v2", "ppos_dex_v2", _x_max_zoom("ppos_dex_v2")),
        ),
    ),
)


def _output(fig: Figure, path: Path, save: bool) -> None:
    fig.tight_layout()
    if save:
        fig.savefig(path)
    else:
        plt.show()
    plt.close(fig)


def _series(ppos_dex_data: list[dict], key: str) -> list[float]:
    # Missing data points are plotted as gaps
    return [d.get(key, math.nan) for d in ppos_dex_data]


def plot_timeseries(
    chart: TimeseriesChart, ppos_dex_data: list[dict], save: bool = False
) -> None:
    fig = plt.figure()
    fig.suptitle(chart.title)
    for row, panel in enumerate(chart.panels, start=1):
        data = ppos_dex_data
        if panel.only_with is not None:
            data = [d for d in data if d.get(panel.only_with)]
        x_axis = list(range(len(data)))
        x_ticks = [d["timestamp"][:10] for d in data]

        ax = fig.add_subplot(len(chart.panels), 1, row)
        ax.set_title(panel.subtitle, fontsize="medium")
        for line in panel.lines:
            ax.plot(x_axis, _series(data, line.key), label=line.label)
        ax.set_xticks(x_axis, x_ticks, rotation=XTICKS_ROTATION)
        ax.locator_params(nbins=N_XTICKS)
        ax.legend()
        ax.set_ylim(0, panel.y_max)
        ax.grid(True)
    _output(fig, TIMESERIES_DIR / f"{chart.name}.png", save)


def snap_suptitle(timestamp: str, algo_threshold: int, accounts: int) -> str:
    return f"{timestamp}\nThreshold: {algo_threshold} ALGO\nAccounts: {accounts}"


def plot_snapshot(chart: SnapshotChart, data: dict, save: bool = False) -> None:
    with plt.style.context(SNAPSHOT_STYLE):
        fig = plt.figure()
        fig.suptitle(
            f"{chart.title}\n"
            + snap_suptitle(
                data["timestamp"][:10], data["algo_threshold"], data["accounts"]
            ),
            fontsize="medium",
        )
        for row, bar in enumerate(chart.bars, start=1):
            if any(data.get(key) is None for key in (bar.key, *bar.requires)):
                continue
            ax = fig.add_subplot(len(chart.bars), 1, row)
            ax.barh(bar.label, data[bar.key], color=bar.color)
            ax.set_xlim(0, bar.x_max(data))
        _output(fig, SNAPSHOT_DIR / f"{chart.name}.png", save)


def timeseries(ppos_dex_data: list[dict], save: bool = False) -> None:
    # Published data comes newest first, plot it in chronological order
    chronological = ppos_dex_data[::-1]
    for chart in TIMESERIES:
        plot_timeseries(chart, chronological, save)


def snapshot(ppos_dex_data: list[dict], save: bool = False) -> None:
    latest = ppos_dex_data[0]
    for chart in SNAPSHOTS:
        plot_snapshot(chart, latest, save)
