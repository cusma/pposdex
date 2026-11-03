import copy
from collections.abc import Callable
from pathlib import Path

import matplotlib.pyplot as plt
import pytest

from pposdex import plots
from pposdex.ppos_dex_data import PPoSDexData

TIMESERIES = [
    "accounts_prt.png",
    "algo_dynamics.png",
    "algo_inequality.png",
    "ppos_dex.png",
    "ppos_inequality_b.png",
    "ppos_inequality_unb.png",
]
SNAPSHOT = [
    "accounts_prt.png",
    "algo_dynamics.png",
    "ppos_dex.png",
    "ppos_inequality.png",
]


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
    assert sorted(p.name for p in (images / kind).iterdir()) == expected
    assert data == original
    assert not plt.get_fignums()


def test_snapshot_without_optional_metrics(
    data: list[PPoSDexData], images: Path
) -> None:
    plots.snapshot(data[-1:], True)
    assert sorted(p.name for p in (images / "snapshot").iterdir()) == SNAPSHOT


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
    assert not list(images.rglob("*.png"))
