from pathlib import Path

import matplotlib.pyplot as plt
import pytest

from pposdex import examples

# The table of the docs: N, entropy and HHI equivalents, then the Nakamoto
# coefficients for the veto, liveness, Nakamoto and upgrade thresholds
TABLE = {
    "One at 80%": (16, 2.8, 1.6, (1, 1, 1, 7)),
    "Six at 15%": (16, 8.7, 7.4, (1, 2, 3, 7)),
    "20 equal": (20, 20, 20, (3, 5, 7, 19)),
    "One at 30%": (71, 36.0, 10.3, (1, 1, 5, 62)),
    "20 large, 80 small": (100, 43.5, 30.8, (3, 6, 9, 61)),
    "100 equal": (100, 100, 100, (11, 21, 34, 91)),
}


@pytest.mark.parametrize("example", examples.EXAMPLES, ids=lambda e: e.name)
def test_values_match_the_docs(example: examples.Example) -> None:
    validators, entropy, hhi, nakamoto = TABLE[example.name]
    assert sum(example.stakes) == 100
    assert example.validators == validators
    assert round(example.entropy_equivalent, 1) == entropy
    assert round(example.hhi_equivalent, 1) == hhi
    assert tuple(example.nakamoto(share) for _, share in examples.THRESHOLDS) == (
        nakamoto
    )


def test_render(images: Path) -> None:
    examples.render(save=True)
    names = [name for name, _ in examples.FIGURES]
    expected = sorted(f"{n}{s}.svg" for n in names for s in ("", ".dark"))
    assert sorted(p.name for p in (images / "examples").iterdir()) == expected
    assert not plt.get_fignums()


def test_show(images: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    shown: list[None] = []
    monkeypatch.setattr(plt, "show", lambda: shown.append(None))
    examples.render()
    assert len(shown) == len(examples.FIGURES)
    assert not images.exists()
