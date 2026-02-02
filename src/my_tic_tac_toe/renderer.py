"""Rich-based renderer for Tic-Tac-Toe game with ASCII art."""

from rich.console import Console
from rich.text import Text
from tic_tac_toe_3x3.game.renderers import Renderer
from tic_tac_toe_3x3.logic.models import GameState, Mark

CELL_WIDTH = 17
CELL_HEIGHT = 7
ROW_LABEL_WIDTH = 3

# ASCII art for X (17x7)
X_ART = [
    "███           ███",
    "████         ████",
    "  ████     ████  ",
    "     ███████     ",
    "  ████     ████  ",
    "████         ████",
    "███           ███",
]

# ASCII art for O (17x7)
O_ART = [
    "    █████████    ",
    "  ███       ███  ",
    " ██           ██ ",
    "██             ██",
    " ██           ██ ",
    "  ███       ███  ",
    "    █████████    ",
]


class RichRenderer(Renderer):
    """Renderer that displays the game board using Rich library with ASCII art.

    Features:
    - Large 17x7 character cells with ASCII art
    - X markers in red, O markers in blue
    - Double-line box drawing borders
    - Column labels (A, B, C) and row labels (1, 2, 3)
    - Game status display below the board
    """

    def __init__(self) -> None:
        """Initialize the renderer."""
        self.console = Console()

    def render(self, game_state: GameState) -> None:
        """Render the current game state.

        Args:
            game_state: Current state of the game.
        """
        self.console.clear()
        self.console.print()

        board = self._build_board(game_state)
        self.console.print(board)
        self.console.print()

        status = self._get_status_text(game_state)
        self.console.print(status)

    def _build_board(self, game_state: GameState) -> Text:
        """Build the complete game board as a Rich Text object.

        Args:
            game_state: Current state of the game.

        Returns:
            Text object with the styled board.
        """
        cells = game_state.grid.cells
        winning_cells = game_state.winning_cells if game_state.game_over else []

        board = Text()

        # Column headers
        board.append_text(self._create_column_headers())
        board.append("\n")

        # Top border
        board.append(" " * ROW_LABEL_WIDTH)
        board.append(
            "╔"
            + "═" * CELL_WIDTH
            + "╦"
            + "═" * CELL_WIDTH
            + "╦"
            + "═" * CELL_WIDTH
            + "╗\n"
        )

        for row in range(3):
            row_lines = self._build_row(row, cells, winning_cells)
            for i, line in enumerate(row_lines):
                # Row label (centered vertically)
                if i == CELL_HEIGHT // 2:
                    board.append(f" {row + 1} ")
                else:
                    board.append(" " * ROW_LABEL_WIDTH)
                board.append_text(line)
                board.append("\n")

            # Horizontal separator or bottom border
            board.append(" " * ROW_LABEL_WIDTH)
            if row < 2:
                board.append(
                    "╠"
                    + "═" * CELL_WIDTH
                    + "╬"
                    + "═" * CELL_WIDTH
                    + "╬"
                    + "═" * CELL_WIDTH
                    + "╣\n"
                )
            else:
                board.append(
                    "╚"
                    + "═" * CELL_WIDTH
                    + "╩"
                    + "═" * CELL_WIDTH
                    + "╩"
                    + "═" * CELL_WIDTH
                    + "╝\n"
                )

        return board

    def _create_column_headers(self) -> Text:
        """Create column header line with A, B, C centered over cells.

        Returns:
            Text object with column headers.
        """
        header = Text()
        header.append(" " * ROW_LABEL_WIDTH)
        header.append(" ")  # Account for left border

        for col, label in enumerate(["A", "B", "C"]):
            padding = (CELL_WIDTH - 1) // 2
            header.append(" " * padding + label + " " * (CELL_WIDTH - padding - 1))
            if col < 2:
                header.append(" ")  # Account for separator

        return header

    def _build_row(self, row: int, cells: str, winning_cells: list[int]) -> list[Text]:
        """Build a single row of the board (3 cells).

        Args:
            row: Row index (0-2).
            cells: All cell contents.
            winning_cells: List of winning cell indices.

        Returns:
            List of Text objects, one per line in the row.
        """
        row_lines: list[Text] = []

        for line_idx in range(CELL_HEIGHT):
            line = Text()
            line.append("║")

            for col in range(3):
                index = row * 3 + col
                cell_content = cells[index]
                is_winning = index in winning_cells
                cell_line = self._get_cell_line(cell_content, line_idx, is_winning)
                line.append_text(cell_line)
                line.append("║")

            row_lines.append(line)

        return row_lines

    def _get_cell_line(self, cell: str, line_idx: int, is_winning: bool) -> Text:
        """Get a single line of ASCII art for a cell.

        Args:
            cell: Cell content (' ', 'X', or '0').
            line_idx: Line index within the cell (0-6).
            is_winning: Whether this cell is part of the winning line.

        Returns:
            Text object for this line.
        """
        if cell == Mark.CROSS:
            style = "bold red reverse" if is_winning else "bold red"
            return Text(X_ART[line_idx], style=style)

        if cell == Mark.NAUGHT:
            style = "bold blue reverse" if is_winning else "bold blue"
            return Text(O_ART[line_idx], style=style)

        return Text(" " * CELL_WIDTH)

    def _get_status_text(self, game_state: GameState) -> Text:
        """Get the status text for the current game state.

        Args:
            game_state: Current state of the game.

        Returns:
            Styled status text.
        """
        if game_state.winner:
            return Text(f"Player {game_state.winner} wins!", style="bold yellow")

        if game_state.tie:
            return Text("It's a tie!", style="bold yellow")

        return Text(f"Player {game_state.current_mark}'s turn", style="bold yellow")
