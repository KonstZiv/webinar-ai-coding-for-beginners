"""Entry point to play Tic-Tac-Toe with RichRenderer."""

from tic_tac_toe_3x3.console_simple.players import ConsolePlayer
from tic_tac_toe_3x3.game.engine import TicTacToe
from tic_tac_toe_3x3.logic.models import Mark

from my_tic_tac_toe import RichRenderer


def main() -> None:
    """Start a game of Tic-Tac-Toe with two console players."""
    player1 = ConsolePlayer(Mark.CROSS)
    player2 = ConsolePlayer(Mark.NAUGHT)
    renderer = RichRenderer()

    TicTacToe(player1, player2, renderer).play()


if __name__ == "__main__":
    main()
