"""
PPoS Dex diagrams: the network topologies of the docs, as figures

Run `python -m pposdex.diagrams` to save them in `./docs/images/diagrams`.

The diagrams are drawn in a space of 1,000 units wide, y pointing down.
"""

import math
from collections.abc import Callable
from functools import partial
from pathlib import Path
from typing import Literal

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Circle

from pposdex.theme import Theme, output

DIAGRAMS_DIR = Path("./docs/images/diagrams")

WIDTH = 1000
# Figure width in inches, as the charts: one unit is 0.648 points
FIG_WIDTH = 9
PT = FIG_WIDTH * 72 / WIDTH

type Kind = Literal["relay", "outside", "hybrid", "p2p", "node", "plain"]

RELAY_R, NODE_R = 30, 18
THICK, THIN = 3.2, 1.3
DASH = (8, 5)


def canvas(theme: Theme, height: float) -> tuple[Figure, Axes]:
    fig = plt.figure(figsize=(FIG_WIDTH, FIG_WIDTH * height / WIDTH))
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(height, 0)
    ax.set_aspect("equal")
    ax.set_axis_off()
    return fig, ax


def dashes(
    width: float, pattern: tuple[float, float] = DASH
) -> tuple[int, tuple[float, ...]]:
    # matplotlib scales the dashes by the line width: undo it
    return 0, tuple(p * PT / width for p in pattern)


def link(
    ax: Axes,
    a: tuple[float, float, float],
    b: tuple[float, float, float],
    theme: Theme,
    width: float,
    p2p: bool = False,
) -> None:
    """A straight link between the borders of two circles (x, y, radius)"""
    (x1, y1, r1), (x2, y2, r2) = a, b
    d = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    ax.plot(
        [x1 + ux * r1, x2 - ux * r2],
        [y1 + uy * r1, y2 - uy * r2],
        color=theme.ink_secondary,
        linewidth=width * PT,
        linestyle=dashes(width * PT) if p2p else "-",
        solid_capstyle="butt",
        dash_capstyle="butt",
    )


def node(
    ax: Axes, x: float, y: float, r: float, kind: Kind, label: str, theme: Theme
) -> None:
    width = (2 if kind != "node" else 1.5) * PT
    ax.add_patch(
        Circle(
            (x, y),
            r,
            facecolor=theme.baseline if kind == "outside" else "none",
            edgecolor=theme.ink_secondary,
            linewidth=width,
            linestyle=dashes(width, (6, 4)) if kind == "p2p" else "-",
            zorder=3,
        )
    )
    if kind == "hybrid":
        inner = 1.3 * PT
        ax.add_patch(
            Circle(
                (x, y),
                r - 5,
                facecolor="none",
                edgecolor=theme.ink_secondary,
                linewidth=inner,
                linestyle=dashes(inner, (4, 3)),
                zorder=3,
            )
        )
    ax.text(
        x,
        y,
        label,
        ha="center",
        va="center",
        fontsize=(max(r * 0.62, 13) if kind != "plain" else 18) * PT,
        fontstyle="italic",
        color=theme.ink,
        zorder=4,
    )


# The Algorand topology: relays (R), hybrid relays (H), a relay outside the DNS
# list (X), a P2P-only relay (L), WebSocket-only nodes (W) and hybrid nodes (Y).
# The layout comes from a search for straight links that never pass over a node
# they do not connect: keep that rule when moving anything.
ALGORAND_NODES: dict[str, tuple[float, float, Kind]] = {
    "R0": (653, 261, "relay"),
    "R1": (559, 390, "hybrid"),
    "R2": (364, 325, "relay"),
    "R3": (346, 168, "outside"),
    "R4": (531, 102, "hybrid"),
    "R5": (495, 256, "relay"),
    "W0": (184, 156, "node"),
    "W1": (415, 50, "node"),
    "W2": (305, 481, "node"),
    "W3": (139, 334, "node"),
    "Y0": (585, 510, "node"),
    "Y1": (695, 79, "node"),
    "Y2": (816, 404, "node"),
    "L": (861, 226, "p2p"),
}

# (from, to, over P2P)
ALGORAND_LINKS: tuple[tuple[str, str, bool], ...] = (
    # The relay mesh
    ("R3", "R4", False),
    ("R2", "R3", False),
    ("R4", "R5", False),
    ("R0", "R5", False),
    ("R1", "R5", False),
    ("R3", "R5", False),
    ("R0", "R4", False),
    ("R2", "R5", False),
    ("R1", "R2", False),
    ("R0", "R1", False),
    ("R1", "R4", True),
    ("L", "R1", True),
    ("L", "R4", True),
    # WebSocket-only nodes: 4 relays each
    ("W0", "R3", False),
    ("W0", "R2", False),
    ("W0", "R5", False),
    ("W0", "R4", False),
    ("W1", "R4", False),
    ("W1", "R3", False),
    ("W1", "R5", False),
    ("W1", "R2", False),
    ("W2", "R2", False),
    ("W2", "R1", False),
    ("W2", "R5", False),
    ("W2", "R3", False),
    ("W3", "R2", False),
    ("W3", "R3", False),
    ("W3", "R5", False),
    ("W3", "R1", False),
    # Hybrid nodes: WebSocket and P2P
    ("Y0", "R0", False),
    ("Y0", "R2", False),
    ("Y0", "R1", True),
    ("Y0", "L", True),
    ("Y1", "R0", False),
    ("Y1", "R5", False),
    ("Y1", "R4", True),
    ("Y1", "L", True),
    ("Y2", "R0", False),
    ("Y2", "R5", False),
    ("Y2", "R1", True),
    ("Y2", "L", True),
)

