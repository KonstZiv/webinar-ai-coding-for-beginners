"""Tests for RichRenderer."""

import pytest
from rich.text import Text
from tic_tac_toe_3x3.game.renderers import Renderer
from tic_tac_toe_3x3.logic.models import GameState, Grid, Mark

from my_tic_tac_toe.renderer import (
    CELL_HEIGHT,
    CELL_WIDTH,
    O_ART,
    X_ART,
    RichRenderer,
)


class TestRichRendererInheritance:
    """Tests for RichRenderer class inheritance."""

    def test_inherits_from_renderer(self) -> None:
        """RichRenderer should inherit from base Renderer class."""
        assert issubclass(RichRenderer, Renderer)

    def test_instance_is_renderer(self) -> None:
        """RichRenderer instance should be instance of Renderer."""
        renderer = RichRenderer()
        assert isinstance(renderer, Renderer)


class TestAsciiArtConstants:
    """Tests for ASCII art constants."""

    def test_x_art_has_correct_height(self) -> None:
        """X_ART should have CELL_HEIGHT lines."""
        assert len(X_ART) == CELL_HEIGHT

    def test_x_art_has_correct_width(self) -> None:
        """Each line of X_ART should have CELL_WIDTH characters."""
        for line in X_ART:
            assert len(line) == CELL_WIDTH

    def test_o_art_has_correct_height(self) -> None:
        """O_ART should have CELL_HEIGHT lines."""
        assert len(O_ART) == CELL_HEIGHT

    def test_o_art_has_correct_width(self) -> None:
        """Each line of O_ART should have CELL_WIDTH characters."""
        for line in O_ART:
            assert len(line) == CELL_WIDTH


class TestGetStatusText:
    """Tests for _get_status_text method."""

    @pytest.fixture
    def renderer(self) -> RichRenderer:
        """Create a RichRenderer instance."""
        return RichRenderer()

    def test_status_x_turn(self, renderer: RichRenderer) -> None:
        """Should show X's turn for empty board."""
        game_state = GameState(Grid("         "))
        status = renderer._get_status_text(game_state)

        assert isinstance(status, Text)
        assert "Player X's turn" in status.plain

    def test_status_o_turn(self, renderer: RichRenderer) -> None:
        """Should show O's turn after X moves."""
        game_state = GameState(Grid("X        "))
        status = renderer._get_status_text(game_state)

        assert "Player 0's turn" in status.plain

    def test_status_x_wins(self, renderer: RichRenderer) -> None:
        """Should show X wins message."""
        game_state = GameState(Grid("XXX00    "))
        status = renderer._get_status_text(game_state)

        assert "Player X wins!" in status.plain

    def test_status_o_wins(self, renderer: RichRenderer) -> None:
        """Should show O wins message."""
        game_state = GameState(Grid("000XX X  "))
        status = renderer._get_status_text(game_state)

        assert "Player 0 wins!" in status.plain

    def test_status_tie(self, renderer: RichRenderer) -> None:
        """Should show tie message."""
        game_state = GameState(Grid("X0XX0X0X0"))
        status = renderer._get_status_text(game_state)

        assert "It's a tie!" in status.plain

    def test_status_has_yellow_style(self, renderer: RichRenderer) -> None:
        """Status text should have yellow style."""
        game_state = GameState(Grid("         "))
        status = renderer._get_status_text(game_state)

        assert status.style is not None
        assert "yellow" in str(status.style)


class TestGetCellLine:
    """Tests for _get_cell_line method."""

    @pytest.fixture
    def renderer(self) -> RichRenderer:
        """Create a RichRenderer instance."""
        return RichRenderer()

    def test_x_cell_returns_x_art(self, renderer: RichRenderer) -> None:
        """Should return X ASCII art for X cell."""
        for line_idx in range(CELL_HEIGHT):
            cell_line = renderer._get_cell_line(Mark.CROSS, line_idx, is_winning=False)
            assert cell_line.plain == X_ART[line_idx]

    def test_o_cell_returns_o_art(self, renderer: RichRenderer) -> None:
        """Should return O ASCII art for O cell."""
        for line_idx in range(CELL_HEIGHT):
            cell_line = renderer._get_cell_line(Mark.NAUGHT, line_idx, is_winning=False)
            assert cell_line.plain == O_ART[line_idx]

    def test_empty_cell_returns_spaces(self, renderer: RichRenderer) -> None:
        """Should return spaces for empty cell."""
        for line_idx in range(CELL_HEIGHT):
            cell_line = renderer._get_cell_line(" ", line_idx, is_winning=False)
            assert cell_line.plain == " " * CELL_WIDTH

    def test_x_cell_has_red_style(self, renderer: RichRenderer) -> None:
        """X cell should have red style."""
        cell_line = renderer._get_cell_line(Mark.CROSS, 0, is_winning=False)
        assert "red" in str(cell_line.style)

    def test_o_cell_has_blue_style(self, renderer: RichRenderer) -> None:
        """O cell should have blue style."""
        cell_line = renderer._get_cell_line(Mark.NAUGHT, 0, is_winning=False)
        assert "blue" in str(cell_line.style)

    def test_winning_x_cell_has_reverse_style(self, renderer: RichRenderer) -> None:
        """Winning X cell should have reverse style."""
        cell_line = renderer._get_cell_line(Mark.CROSS, 0, is_winning=True)
        assert "reverse" in str(cell_line.style)

    def test_winning_o_cell_has_reverse_style(self, renderer: RichRenderer) -> None:
        """Winning O cell should have reverse style."""
        cell_line = renderer._get_cell_line(Mark.NAUGHT, 0, is_winning=True)
        assert "reverse" in str(cell_line.style)


