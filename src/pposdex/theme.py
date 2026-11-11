"""
PPoS Dex chart themes: every chart is drawn in a light and a dark variant
"""

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# Colorblind-safe categorical slots, validated on the mdBook light and dark
# themes backgrounds: at most six series per chart
LIGHT_SERIES = ("#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300")
DARK_SERIES = ("#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#008300")

# Browsers render the system font. None is installed for matplotlib, which lays
# out the text with its own DejaVu Sans: the same on every machine
FONTS = ["system-ui", "-apple-system", "Segoe UI", "sans-serif"]


@dataclass(frozen=True)
class Theme:
    name: str
    # Appended to the file name of the chart variant
    suffix: str
    ink: str
    ink_secondary: str
    muted: str
    grid: str
    baseline: str
    # Empty bar tracks and periods without data
    track: str
    series: tuple[str, str, str, str, str, str]
    # Time progression, from the oldest to the newest data
    sequential: tuple[str, ...]
    # Less decentralized, no change, more decentralized
    diverging: tuple[str, str, str]
    good: str
    bad: str


LIGHT = Theme(
    name="light",
    suffix="",
    ink="#0b0b0b",
    ink_secondary="#52514e",
    muted="#76746f",
    grid="#e1e0d9",
    baseline="#c3c2b7",
    track="#f0efec",
    series=LIGHT_SERIES,
    sequential=("#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#104281", "#0d366b"),
    diverging=("#e34948", "#f0efec", "#2a78d6"),
    good="#006300",
    bad="#d03b3b",
)

DARK = Theme(
    name="dark",
    suffix=".dark",
    ink="#f0efec",
    ink_secondary="#c3c2b7",
    muted="#9d9b94",
    grid="#ffffff1c",
    baseline="#ffffff47",
    track="#ffffff12",
    series=DARK_SERIES,
    sequential=("#184f95", "#1c5cab", "#2a78d6", "#5598e7", "#86b6ef", "#cde2fb"),
    diverging=("#e66767", "#3a3d44", "#3987e5"),
    good="#0ca30c",
    bad="#e66767",
)

THEMES = (LIGHT, DARK)


def _rc(theme: Theme) -> dict[Any, Any]:
    return {
        "font.family": "sans-serif",
        "font.sans-serif": [*FONTS, *mpl.rcParams["font.sans-serif"]],
        "font.size": 11,
        # Text stays text in the SVG: crisp, selectable and in the page font
        "svg.fonttype": "none",
        "figure.facecolor": "none",
        "axes.facecolor": "none",
        "savefig.facecolor": "none",
        "savefig.transparent": True,
        "text.color": theme.ink,
        "axes.titlecolor": theme.ink_secondary,
        "axes.titlesize": 11,
        "axes.titlelocation": "left",
        "axes.titlepad": 10,
        "axes.labelcolor": theme.ink_secondary,
        "axes.edgecolor": theme.baseline,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.axisbelow": True,
        "axes.prop_cycle": f"cycler(color={list(theme.series)})",
        "grid.color": theme.grid,
        "grid.linewidth": 0.8,
        "xtick.color": theme.baseline,
        "xtick.labelcolor": theme.muted,
        "ytick.color": theme.baseline,
        "ytick.labelcolor": theme.muted,
        "ytick.left": False,
        "xtick.major.size": 4,
        "lines.linewidth": 1.6,
        "lines.solid_capstyle": "round",
        "legend.frameon": False,
    }


@contextmanager
def use(theme: Theme) -> Iterator[None]:
    with mpl.rc_context(_rc(theme)):
        yield


def title(fig: Figure, text: str, theme: Theme) -> None:
    fig.suptitle(
        text, x=0.01, ha="left", fontsize=14, fontweight="bold", color=theme.ink
    )


type Chart = Callable[[Theme], Figure]


def output(chart: Chart, path: Path, save: bool) -> None:
    """Save the chart in both themes as SVG, or show it in the light theme"""
    if not save:
        with use(LIGHT):
            fig = chart(LIGHT)
            plt.show()
            plt.close(fig)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    for theme in THEMES:
        with use(theme):
            fig = chart(theme)
            fig.savefig(path.with_name(f"{path.name}{theme.suffix}.svg"))
            plt.close(fig)
