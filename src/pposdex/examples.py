"""
PPoS Dex examples: the stake distributions of the docs, as figures

Run `python -m pposdex.examples` to save them in `./docs/images/examples`.
"""

import math
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from itertools import accumulate, combinations
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.patches import Circle, FancyBboxPatch, Patch
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
    def entropy(self) -> float:
        """Shannon entropy of the stake shares, in nats"""
        total = sum(self.stakes)
        return -sum(s / total * math.log(s / total) for s in self.stakes)

    @property
    def entropy_equivalent(self) -> float:
        return math.exp(self.entropy)

    @property
    def theil_t(self) -> float:
        """The gap between the maximum entropy, ln N, and the entropy"""
        return idx.theil_t(list(self.stakes))

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


# The ALGO shared between two validators, to count the arrangements
ALGO = (1, 2, 3, 4)
# Radius of an ALGO coin, and the slots of the two validators, in coin widths
COIN = 0.36
SLOTS_A, SLOTS_B = 0.0, 4.6
# Width of a case, its two validators side by side, and the gap to the next
CASE = SLOTS_B + 4 + 1.6


def arrangements(held: int) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    """Every way validator A holds `held` of the ALGO, B the rest"""
    return [(a, tuple(c for c in ALGO if c not in a)) for a in combinations(ALGO, held)]


def arrangements_figure(theme: Theme) -> Figure:
    fig, ax = plt.subplots(figsize=(9, 3.4), layout="constrained")
    title(fig, "Counting Arrangements", theme)
    ax.set_title(
        "Four ALGO, each with its own number and color, shared between "
        "validators A and B: each row is one way"
    )
    rows = max(len(arrangements(held)) for held in (2, 3, 4))
    # The three cases side by side, on the same scale
    for case, held in enumerate((4, 3, 2)):
        left = case * CASE
        ways = arrangements(held)
        plural = "s" if len(ways) > 1 else ""
        ax.text(
            left + (SLOTS_B + 4) / 2,
            -2.0,
            f"A holds {held}, B holds {len(ALGO) - held}",
            ha="center",
            va="bottom",
            fontweight="bold",
        )
        ax.text(
            left + (SLOTS_B + 4) / 2,
            -1.95,
            f"{len(ways)} arrangement{plural}",
            ha="center",
            va="top",
            color=theme.ink_secondary,
            fontsize=10,
        )
        for x, name in ((SLOTS_A, "A"), (SLOTS_B, "B")):
            ax.text(
                left + x + 2,
                -0.75,
                name,
                ha="center",
                color=theme.muted,
                fontsize=9,
            )
        for row, (a, b) in enumerate(ways):
            for x, coins in ((left + SLOTS_A, a), (left + SLOTS_B, b)):
                ax.add_patch(
                    FancyBboxPatch(
                        (x + 0.08, row - 0.45),
                        3.84,
                        0.9,
                        boxstyle="round,pad=0,rounding_size=0.2",
                        color=theme.track,
                        linewidth=0,
                    )
                )
                for slot, coin in enumerate(coins):
                    center = (x + 0.5 + slot, row)
                    # Each ALGO keeps its color and number in every arrangement
                    ax.add_patch(
                        Circle(
                            center,
                            COIN,
                            facecolor="none",
                            edgecolor=theme.series[coin - 1],
                            linewidth=2.4,
                        )
                    )
                    ax.text(
                        *center,
                        str(coin),
                        ha="center",
                        va="center",
                        fontsize=9,
                        fontweight="bold",
                    )
    ax.set_xlim(-0.1, 2 * CASE + SLOTS_B + 4.1)
    ax.set_ylim(rows - 0.4, -2.9)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


def two_validators_entropy(share: float) -> float:
    """Entropy of the stake of two validators, the first holding `share` of it"""
    return -sum(s * math.log(s) for s in (share, 1 - share) if s > 0)


