"""Non-blocking keyboard input for Unix terminals."""

import atexit
import select
import sys
import termios
import tty
from types import TracebackType


class NonBlockingInput:
    """Context manager for non-blocking keyboard input.

    Uses termios and select for Unix-compatible non-blocking input.
    Automatically restores terminal settings on exit.

    Example:
        with NonBlockingInput() as kb:
            while True:
                key = kb.key_pressed()
                if key == " ":
                    break
    """

    def __init__(self) -> None:
        """Initialize the non-blocking input handler."""
        self._old_settings: list[int] | None = None
        self._fd = sys.stdin.fileno()

    def __enter__(self) -> NonBlockingInput:
        """Enable non-blocking mode."""
        self._old_settings = termios.tcgetattr(self._fd)
        tty.setcbreak(self._fd)
        atexit.register(self._restore)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Restore terminal settings."""
        self._restore()
        atexit.unregister(self._restore)

    def _restore(self) -> None:
        """Restore original terminal settings."""
        if self._old_settings is not None:
            termios.tcsetattr(self._fd, termios.TCSADRAIN, self._old_settings)

    def key_pressed(self) -> str | None:
        """Check if a key was pressed without blocking.

        Returns:
            The pressed key character, or None if no key was pressed.
        """
        if select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.read(1)
        return None
