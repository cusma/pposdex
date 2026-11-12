import math
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

# The overall and top evenness
EVENNESS = {
    "One at 80%": (0.18, 0.56),
    "Six at 15%": (0.55, 0.84),
    "20 equal": (1, 1),
    "One at 30%": (0.51, 0.29),
    "20 large, 80 small": (0.44, 0.71),
    "100 equal": (1, 1),
}


# The entropy and the Theil T index
ENTROPY = {
    "One at 80%": (1.03, 1.74),
    "Six at 15%": (2.17, 0.60),
    "20 equal": (3.00, 0),
    "One at 30%": (3.58, 0.68),
    "20 large, 80 small": (3.77, 0.83),
    "100 equal": (4.61, 0),
}


@pytest.mark.parametrize("example", examples.EXAMPLES, ids=lambda e: e.name)
def test_entropy_matches_the_docs(example: examples.Example) -> None:
    entropy, theil = ENTROPY[example.name]
    assert round(example.entropy, 2) == entropy
    assert round(example.theil_t, 2) == theil
    # Theil's T is the gap between the maximum entropy, ln N, and the entropy
    maximum = math.log(example.validators)
    assert example.entropy + example.theil_t == pytest.approx(maximum)


def test_arrangements_match_the_docs() -> None:
    assert [len(examples.arrangements(held)) for held in (4, 3, 2)] == [1, 4, 6]
    # Every arrangement shares out all the ALGO, once
    for a, b in examples.arrangements(2):
        assert sorted(a + b) == list(examples.ALGO)


def test_two_validators_entropy() -> None:
    assert examples.two_validators_entropy(0) == 0
    assert examples.two_validators_entropy(1) == 0
    assert examples.two_validators_entropy(0.5) == pytest.approx(math.log(2))
    assert examples.two_validators_entropy(0.8) == pytest.approx(
        examples.two_validators_entropy(0.2)
    )


@pytest.mark.parametrize("example", examples.EXAMPLES, ids=lambda e: e.name)
def test_evenness_matches_the_docs(example: examples.Example) -> None:
    entropy, hhi = example.entropy_equivalent, example.hhi_equivalent
    overall, top = EVENNESS[example.name]
    assert round(entropy / example.validators, 2) == overall
    assert round(hhi / entropy, 2) == top


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


# The Nodes Hardware Decentralization table of the docs
NODES_TABLE = {1_000: 0.01, 3_000: 0.09, 5_000: 0.22, 10_000: 0.63, 20_000: 0.98}


@pytest.mark.parametrize(("nodes", "expected"), NODES_TABLE.items())
def test_nodes_hardware_matches_the_docs(nodes: int, expected: float) -> None:
    assert round(examples.nodes_hardware(nodes), 2) == expected


def test_observed_nodes_match_the_docs() -> None:
    low, high = examples.OBSERVED_NODES
    first, last = examples.OBSERVED_YEARS
    assert round(examples.nodes_hardware(low), 2) == 0.01
    assert round(examples.nodes_hardware(high), 2) == 0.13
    # The range and its years, as the Nodes page quotes them
    nodes_page = (Path(__file__).parents[2] / "docs/project/nodes.md").read_text()
    text = f"from about {low:,} to {high:,} full-time nodes between {first} and"
    assert text in nodes_page
    assert f"{first}\u2013{last}" in nodes_page
