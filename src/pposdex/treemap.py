"""
Treemaps of stake distributions: each validator a rectangle, its area its stake
"""

from collections.abc import Sequence

from matplotlib.axes import Axes
from matplotlib.patches import Rectangle

type Box = tuple[float, float, float, float]


def _worst(row: list[float], side: float) -> float:
    """The worst aspect ratio of a row of areas laid along a side"""
    total = sum(row)
    return max(max(side**2 * a / total**2, total**2 / (side**2 * a)) for a in row)


def squarify(areas: Sequence[float], box: Box) -> list[Box]:
    """Treemap of the areas, largest first, as squarish boxes filling the box"""
    x, y, width, height = box
    scale = width * height / sum(areas)
    left = [a * scale for a in areas]
    boxes: list[Box] = []
    while left:
        side = min(width, height)
        row = [left.pop(0)]
        while left and _worst([*row, left[0]], side) <= _worst(row, side):
            row.append(left.pop(0))
        thickness = sum(row) / side
        offset = 0.0
        for area in row:
            length = area / thickness
            if width >= height:
                boxes.append((x, y + offset, thickness, length))
            else:
                boxes.append((x + offset, y, length, thickness))
            offset += length
        if width >= height:
            x, width = x + thickness, width - thickness
        else:
            y, height = y + thickness, height - thickness
    return boxes


def draw(ax: Axes, areas: Sequence[float], colors: Sequence[str], gap: float) -> None:
    """Draw the treemap of the areas in a unit square, each box in its color

    The gap between the boxes is a fraction of the square side
    """
    ax.set_xlim(0, 1)
    ax.set_ylim(1, 0)
    ax.set_aspect("equal")
    ax.axis("off")
    for (x, y, width, height), color in zip(
        squarify(areas, (0, 0, 1, 1)), colors, strict=True
    ):
        ax.add_patch(
            Rectangle(
                (x + gap / 2, y + gap / 2),
                max(width - gap, 0),
                max(height - gap, 0),
                color=color,
                linewidth=0,
            )
        )