LABELS: dict[Kind, str] = {
    "relay": "R",
    "outside": "R",
    "hybrid": "H",
    "p2p": "R",
    "node": "N",
    "plain": "",
}


def radius(kind: Kind) -> float:
    return NODE_R if kind == "node" else RELAY_R


def is_relay(name: str) -> bool:
    return ALGORAND_NODES[name][2] != "node"


def algorand_figure(theme: Theme) -> Figure:
    fig, ax = canvas(theme, 785)
    circles = {k: (x, y, radius(kind)) for k, (x, y, kind) in ALGORAND_NODES.items()}
    for a, b, p2p in ALGORAND_LINKS:
        thick = is_relay(a) and is_relay(b)
        link(ax, circles[a], circles[b], theme, THICK if thick else THIN, p2p)
    for x, y, kind in ALGORAND_NODES.values():
        node(ax, x, y, radius(kind), kind, LABELS[kind], theme)

    # Legend
    top = 565
    ax.plot([40, WIDTH - 40], [top, top], color=theme.baseline, linewidth=PT)

    def entry(x: float, y: float, text: str) -> None:
        ax.text(x, y, text, va="center", fontsize=15 * PT, color=theme.ink)

    def sample(x: float, y: float, width: float, p2p: bool) -> None:
        ax.plot(
            [x, x + 44],
            [y, y],
            color=theme.ink_secondary,
            linewidth=width * PT,
            linestyle=dashes(width * PT) if p2p else "-",
        )

    rows = [top + 35, top + 82, top + 129, top + 176]
    kinds: tuple[tuple[Kind, str], ...] = (
        ("relay", "Relay in the DNS bootstrap list"),
        ("outside", "Relay outside the list (phonebook, DHT)"),
        ("hybrid", "Hybrid relay: WebSocket and P2P"),
        ("p2p", "P2P relay: P2P only"),
    )
    for y, (kind, text) in zip(rows, kinds, strict=True):
        node(ax, 62, y, 16, kind, LABELS[kind], theme)
        entry(92, y, text)
    node(ax, 482, rows[0], 12, "node", "N", theme)
    entry(512, rows[0], "Non-relay node: up to 4 outgoing links per network")
    for dy, width, text in (
        (-11, THICK, "Relay to relay"),
        (11, THIN, "Node to relay"),
    ):
        sample(460, rows[1] + dy, width, p2p=False)
        sample(560, rows[1] + dy, width, p2p=True)
        entry(615, rows[1] + dy, text)
    entry(460, rows[2], "Solid: WebSocket")
    entry(615, rows[2], "Dashed: P2P")
    return fig


def ring(
    cx: float, cy: float, r: float, n: int, start: float
) -> list[tuple[float, float]]:
    return [
        (
            cx + r * math.cos(math.radians(start + 360 * i / n)),
            cy + r * math.sin(math.radians(start + 360 * i / n)),
        )
        for i in range(n)
    ]


# Example networks: (name, nodes, links, index of N1, index of N2, title position)
type Network = tuple[
    str,
    list[tuple[float, float]],
    list[tuple[int, int]],
    int,
    int,
    tuple[float, float],
]

NETWORKS: tuple[Network, ...] = (
    # A: a chain, a single path from N1 to N2
    (
        "A",
        [(52 + 66 * i, 150) for i in range(7)],
        [(i, i + 1) for i in range(6)],
        0,
        6,
        (250, 290),
    ),
    # B: a ring, two paths
    (
        "B",
        ring(760, 150, 112, 7, -90),
        [(i, (i + 1) % 7) for i in range(7)],
        6,
        3,
        (760, 330),
    ),
    # C: a star, every path through the center
    (
        "C",
        [(250, 520), *ring(250, 520, 110, 6, 0)],
        [(0, i) for i in range(1, 7)],
        5,
        2,
        (250, 700),
    ),
    # D: a mesh, many paths
    (
        "D",
        [
            (760, 415),
            (680, 465),
            (845, 465),
            (650, 560),
            (870, 560),
            (700, 640),
            (820, 640),
        ],
        [
            (0, 1),
            (0, 2),
            (1, 2),
            (1, 5),
            (2, 3),
            (2, 4),
            (3, 4),
            (3, 6),
            (4, 5),
            (5, 6),
        ],
        1,
        6,
        (760, 715),
    ),
)
NETWORK_R = 24


def networks_figure(theme: Theme) -> Figure:
    fig, ax = canvas(theme, 740)
    for name, points, links, n1, n2, (tx, ty) in NETWORKS:
        for a, b in links:
            link(
                ax,
                (*points[a], NETWORK_R),
                (*points[b], NETWORK_R),
                theme,
                1.5,
            )
        for i, (x, y) in enumerate(points):
            label = {n1: "N₁", n2: "N₂"}.get(i, "")
            node(ax, x, y, NETWORK_R, "plain", label, theme)
        ax.text(
            tx,
            ty,
            f"Network {name}",
            ha="center",
            va="center",
            fontsize=24 * PT,
            fontweight="bold",
            color=theme.ink,
        )
    return fig


DIAGRAMS: tuple[tuple[str, Callable[[Theme], Figure]], ...] = (
    ("algorand_topology", algorand_figure),
    ("topologies", networks_figure),
)


def render(save: bool = False) -> None:
    for name, figure in DIAGRAMS:
        output(partial(figure), DIAGRAMS_DIR / name, save)


def main() -> None:  # pragma: no cover
    render(save=True)


if __name__ == "__main__":
    main()
