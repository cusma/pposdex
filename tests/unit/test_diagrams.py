import math
from pathlib import Path

import matplotlib.pyplot as plt
import pytest

from pposdex import diagrams

NODES = diagrams.ALGORAND_NODES


def _gap(point: str, a: str, b: str) -> float:
    """Distance between a node's border and the link from a to b"""
    (px, py, kind), (ax, ay, _), (bx, by, _) = NODES[point], NODES[a], NODES[b]
    dx, dy = bx - ax, by - ay
    t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - ax - t * dx, py - ay - t * dy) - diagrams.radius(kind)


def test_links_never_pass_over_a_node() -> None:
    for a, b, _ in diagrams.ALGORAND_LINKS:
        for point in NODES:
            if point not in (a, b):
                assert _gap(point, a, b) > 0, (point, a, b)


def test_non_relay_nodes_have_up_to_4_links_per_network() -> None:
    for name, (_, _, kind) in NODES.items():
        if kind != "node":
            continue
        for p2p in (False, True):
            links = [
                link
                for link in diagrams.ALGORAND_LINKS
                if name in link[:2] and link[2] == p2p
            ]
            assert len(links) <= 4


def test_render(images: Path) -> None:
    diagrams.render(save=True)
    names = [name for name, _ in diagrams.DIAGRAMS]
    expected = sorted(f"{n}{s}.svg" for n in names for s in ("", ".dark"))
    assert sorted(p.name for p in (images / "diagrams").iterdir()) == expected
    assert not plt.get_fignums()


def test_show(images: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    shown: list[None] = []
    monkeypatch.setattr(plt, "show", lambda: shown.append(None))
    diagrams.render()
    assert len(shown) == len(diagrams.DIAGRAMS)
    assert not images.exists()
