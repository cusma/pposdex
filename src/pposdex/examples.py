"""
PPoS Dex examples: the stake distributions of the docs, as figures

Run `python -m pposdex.examples` to save them in `./docs/images/examples`.
"""

import math
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from itertools import accumulate
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter, NullFormatter, PercentFormatter

from pposdex import inequality_idx as idx
from pposdex import treemap
from pposdex.plots import count
from pposdex.ppos_dex_data import V3_SHARES
from pposdex.theme import Theme, output, title

EXAMPLES_DIR = Path("./docs/images/examples")


@dataclass(frozen=True)
class Example:
    name: str
    # Stake percent of each validator, the largest first
    stakes: tuple[float, ...]

    @property
    def validators(self) -> int:
        return len(self.stakes)

    @property
    def entropy_equivalent(self) -> float:
        total = sum(self.stakes)
        entropy = -sum(s / total * math.log(s / total) for s in self.stakes)
        return math.exp(entropy)

    @property
    def hhi_equivalent(self) -> float:
        return 1 / idx.herfindahl_hirschman(list(self.stakes))

    def nakamoto(self, share: float) -> int:
        return idx.nakamoto_coefficient(list(self.stakes), share)


EXAMPLES = (
    Example("One at 80%", (80, *[2] * 5, *[1] * 10)),
    Example("Six at 15%", (*[15] * 6, *[1] * 10)),
    Example("20 equal", (5,) * 20),
    Example("One at 30%", (30, *[1] * 70)),
    Example("20 large, 80 small", (*[4] * 20, *[0.25] * 80)),
    Example("100 equal", (1,) * 100),
)

THRESHOLDS = (
    ("Veto", V3_SHARES["veto"]),
    ("Liveness", V3_SHARES["liveness"]),
    ("Nakamoto", V3_SHARES["nakamoto"]),
    ("Upgrade", V3_SHARES["upgrade"]),
)


# Gap between the validators of a treemap, as a fraction of its side
GAP = 0.012


def treemap_figure(theme: Theme) -> Figure:
    fig, axes = plt.subplots(2, 3, figsize=(9, 6.9), layout="constrained")
    title(fig, "Who Holds the Stake", theme)
    fig.text(
        0.01,
        1 - 0.55 / fig.get_figheight(),
        "Each rectangle is a validator, its area its stake",
        color=theme.ink_secondary,
        fontsize=10,
    )
    fig.get_layout_engine().set(rect=(0, 0, 1, 1 - 0.75 / fig.get_figheight()))  # type: ignore[union-attr,call-arg]
    for ax, example in zip(axes.flat, EXAMPLES, strict=True):
        ax.set_title(f"{example.name}\n{example.validators} validators")
        treemap.draw(ax, example.stakes, [theme.series[0]] * example.validators, GAP)
    return fig


def coalition_figure(theme: Theme) -> Figure:
    fig, ax = plt.subplots(figsize=(9, 5.6), layout="constrained")
    title(fig, "How Many Validators Reach Each Threshold", theme)
    ax.set_title(
        "Stake of the largest validators: where a line crosses a threshold is its "
        "Nakamoto coefficient"
    )
    for example, color in zip(EXAMPLES, theme.series, strict=True):
        held = [0, *accumulate(example.stakes)]
        ax.plot(
            range(len(held)),
            [h / 100 for h in held],
            drawstyle="steps-post",
            color=color,
            label=example.name,
        )
        for _, share in THRESHOLDS:
            n = example.nakamoto(share)
            ax.plot([n], [held[n] / 100], "o", color=color, markersize=5, zorder=3)
    for name, share in THRESHOLDS:
        ax.axhline(share, color=theme.baseline, linewidth=1, linestyle=(0, (4, 3)))
        ax.annotate(
            f"{name} {share:.0%}",
            (1, share),
            xycoords=("axes fraction", "data"),
            xytext=(6, 0),
            textcoords="offset points",
            va="center",
            color=theme.ink_secondary,
            fontsize=9,
        )
    ax.set_xscale("log")
    ax.set_xlim(0.9, 110)
    ax.set_ylim(0, 1.02)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: count(v)))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(PercentFormatter(1))
    ax.set_xlabel("Largest validators (log scale)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncols=3, frameon=False)
    return fig


def effective_figure(theme: Theme) -> Figure:
    fig, ax = plt.subplots(figsize=(9, 4.4), layout="constrained")
    title(fig, "What the Inequality Indexes Miss", theme)
    ax.set_title("Validators, and the equal-stake validators they are worth")
    marks: tuple[tuple[str, Callable[[Example], float], str, str], ...] = (
        ("Validators", lambda e: e.validators, "o", theme.series[0]),
        ("Entropy equivalent", lambda e: e.entropy_equivalent, "D", theme.series[1]),
        ("HHI equivalent", lambda e: e.hhi_equivalent, "s", theme.series[2]),
    )
    rows = range(len(EXAMPLES))
    for row, example in zip(rows, EXAMPLES, strict=True):
        values = [value(example) for _, value, _, _ in marks]
        ax.plot(
            [min(values), max(values)],
            [row, row],
            color=theme.baseline,
            linewidth=2,
            zorder=1,
        )
    # Slightly apart, so the marks of equal values all show
    for (label, value, marker, color), dodge in zip(
        marks, (-0.16, 0, 0.16), strict=True
    ):
        ax.plot(
            [value(e) for e in EXAMPLES],
            [row + dodge for row in rows],
            marker,
            color=color,
            markersize=8,
            linestyle="none",
            label=label,
            zorder=2,
        )
    ax.set_yticks(list(rows), [e.name for e in EXAMPLES])
    ax.invert_yaxis()
    ax.set_xscale("log")
    ax.set_xlim(1, 150)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: count(v)))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.grid(True, axis="x")
    ax.grid(False, axis="y")
    ax.tick_params(axis="y", length=0)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncols=3, frameon=False)
    return fig