def two_validators_figure(theme: Theme) -> Figure:
    fig, ax = plt.subplots(figsize=(9, 4.2), layout="constrained")
    title(fig, "The Entropy of Two Validators", theme)
    ax.set_title(
        "By the share of the stake A holds, B holding the rest: "
        "0 when one holds it all, the maximum when equal"
    )
    shares = [i / 400 for i in range(401)]
    ax.plot(
        shares,
        [two_validators_entropy(s) for s in shares],
        color=theme.series[0],
        linewidth=2.2,
        zorder=2,
    )
    maximum = math.log(2)
    ax.axhline(maximum, color=theme.baseline, linewidth=1, linestyle=(0, (4, 3)))
    ax.annotate(
        "ln 2 ≈ 0.69",
        (1, maximum),
        xycoords=("axes fraction", "data"),
        xytext=(6, 0),
        textcoords="offset points",
        va="center",
        color=theme.ink_secondary,
        fontsize=9,
    )
    # Labels clear of the curve: under it at the ends, above it at the top
    for share, label, offset, align in (
        (0, "B holds it all: 0", (8, 4), "left"),
        (0.5, "Equal stakes: the maximum", (0, 9), "center"),
        (1, "A holds it all: 0", (-8, 4), "right"),
    ):
        y = two_validators_entropy(share)
        ax.plot(
            [share],
            [y],
            "o",
            color=theme.series[0],
            markersize=6,
            zorder=3,
            clip_on=False,
        )
        ax.annotate(
            label,
            (share, y),
            xytext=offset,
            textcoords="offset points",
            ha=align,
            va="bottom",
            color=theme.ink_secondary,
            fontsize=9,
        )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.8)
    ax.xaxis.set_major_formatter(PercentFormatter(1))
    ax.set_xlabel("Share of the stake held by A")
    ax.set_ylabel("Entropy, in nats")
    return fig


# Gap between the entropy and Theil's T segments of a bar, in nats
SEGMENT_GAP = 0.02


def entropy_figure(theme: Theme) -> Figure:
    fig, ax = plt.subplots(figsize=(9, 4.8), layout="constrained")
    title(fig, "Entropy and Its Maximum", theme)
    ax.set_title(
        "Each bar is the maximum, ln N: the entropy of the stake, then Theil's T, "
        "lost to concentration"
    )
    rows = range(len(EXAMPLES))
    for row, example in zip(rows, EXAMPLES, strict=True):
        entropy, theil = example.entropy, example.theil_t
        ax.barh(row, entropy, height=0.4, color=theme.series[0])
        if theil > SEGMENT_GAP:
            ax.barh(
                row,
                theil - SEGMENT_GAP,
                left=entropy + SEGMENT_GAP,
                height=0.4,
                color=theme.series[1],
            )
        ax.annotate(
            f"T = {theil:.2f}" if round(theil, 2) else "T = 0",
            (entropy + theil, row),
            xytext=(6, 0),
            textcoords="offset points",
            va="center",
            color=theme.ink_secondary,
            fontsize=9,
        )
    ax.set_yticks(
        list(rows), [f"{e.name}\n{e.validators} validators" for e in EXAMPLES]
    )
    ax.invert_yaxis()
    ax.set_xlim(0, 5.4)
    ax.grid(True, axis="x")
    ax.grid(False, axis="y")
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("Entropy, in nats")
    ax.legend(
        handles=[
            Patch(color=theme.series[0], label="Entropy H"),
            Patch(color=theme.series[1], label="Theil's T, lost to concentration"),
        ],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.16),
        ncols=2,
        frameon=False,
    )
    return fig


# Nodes Hardware Decentralization: speed of growth and inflection point
NODES_K = 2
NODES_LAMBDA = 10_000
# Full-time node equivalents estimated by Nodely, over the years observed
OBSERVED_NODES = (1_200, 3_700)
OBSERVED_YEARS = (2024, 2026)


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
    first, last = OBSERVED_YEARS
    ax.axvspan(low, high, color=theme.track, zorder=0)
    ax.annotate(
        f"Algorand, {first}\u2013{last}\n{count(low)} to {count(high)} nodes",
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
    ("arrangements", arrangements_figure),
    ("two_validators", two_validators_figure),
    ("entropy", entropy_figure),
    ("nodes_hardware", nodes_figure),
)


def render(save: bool = False) -> None:
    for name, figure in FIGURES:
        output(partial(figure), EXAMPLES_DIR / name, save)


def main() -> None:  # pragma: no cover
    render(save=True)


if __name__ == "__main__":
    main()
