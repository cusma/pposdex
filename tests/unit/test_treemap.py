import pytest

from pposdex import treemap
from pposdex.examples import EXAMPLES, Example


class TestSquarify:
    @pytest.mark.parametrize("example", EXAMPLES, ids=lambda e: e.name)
    def test_areas_are_proportional(self, example: Example) -> None:
        stakes = [float(stake) for stake in example.stakes]
        boxes = treemap.squarify(stakes, (0, 0, 2, 1))
        areas = [width * height for _, _, width, height in boxes]
        assert areas == pytest.approx([2 * stake / 100 for stake in stakes])

    def test_boxes_fill_the_box(self) -> None:
        boxes = treemap.squarify([1.0] * 4, (0, 0, 1, 1))
        assert sorted((round(x, 9), round(y, 9)) for x, y, _, _ in boxes) == [
            (0, 0),
            (0, 0.5),
            (0.5, 0),
            (0.5, 0.5),
        ]
