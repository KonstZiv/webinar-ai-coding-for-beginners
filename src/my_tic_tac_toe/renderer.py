"""Rich-based renderer for Tic-Tac-Toe game with ASCII art."""

import sys

from rich.console import Console
from rich.text import Text
from tic_tac_toe_3x3.game.renderers import Renderer
from tic_tac_toe_3x3.logic.models import GameState, Mark

from my_tic_tac_toe.cascade import CascadeAnimation

CELL_WIDTH = 17
CELL_HEIGHT = 7
ROW_LABEL_WIDTH = 3

# ANSI escape codes for cursor control
CURSOR_HOME = "\033[H"  # Move cursor to home position (top-left)
CLEAR_SCREEN = "\033[2J"  # Clear entire screen
CLEAR_TO_END = "\033[J"  # Clear from cursor to end of screen

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
    - In-place screen updates (no scrolling)
    """

    def __init__(self) -> None:
        """Initialize the renderer."""
        self.console = Console()
        self._cascade_played = False
        self._first_render = True
        self._current_state: GameState | None = None
        self._error_message: str | None = None

    def render(self, game_state: GameState) -> None:
        """Render the current game state.

        Args:
            game_state: Current state of the game.
        """
        self._current_state = game_state
        self._error_message = None

        if self._first_render:
            # First render - clear screen
            sys.stdout.write(CLEAR_SCREEN + CURSOR_HOME)
            sys.stdout.flush()
            self._first_render = False
        else:
            # Subsequent renders - move cursor to home and overwrite
            sys.stdout.write(CURSOR_HOME)
            sys.stdout.flush()

        self._print_content(game_state)

        # Play cascade animation on game over
        if game_state.game_over and not self._cascade_played:
            self._cascade_played = True
            self._play_cascade_animation(game_state)

    def _print_content(
        self, game_state: GameState, error_message: str | None = None
    ) -> None:
        """Print the game content.

        Args:
            game_state: Current game state.
            error_message: Optional error message to display.
        """
        self.console.print()
        board = self._build_board(game_state)
        self.console.print(board)
        self.console.print()

        status = self._get_status_text(game_state)
        self.console.print(status)

        if error_message:
            self.console.print()
            self.console.print(error_message, style="red")

        # Clear any remaining content from previous longer output
        sys.stdout.write(CLEAR_TO_END)
        sys.stdout.flush()

    def get_input(self, prompt: Text) -> str:
        """Get user input.

        Args:
            prompt: Styled prompt text.

        Returns:
            User input string.
        """
        return self.console.input(prompt)

    def show_error(self, message: str) -> None:
        """Show error message and redraw screen.

        Args:
            message: Error message to display.
        """
        self._error_message = message
        if self._current_state is not None:
            # Move cursor to home and redraw with error
            sys.stdout.write(CURSOR_HOME)
            sys.stdout.flush()
            self._print_content(self._current_state, message)

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

    def _play_cascade_animation(self, game_state: GameState) -> None:
        """Play the cascade falling animation.

        Args:
            game_state: Current game state.
        """
        # Determine frozen cells (winning cells stay in place, tie = all fall)
        frozen_cells = set(game_state.winning_cells) if game_state.winner else set()

        # Build board content for animation
        board_lines, board_styles = self._build_board_for_animation(game_state)

        # Create and run animation
        animation = CascadeAnimation(
            board_lines=board_lines,
            board_styles=board_styles,
            frozen_cells=frozen_cells,
            console=self.console,
        )
        animation.run()

    def _build_board_for_animation(
        self, game_state: GameState
    ) -> tuple[list[str], list[list[str | None]]]:
        """Build board content as plain strings with style information.

        Args:
            game_state: Current game state.

        Returns:
            Tuple of (lines, styles) where lines is list of strings
            and styles is 2D list of style strings.
        """
        cells = game_state.grid.cells
        winning_cells = game_state.winning_cells if game_state.game_over else []

        lines: list[str] = []
        styles: list[list[str | None]] = []

        # Column headers
        header = self._create_column_headers()
        header_str = header.plain
        lines.append(header_str)
        styles.append([None] * len(header_str))

        # Top border
        top_border = (
            " " * ROW_LABEL_WIDTH
            + "╔"
            + "═" * CELL_WIDTH
            + "╦"
            + "═" * CELL_WIDTH
            + "╦"
            + "═" * CELL_WIDTH
            + "╗"
        )
        lines.append(top_border)
        styles.append([None] * len(top_border))

        for row in range(3):
            row_content = self._build_row(row, cells, winning_cells)
            for i, line_text in enumerate(row_content):
                # Row label
                if i == CELL_HEIGHT // 2:
                    prefix = f" {row + 1} "
                else:
                    prefix = " " * ROW_LABEL_WIDTH

                line_str = prefix + line_text.plain
                lines.append(line_str)

                # Build styles for this line
                line_styles: list[str | None] = [None] * len(prefix)
                # Extract styles from Rich Text spans
                for start, end, style in line_text._spans:
                    style_str = str(style) if style else None
                    for idx in range(start, min(end, len(line_text.plain))):
                        if len(line_styles) <= len(prefix) + idx:
                            line_styles.extend(
                                [None] * (len(prefix) + idx - len(line_styles) + 1)
                            )
                        line_styles[len(prefix) + idx] = style_str
                # Pad to line length
                while len(line_styles) < len(line_str):
                    line_styles.append(None)
                styles.append(line_styles)

            # Separator or bottom border
            if row < 2:
                sep = (
                    " " * ROW_LABEL_WIDTH
                    + "╠"
                    + "═" * CELL_WIDTH
                    + "╬"
                    + "═" * CELL_WIDTH
                    + "╬"
                    + "═" * CELL_WIDTH
                    + "╣"
                )
            else:
                sep = (
                    " " * ROW_LABEL_WIDTH
                    + "╚"
                    + "═" * CELL_WIDTH
                    + "╩"
                    + "═" * CELL_WIDTH
                    + "╩"
                    + "═" * CELL_WIDTH
                    + "╝"
                )
            lines.append(sep)
            styles.append([None] * len(sep))

        # Status line
        status = self._get_status_text(game_state)
        lines.append("")  # Empty line
        styles.append([])
        lines.append(status.plain)
        status_styles: list[str | None] = []
        for start, end, style in status._spans:
            style_str = str(style) if style else None
            while len(status_styles) < end:
                status_styles.append(style_str if len(status_styles) >= start else None)
        while len(status_styles) < len(status.plain):
            status_styles.append("bold yellow")
        styles.append(status_styles)

        return lines, styles
