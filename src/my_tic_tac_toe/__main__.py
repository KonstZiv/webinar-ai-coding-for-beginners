"""Entry point to play Tic-Tac-Toe with RichRenderer."""

import argparse

from tic_tac_toe_3x3.game.engine import TicTacToe
from tic_tac_toe_3x3.game.players import MinimaxComputerPlayer, RandomComputerPlayer
from tic_tac_toe_3x3.logic.models import Mark

from my_tic_tac_toe import RichRenderer
from my_tic_tac_toe.player import RichPlayer


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Play Tic-Tac-Toe with a beautiful Rich renderer.",
    )
    parser.add_argument(
        "--ai",
        nargs="?",
        const="minimax",
        choices=["minimax", "random"],
        help="Play against AI (default: minimax). Options: minimax, random",
    )
    parser.add_argument(
        "--ai-first",
        action="store_true",
        help="AI plays first (as X). By default, human plays first.",
    )
    return parser.parse_args()


def main() -> None:
    """Start a game of Tic-Tac-Toe."""
    args = parse_args()
    renderer = RichRenderer()

    if args.ai:
        ai_class = (
            MinimaxComputerPlayer if args.ai == "minimax" else RandomComputerPlayer
        )

        if args.ai_first:
            player1 = ai_class(Mark.CROSS)
            player2 = RichPlayer(Mark.NAUGHT, renderer)
        else:
            player1 = RichPlayer(Mark.CROSS, renderer)
            player2 = ai_class(Mark.NAUGHT)
    else:
        player1 = RichPlayer(Mark.CROSS, renderer)
        player2 = RichPlayer(Mark.NAUGHT, renderer)

    TicTacToe(player1, player2, renderer).play()


if __name__ == "__main__":
    main()