class TestBuildBoard:
    """Tests for _build_board method."""

    @pytest.fixture
    def renderer(self) -> RichRenderer:
        """Create a RichRenderer instance."""
        return RichRenderer()

    def test_board_contains_column_headers(self, renderer: RichRenderer) -> None:
        """Board should contain A, B, C column headers."""
        game_state = GameState(Grid("         "))
        board = renderer._build_board(game_state)
        board_text = board.plain

        assert "A" in board_text
        assert "B" in board_text
        assert "C" in board_text

    def test_board_contains_row_labels(self, renderer: RichRenderer) -> None:
        """Board should contain 1, 2, 3 row labels."""
        game_state = GameState(Grid("         "))
        board = renderer._build_board(game_state)
        board_text = board.plain

        # Row labels appear at the start of middle lines
        assert " 1 " in board_text
        assert " 2 " in board_text
        assert " 3 " in board_text

    def test_board_contains_double_line_borders(self, renderer: RichRenderer) -> None:
        """Board should contain double-line box drawing characters."""
        game_state = GameState(Grid("         "))
        board = renderer._build_board(game_state)
        board_text = board.plain

        assert "╔" in board_text
        assert "╗" in board_text
        assert "╚" in board_text
        assert "╝" in board_text
        assert "╦" in board_text
        assert "╩" in board_text
        assert "╠" in board_text
        assert "╣" in board_text
        assert "╬" in board_text
        assert "═" in board_text
        assert "║" in board_text

    def test_board_contains_x_art_when_x_placed(self, renderer: RichRenderer) -> None:
        """Board should contain X ASCII art when X is placed."""
        game_state = GameState(Grid("X        "))
        board = renderer._build_board(game_state)
        board_text = board.plain

        # Check that X art pattern is in the board
        assert "███████" in board_text

    def test_board_contains_o_art_when_o_placed(self, renderer: RichRenderer) -> None:
        """Board should contain O ASCII art when O is placed."""
        game_state = GameState(Grid("X0       "))
        board = renderer._build_board(game_state)
        board_text = board.plain

        # Check that O art pattern is in the board
        assert "█████████" in board_text


class TestRender:
    """Tests for render method."""

    @pytest.fixture
    def renderer(self) -> RichRenderer:
        """Create a RichRenderer instance."""
        return RichRenderer()

    def test_render_empty_board_no_error(self, renderer: RichRenderer) -> None:
        """Render should not raise error for empty board."""
        game_state = GameState(Grid("         "))
        renderer.render(game_state)

    def test_render_game_in_progress_no_error(self, renderer: RichRenderer) -> None:
        """Render should not raise error for game in progress."""
        game_state = GameState(Grid("X0X 0    "))
        renderer.render(game_state)

    def test_render_x_wins_no_error(self, renderer: RichRenderer) -> None:
        """Render should not raise error when X wins."""
        game_state = GameState(Grid("XXX00    "))
        renderer.render(game_state)

    def test_render_o_wins_no_error(self, renderer: RichRenderer) -> None:
        """Render should not raise error when O wins."""
        game_state = GameState(Grid("000XX X  "))
        renderer.render(game_state)

    def test_render_tie_no_error(self, renderer: RichRenderer) -> None:
        """Render should not raise error for tie."""
        game_state = GameState(Grid("X0XX0X0X0"))
        renderer.render(game_state)


class TestCreateColumnHeaders:
    """Tests for _create_column_headers method."""

    @pytest.fixture
    def renderer(self) -> RichRenderer:
        """Create a RichRenderer instance."""
        return RichRenderer()

    def test_headers_contain_all_labels(self, renderer: RichRenderer) -> None:
        """Headers should contain A, B, C labels."""
        headers = renderer._create_column_headers()
        header_text = headers.plain

        assert "A" in header_text
        assert "B" in header_text
        assert "C" in header_text

    def test_headers_are_text_object(self, renderer: RichRenderer) -> None:
        """Headers should be a Rich Text object."""
        headers = renderer._create_column_headers()
        assert isinstance(headers, Text)