# Nodes Hardware Decentralization: speed of growth and inflection point
NODES_K = 2
NODES_LAMBDA = 10_000
# Full-time node equivalents estimated by Nodely since 2024
OBSERVED_NODES = (1_200, 3_700)


def nodes_hardware(
    nodes: float, lam: float = NODES_LAMBDA, k: float = NODES_K
) -> float:
    return 1 - math.exp(-((nodes / lam) ** k))


def nodes_figure(theme: Theme) -> Figure:
    fig, ax = plt.subplots(figsize=(9, 4.6), layout="constrained")
    title(fig, "Nodes Hardware Decentralization", theme)
    ax.set_title(
        f"By number of nodes, with k = {NODES_K}: "
        "the inflection point λ is a judgment call"
    )
    nodes = [10 ** (2 + i / 100) for i in range(351)]
    low, high = OBSERVED_NODES
    ax.axvspan(low, high, color=theme.track, zorder=0)
    ax.annotate(
        f"Algorand today\n{count(low)} to {count(high)} nodes",
        (math.sqrt(low * high), 0.5),
        ha="center",
        va="center",
        color=theme.ink_secondary,
        fontsize=9,
    )
    for lam, style, width, color in (
        (1_000, (0, (4, 3)), 1.2, theme.muted),
        (NODES_LAMBDA, "-", 2.2, theme.series[0]),
        (100_000, (0, (4, 3)), 1.2, theme.muted),
    ):
        ax.plot(
            nodes,
            [nodes_hardware(n, lam) for n in nodes],
            linestyle=style,
            linewidth=width,
            color=color,
            zorder=2,
        )
        y = nodes_hardware(lam, lam)
        ax.plot([lam], [y], "o", color=color, markersize=5, zorder=3)
        ax.annotate(
            f"λ = {count(lam)}",
            (lam, y),
            xytext=(8, -4),
            textcoords="offset points",
            ha="left",
            va="top",
            color=theme.ink if lam == NODES_LAMBDA else theme.muted,
            fontsize=9,
            fontweight="bold" if lam == NODES_LAMBDA else "normal",
        )
    ax.set_xscale("log")
    ax.set_xlim(nodes[0], nodes[-1])
    ax.set_ylim(0, 1.02)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: count(v)))
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xlabel("Nodes (log scale)")
    return fig


FIGURES: tuple[tuple[str, Callable[[Theme], Figure]], ...] = (
    ("stakes", treemap_figure),
    ("coalitions", coalition_figure),
    ("effective_numbers", effective_figure),
    ("nodes_hardware", nodes_figure),
)


def render(save: bool = False) -> None:
    for name, figure in FIGURES:
        output(partial(figure), EXAMPLES_DIR / name, save)


def main() -> None:  # pragma: no cover
    render(save=True)


if __name__ == "__main__":
    main()
