"""Rich-based player for Tic-Tac-Toe with styled input."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from rich.text import Text
from tic_tac_toe_3x3.game.players import Player
from tic_tac_toe_3x3.logic.exceptions import InvalidMove
from tic_tac_toe_3x3.logic.models import GameState, Mark, Move

if TYPE_CHECKING:
    from my_tic_tac_toe.renderer import RichRenderer


def grid_to_index(grid: str) -> int:
    """Convert grid coordinates to cell index.

    Args:
        grid: Coordinates like "a1", "A1", "1a", "1A".

    Returns:
        Cell index from 0 to 8.

    Raises:
        ValueError: If coordinates are invalid.
    """
    grid = grid.strip()
    if re.match(r"[abcABC][123]", grid):
        col, row = grid[0], grid[1]
    elif re.match(r"[123][abcABC]", grid):
        row, col = grid[0], grid[1]
    else:
        raise ValueError("Invalid grid coordinates")
    return 3 * (int(row) - 1) + (ord(col.upper()) - ord("A"))


class RichPlayer(Player):
    """Human player with Rich-styled console input.

    Uses renderer's get_input() for in-place display updates.
    """

    def __init__(self, mark: Mark, renderer: RichRenderer) -> None:
        """Initialize the Rich player.

        Args:
            mark: Player's mark (X or O).
            renderer: RichRenderer instance for display.
        """
        super().__init__(mark)
        self.renderer = renderer

    def get_move(self, game_state: GameState) -> Move | None:
        """Get the player's move.

        Args:
            game_state: Current game state.

        Returns:
            Move object with the new game state, or None if game is over.
        """
        while not game_state.game_over:
            prompt = Text()
            prompt.append(f"{self.mark}", style="bold yellow")
            prompt.append("'s move: ", style="yellow")

            try:
                user_input = self.renderer.get_input(prompt)
                index = grid_to_index(user_input)
            except ValueError:
                self.renderer.show_error(
                    "Please provide coordinates in the form of A1 or 1A"
                )
                continue

            try:
                return game_state.make_move_to(index)
            except InvalidMove:
                self.renderer.show_error("That cell is already occupied.")

        return None