class TestBuildRow:
    """Tests for _build_row method."""

    @pytest.fixture
    def renderer(self) -> RichRenderer:
        """Create a RichRenderer instance."""
        return RichRenderer()

    def test_row_has_correct_number_of_lines(self, renderer: RichRenderer) -> None:
        """Each row should have CELL_HEIGHT lines."""
        cells = "         "
        row_lines = renderer._build_row(0, cells, [])
        assert len(row_lines) == CELL_HEIGHT

    def test_row_lines_contain_separators(self, renderer: RichRenderer) -> None:
        """Row lines should contain vertical separators."""
        cells = "         "
        row_lines = renderer._build_row(0, cells, [])

        for line in row_lines:
            assert line.plain.count("║") == 4  # 3 cells = 4 separators


class TestWinningCellsHighlight:
    """Tests for winning cells highlight."""

    @pytest.fixture
    def renderer(self) -> RichRenderer:
        """Create a RichRenderer instance."""
        return RichRenderer()

    def _get_cell_styles(
        self, renderer: RichRenderer, game_state: GameState
    ) -> list[str | None]:
        """Extract styles for each cell.

        Returns list of 9 style strings (or None for empty cells).
        """
        cells = game_state.grid.cells
        winning_cells = game_state.winning_cells if game_state.game_over else []
        styles: list[str | None] = []

        for index in range(9):
            cell_content = cells[index]
            if cell_content == " ":
                styles.append(None)
            else:
                cell_line = renderer._get_cell_line(
                    cell_content, 0, index in winning_cells
                )
                styles.append(str(cell_line.style) if cell_line.style else None)

        return styles

    @pytest.mark.parametrize(
        (
            "grid",
            "starting_mark",
            "expected_winner",
            "expected_winning_cells",
            "description",
        ),
        [
            # Horizontal wins - X wins (X started, X>O)
            ("XXX00    ", Mark.CROSS, Mark.CROSS, [0, 1, 2], "top row"),
            ("00 XXX   ", Mark.CROSS, Mark.CROSS, [3, 4, 5], "middle row"),
            ("00 X0 XXX", Mark.CROSS, Mark.CROSS, [6, 7, 8], "bottom row"),
            # Vertical wins - X wins (X started, X>O)
            ("X00X  X  ", Mark.CROSS, Mark.CROSS, [0, 3, 6], "left column"),
            (" X00X 0XX", Mark.CROSS, Mark.CROSS, [1, 4, 7], "middle column"),
            (" 0X0 X  X", Mark.CROSS, Mark.CROSS, [2, 5, 8], "right column"),
            # Diagonal wins - X wins (X started, X>O)
            ("X00XX  0X", Mark.CROSS, Mark.CROSS, [0, 4, 8], "main diagonal"),
            (" 0X X X0 ", Mark.CROSS, Mark.CROSS, [2, 4, 6], "anti diagonal"),
        ],
        ids=[
            "horizontal-top",
            "horizontal-middle",
            "horizontal-bottom",
            "vertical-left",
            "vertical-middle",
            "vertical-right",
            "diagonal-main",
            "diagonal-anti",
        ],
    )
    def test_winning_cells_highlighted(
        self,
        renderer: RichRenderer,
        grid: str,
        starting_mark: Mark,
        expected_winner: Mark,
        expected_winning_cells: list[int],
        description: str,
    ) -> None:
        """Winning cells should be highlighted with reverse style."""
        game_state = GameState(Grid(grid), starting_mark)

        assert game_state.winner == expected_winner
        assert game_state.winning_cells == expected_winning_cells

        styles = self._get_cell_styles(renderer, game_state)

        # Check winning cells have reverse style
        for cell_idx in expected_winning_cells:
            assert styles[cell_idx] is not None, f"Cell {cell_idx} should have style"
            assert "reverse" in styles[cell_idx], (
                f"Winning cell {cell_idx} ({description}) should be highlighted"
            )

        # Check non-winning filled cells do NOT have reverse style
        for cell_idx in range(9):
            if cell_idx not in expected_winning_cells and styles[cell_idx] is not None:
                assert "reverse" not in styles[cell_idx], (
                    f"Non-winning cell {cell_idx} should not be highlighted"
                )

    def test_no_highlight_when_game_in_progress(self, renderer: RichRenderer) -> None:
        """No cells should be highlighted when game is in progress."""
        game_state = GameState(Grid("X0X 0    "))

        assert not game_state.game_over
        assert game_state.winning_cells == []

        styles = self._get_cell_styles(renderer, game_state)

        for i, style in enumerate(styles):
            if style is not None:
                assert "reverse" not in style, f"Cell {i} should not be highlighted"

    def test_no_highlight_on_tie(self, renderer: RichRenderer) -> None:
        """No cells should be highlighted on tie."""
        game_state = GameState(Grid("X0XX0X0X0"))

        assert game_state.tie
        assert game_state.winning_cells == []

        styles = self._get_cell_styles(renderer, game_state)

        for i, style in enumerate(styles):
            if style is not None:
                assert "reverse" not in style, f"Cell {i} should not be highlighted"
