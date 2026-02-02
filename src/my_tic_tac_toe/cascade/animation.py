"""Cascade animation effect for game over."""

import math
import sys
import time

from rich.console import Console
from rich.text import Text

from .keyboard import NonBlockingInput
from .particle import Particle, is_in_frozen_area

# ANSI escape codes for cursor control
CURSOR_HOME = "\033[H"  # Move cursor to home position (top-left)
HIDE_CURSOR = "\033[?25l"  # Hide cursor
SHOW_CURSOR = "\033[?25h"  # Show cursor

# Pulse colors for winning cells (from dim to bright)
# Using grey scale for dim and bright colors for peak
PULSE_COLORS_RED = [
    "grey30",
    "grey42",
    "grey54",
    "grey66",
    "red",
    "bright_red",
    "bold bright_red",
]

PULSE_COLORS_BLUE = [
    "grey30",
    "grey42",
    "grey54",
    "grey66",
    "blue",
    "bright_blue",
    "bold bright_blue",
]


class CascadeAnimation:
    """Cascade falling animation for game over effect.

    Renders characters falling down and accumulating at the bottom
    of the screen, similar to the Cascade virus effect.
    """

    FPS = 25
    MIN_WIDTH = 60
    MIN_HEIGHT = 30

    def __init__(
        self,
        board_lines: list[str],
        board_styles: list[list[str | None]],
        frozen_cells: set[int],
        console: Console,
    ) -> None:
        """Initialize the cascade animation.

        Args:
            board_lines: List of strings representing board rows.
            board_styles: 2D list of Rich styles for each character.
            frozen_cells: Set of cell indices that should not fall.
            console: Rich Console instance.
        """
        self.console = console
        self.width, self.height = console.size

        # Initialize particles from board
        self.particles: list[Particle] = []
        self._init_particles(board_lines, board_styles, frozen_cells)

        # Floor height for each column (for accumulation)
        self.floor: list[int] = [self.height] * self.width

        # Pulse animation state
        self._frame_count = 0
        self._pulse_speed = 0.15  # How fast the pulse cycles

    def _init_particles(
        self,
        board_lines: list[str],
        board_styles: list[list[str | None]],
        frozen_cells: set[int],
    ) -> None:
        """Initialize particles from board content.

        Args:
            board_lines: List of strings representing board rows.
            board_styles: 2D list of Rich styles for each character.
            frozen_cells: Set of cell indices that should not fall.
        """
        for y, line in enumerate(board_lines):
            for x, char in enumerate(line):
                if char != " " and char != "\n":
                    style = (
                        board_styles[y][x]
                        if y < len(board_styles) and x < len(board_styles[y])
                        else None
                    )
                    frozen = is_in_frozen_area(x, y, frozen_cells)
                    particle = Particle.create(char, x, y, style, frozen)
                    self.particles.append(particle)

    def update(self) -> bool:
        """Update all particle positions.

        Returns:
            True if any particles are still moving.
        """
        still_moving = False

        for p in self.particles:
            if p.frozen or p.velocity == 0:
                # Skip frozen particles and particles that have already landed
                continue

            # Calculate target floor position for current column
            floor_y = self.floor[p.x] if 0 <= p.x < len(self.floor) else self.height

            # Check if particle reached floor/obstacle
            new_y = p.y + p.velocity
            if new_y >= floor_y - 1:
                # Particle hit something - try to slide sideways based on spin
                side_x = p.x + p.spin

                # Check if side position is valid and has room below current position
                if 0 <= side_x < len(self.floor):
                    side_floor = self.floor[side_x]
                    # Can slide if there's room below current y position
                    if side_floor > int(p.y) + 1:
                        # Slide to the side and continue falling
                        p.x = side_x
                        p.y = new_y
                        still_moving = True
                        continue

                # Can't slide - land here
                p.y = floor_y - 1
                if 0 <= p.x < len(self.floor):
                    self.floor[p.x] -= 1
                p.velocity = 0
            else:
                p.y = new_y
                still_moving = True

        return still_moving

    def render_frame(self) -> Text:
        """Render current animation state as Rich Text.

        Returns:
            Text object representing current frame.
        """
        # Create empty screen buffer
        screen: list[list[str]] = [
            [" " for _ in range(self.width)] for _ in range(self.height)
        ]
        styles: list[list[str | None]] = [
            [None for _ in range(self.width)] for _ in range(self.height)
        ]

        # Calculate pulse phase (0 to 1 to 0, sine wave)
        pulse_phase = (math.sin(self._frame_count * self._pulse_speed) + 1) / 2
        pulse_index = int(pulse_phase * (len(PULSE_COLORS_RED) - 1))

        # Place particles
        for p in self.particles:
            y = int(p.y)
            if 0 <= y < self.height and 0 <= p.x < self.width:
                screen[y][p.x] = p.char

                # Apply pulse effect to frozen (winning) particles
                if p.frozen and p.style:
                    if "red" in p.style.lower():
                        styles[y][p.x] = PULSE_COLORS_RED[pulse_index]
                    elif "blue" in p.style.lower():
                        styles[y][p.x] = PULSE_COLORS_BLUE[pulse_index]
                    else:
                        styles[y][p.x] = p.style
                else:
                    styles[y][p.x] = p.style

        # Convert to Rich Text
        result = Text()
        for row_idx, row in enumerate(screen):
            for col_idx, char in enumerate(row):
                style = styles[row_idx][col_idx]
                result.append(char, style=style)
            if row_idx < self.height - 1:
                result.append("\n")

        return result

    def run(self) -> None:
        """Run the cascade animation.

        Animation continues until all particles have fallen
        or Space is pressed.
        """
        # Skip if terminal too small
        if self.width < self.MIN_WIDTH or self.height < self.MIN_HEIGHT:
            return

        frame_time = 1.0 / self.FPS

        # Hide cursor during animation
        sys.stdout.write(HIDE_CURSOR)
        sys.stdout.flush()

        try:
            with NonBlockingInput() as kb:
                while True:
                    # Check for Space to interrupt
                    key = kb.key_pressed()
                    if key == " ":
                        break

                    # Update particles
                    still_moving = self.update()

                    # Update pulse frame counter
                    self._frame_count += 1

                    # Move cursor to home and render frame
                    sys.stdout.write(CURSOR_HOME)
                    sys.stdout.flush()
                    self.console.print(self.render_frame(), end="")

                    # Animation complete?
                    if not still_moving:
                        time.sleep(1.0)  # Pause before exit
                        break

                    time.sleep(frame_time)
        finally:
            # Show cursor again
            sys.stdout.write(SHOW_CURSOR)
            sys.stdout.flush()
