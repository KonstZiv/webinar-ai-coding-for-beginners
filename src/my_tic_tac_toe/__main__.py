"""Entry point to play Tic-Tac-Toe with RichRenderer."""

import argparse

from tic_tac_toe_3x3.console_simple.players import ConsolePlayer
from tic_tac_toe_3x3.game.engine import TicTacToe
from tic_tac_toe_3x3.game.players import MinimaxComputerPlayer, RandomComputerPlayer
from tic_tac_toe_3x3.logic.models import Mark

from my_tic_tac_toe import RichRenderer


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Play Tic-Tac-Toe with a beautiful Rich renderer.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m my_tic_tac_toe              # Two human players
  python -m my_tic_tac_toe --ai         # Play against Minimax AI (unbeatable)
  python -m my_tic_tac_toe --ai random  # Play against Random AI
  python -m my_tic_tac_toe --ai-first   # AI plays first (X)
""",
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
            player2 = ConsolePlayer(Mark.NAUGHT)
        else:
            player1 = ConsolePlayer(Mark.CROSS)
            player2 = ai_class(Mark.NAUGHT)
    else:
        player1 = ConsolePlayer(Mark.CROSS)
        player2 = ConsolePlayer(Mark.NAUGHT)

    TicTacToe(player1, player2, renderer).play()


if __name__ == "__main__":
    main()
