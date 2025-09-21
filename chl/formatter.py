import logging
from typing import Optional

from colors import color


def get_ansi_colour(fg: Optional[str] = None, bg: Optional[str] = None, style: Optional[str] = None) -> str:
    return color("", fg=fg, bg=bg, style=style)[:-4]


class ColouredFormatter(logging.Formatter):
    def __init__(
        self,
        fmt: str,
        debug: str = "cyan",
        info: str = "green",
        warning: str = "yellow",
        error: str = "red",
        critical: str = get_ansi_colour(fg="red", style="bold"),
    ):
        super().__init__()
        reset = "\x1b[0m"
        format_str = fmt.replace("%(message)s", reset + "%(message)s")

        if not debug.startswith("\x1b"):
            debug = get_ansi_colour(fg=debug)
        if not info.startswith("\x1b"):
            info = get_ansi_colour(fg=info)
        if not warning.startswith("\x1b"):
            warning = get_ansi_colour(fg=warning)
        if not error.startswith("\x1b"):
            error = get_ansi_colour(fg=error)
        if not critical.startswith("\x1b"):
            critical = get_ansi_colour(fg=critical)

        self.level_formatters = {
            logging.DEBUG: logging.Formatter(fmt=debug + format_str),
            logging.INFO: logging.Formatter(fmt=info + format_str),
            logging.WARNING: logging.Formatter(fmt=warning + format_str),
            logging.ERROR: logging.Formatter(fmt=error + format_str),
            logging.CRITICAL: logging.Formatter(fmt=critical + format_str),
        }

    def format(self, record: logging.LogRecord) -> str:
        formatter = self.level_formatters.get(record.levelno)
        assert formatter is not None, f"No logging formatter found for {record.levelno}"
        return formatter.format(record)


# Tests


def test_get_ansi_colour():
    assert get_ansi_colour(fg="blue") == "\x1b[34m"
    assert get_ansi_colour(fg="red", bg="yellow", style="underline") == "\x1b[31;43;4m"


def test_colour_formatter():
    formatter = ColouredFormatter(
        "[cf test - %(levelname)s] %(message)s",
        debug="purple",
        info="green",
        warning=get_ansi_colour(fg="yellow", bg="white", style="italic"),
        error="red",
        critical="red",
    )
    reset_colour = "\x1b[0m"

    record = logging.LogRecord(
        name="test", level=logging.DEBUG, pathname="test", lineno=0, msg="debug test", args=(), exc_info=None
    )
    assert formatter.format(record) == f"{get_ansi_colour('purple')}[cf test - DEBUG] {reset_colour}debug test"

    record = logging.LogRecord(
        name="test", level=logging.INFO, pathname="test", lineno=0, msg="info test", args=(), exc_info=None
    )
    assert formatter.format(record) == f"{get_ansi_colour('green')}[cf test - INFO] {reset_colour}info test"

    record = logging.LogRecord(
        name="test", level=logging.WARNING, pathname="test", lineno=0, msg="warning test", args=(), exc_info=None
    )
    assert (
        formatter.format(record)
        == f"{get_ansi_colour('yellow', bg='white', style='italic')}[cf test - WARNING] {reset_colour}warning test"
    )

    record = logging.LogRecord(
        name="test", level=logging.ERROR, pathname="test", lineno=0, msg="error test", args=(), exc_info=None
    )
    assert formatter.format(record) == f"{get_ansi_colour('red')}[cf test - ERROR] {reset_colour}error test"

    record = logging.LogRecord(
        name="test", level=logging.CRITICAL, pathname="test", lineno=0, msg="critical test", args=(), exc_info=None
    )
    assert formatter.format(record) == f"{get_ansi_colour('red')}[cf test - CRITICAL] {reset_colour}critical test"

    # Just to complete coverage
    formatter = ColouredFormatter("[cf test - %(levelname)s] %(message)s", warning="orange")
    record = logging.LogRecord(
        name="test", level=logging.WARNING, pathname="test", lineno=0, msg="warning test", args=(), exc_info=None
    )
    assert (
        formatter.format(record)
        == f"{get_ansi_colour('orange')}[cf test - WARNING] {reset_colour}warning test"
    )

