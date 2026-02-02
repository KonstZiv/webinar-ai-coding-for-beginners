"""Particle dataclass and physics helpers for cascade animation."""

import random
from dataclasses import dataclass


@dataclass
class Particle:
    """A single character particle in the cascade animation.

    Attributes:
        char: The character to display.
        x: Horizontal position (column).
        y: Vertical position (row), float for smooth animation.
        velocity: Falling speed (rows per frame).
        style: Rich style string (e.g., "bold red").
        frozen: If True, particle doesn't fall.
        spin: Spin direction (-1 for left, +1 for right).
    """

    char: str
    x: int
    y: float
    velocity: float
    style: str | None
    frozen: bool
    spin: int  # -1 = left, +1 = right

    @classmethod
    def create(
        cls,
        char: str,
        x: int,
        y: int,
        style: str | None = None,
        frozen: bool = False,
    ) -> Particle:
        """Create a particle with random velocity and spin.

        Args:
            char: The character to display.
            x: Horizontal position (column).
            y: Vertical position (row).
            style: Rich style string.
            frozen: If True, particle doesn't fall.

        Returns:
            A new Particle instance.
        """
        velocity = 0.0 if frozen else random.uniform(0.08, 0.4)
        spin = 0 if frozen else random.choice([-1, 1])
        return cls(
            char=char,
            x=x,
            y=float(y),
            velocity=velocity,
            style=style,
            frozen=frozen,
            spin=spin,
        )


# Cell dimensions from renderer
CELL_WIDTH = 17
CELL_HEIGHT = 7
ROW_LABEL_WIDTH = 3


def cell_to_screen_bounds(cell_index: int) -> tuple[int, int, int, int]:
    """Convert cell index (0-8) to screen bounds.

    Args:
        cell_index: Cell index from 0 to 8.

    Returns:
        Tuple of (x1, y1, x2, y2) screen coordinates.
    """
    row = cell_index // 3
    col = cell_index % 3

    # X position: row_label + border + col * (cell_width + separator)
    x1 = ROW_LABEL_WIDTH + 1 + col * (CELL_WIDTH + 1)
    x2 = x1 + CELL_WIDTH

    # Y position: header + top_border + row * (cell_height + separator)
    y1 = 2 + row * (CELL_HEIGHT + 1)
    y2 = y1 + CELL_HEIGHT

    return x1, y1, x2, y2


def is_in_frozen_area(x: int, y: int, frozen_cells: set[int]) -> bool:
    """Check if screen coordinate is inside a frozen cell.

    Args:
        x: Screen column.
        y: Screen row.
        frozen_cells: Set of frozen cell indices.

    Returns:
        True if coordinate is inside a frozen cell.
    """
    for cell_index in frozen_cells:
        x1, y1, x2, y2 = cell_to_screen_bounds(cell_index)
        if x1 <= x < x2 and y1 <= y < y2:
            return True
    return False
