"""This module stores the tests for all classes and functions available from the utilities.py module."""

import os
import re
import sys
import tempfile
import textwrap
from pathlib import Path
from typing import Any, Generator

import pytest
from pydantic import ValidationError

from ataraxis_base_utilities import Console, LogBackends, LogLevel


@pytest.fixture
def temp_dir() -> Generator[Path, Any, None]:
    """Generates and yields the temporary directory used by the tests that involve log file operations."""
    tmpdirname: str
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield Path(tmpdirname)


def error_format(message: str) -> str:
    """Formats the input message to match the default Console format and escapes it using re, so that it can be used to
    verify raised exceptions.

    This method is used to setup pytest 'match' clauses to verify raised exceptions.
    """
    return re.escape(textwrap.fill(message, width=120, break_long_words=False, break_on_hyphens=False))


@pytest.mark.parametrize("backend", [LogBackends.LOGURU, LogBackends.CLICK])
def test_console_initialization(backend, temp_dir) -> None:
    """Tests successful console initialization."""
    console = Console(
        logger_backend=backend,
        message_log_path=temp_dir / "message.log",
        error_log_path=temp_dir / "error.log",
        debug_log_path=temp_dir / "debug.log",
    )
    assert console._backend == backend
    assert console._message_log_path == temp_dir / "message.log"
    assert console._error_log_path == temp_dir / "error.log"
    assert console._debug_log_path == temp_dir / "debug.log"


@pytest.mark.parametrize("backend", [LogBackends.LOGURU, LogBackends.CLICK])
def test_console_invalid_initialization_argument_type(backend, temp_dir) -> None:
    """Tests that pydantic wrapper successfully catches and handles invalid initialization argument types.

    Also verifies that pydantic attempts to convert valid equivalents to correct type, eg: int 1 -> bool True.
    """
    with pytest.raises(ValidationError):
        # noinspection PyTypeChecker
        Console(logger_backend=None)
    with pytest.raises(ValidationError):
        # noinspection PyTypeChecker
        Console(message_log_path=123)
    with pytest.raises(ValidationError):
        # noinspection PyTypeChecker
        Console(line_width="None")
    with pytest.raises(ValidationError):
        # noinspection PyTypeChecker
        Console(break_on_hyphens=None)
    # noinspection PyTypeChecker
    Console(break_on_hyphens=1)  # Works due to pydantic automatically parsing bool-equivalents as bools.
    with pytest.raises(ValidationError):
        # noinspection PyTypeChecker
        Console(use_color=None)


@pytest.mark.parametrize("backend", [LogBackends.LOGURU, LogBackends.CLICK])
def test_console_invalid_initialization_line_width(backend) -> None:
    """Tests invalid line_width input during Console initialization."""

    # Uses an invalid width of <= 0
    message = (
        f"Invalid 'line_width' argument encountered when instantiating Console class instance. "
        f"Expected a value greater than 0, but encountered {0}."
    )
    with pytest.raises(ValueError, match=error_format(message)):
        Console(logger_backend=backend, line_width=0)


@pytest.mark.parametrize("backend", [LogBackends.LOGURU, LogBackends.CLICK])
def test_console_invalid_initialization_log_paths(backend, temp_dir) -> None:
    """Tests invalid path inputs during Console initialization."""
    valid_extensions: set[str] = {".txt", ".log", ".json"}

    # Uses a non-supported 'zipp' extension to trigger ValueErrors.
    message = (
        f"Invalid 'debug_log_path' argument encountered when instantiating Console class instance. "
        f"Expected a path ending in a file name with one of the supported extensions:"
        f"{', '.join(valid_extensions)}, but encountered {temp_dir / 'invalid.zipp'}."
    )
    with pytest.raises(ValueError, match=error_format(message)):
        Console(logger_backend=backend, debug_log_path=temp_dir / "invalid.zipp")
    message = (
        f"Invalid 'message_log_path' argument encountered when instantiating Console class instance. "
        f"Expected a path ending in a file name with one of the supported extensions:"
        f"{', '.join(valid_extensions)}, but encountered {temp_dir / 'invalid.zipp'}."
    )
    with pytest.raises(ValueError, match=error_format(message)):
        Console(logger_backend=backend, message_log_path=temp_dir / "invalid.zipp")
    message = (
        f"Invalid 'error_log_path' argument encountered when instantiating Console class instance. "
        f"Expected a path ending in a file name with one of the supported extensions:"
        f"{', '.join(valid_extensions)}, but encountered {temp_dir / 'invalid.zipp'}."
    )
    with pytest.raises(ValueError, match=error_format(message)):
        Console(logger_backend=backend, error_log_path=temp_dir / "invalid.zipp")


@pytest.mark.parametrize("backend", [LogBackends.LOGURU, LogBackends.CLICK])
def test_console_add_handles(backend, tmp_path, capsys) -> None:
    """Verifies that add_handles method works as expected for all supported backends."""
    # Setup
    debug_log = tmp_path / "debug.log"
    message_log = tmp_path / "message.log"
    error_log = tmp_path / "error.log"
    console = Console(
        logger_backend=backend, debug_log_path=debug_log, message_log_path=message_log, error_log_path=error_log
    )

    # Tests LOGURU backend
    if backend == LogBackends.LOGURU:
        # Removes existing handlers
        console._logger.remove()

        # Tests default behavior
        console.add_handles()
        assert len(console._logger._core.handlers) == 2  # Only message_terminal by default

        # Removes handlers for next test
        console._logger.remove()

        # Tests with all handlers
        console.add_handles(
            debug_terminal=True,
            debug_file=True,
            message_terminal=True,
            message_file=True,
            error_terminal=True,
            error_file=True,
        )
        assert len(console._logger._core.handlers) == 6

        # Tests each handler
        logger = console._logger.bind(ataraxis_terminal=True, ataraxis_log=True)
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")

        captured = capsys.readouterr()

        # Checks terminal output
        assert "Debug message" in captured.out
        assert "Info message" in captured.out
        assert "Warning message" in captured.out
        assert "Error message" in captured.err

        # Checks file output
        debug_log_content = debug_log.read_text()
        message_log_content = message_log.read_text()
        error_log_content = error_log.read_text()

        assert "Debug message" in debug_log_content
        assert "Info message" in message_log_content
        assert "Warning message" in message_log_content
        assert "Error message" in error_log_content

        # Tests removing handlers
        console._logger.remove()
        assert len(console._logger._core.handlers) == 0

    # Tests CLICK backend
    elif backend == LogBackends.CLICK:
        # For CLICK backend, add_handles should do nothing
        initial_handlers = len(console._logger._core.handlers) if console._logger else 0
        console.add_handles()
        assert len(console._logger._core.handlers) if console._logger else 0 == initial_handlers

    # Tests has_handles property. Should be 0 for both backends, as loguru tests involves removing all handles and
    # click backend does not instantiate handles in the first place.
    assert not console.has_handles

    # Enables the console and adds handles for the tests below to work for both backends
    console.enable()
    console.add_handles(
        debug_terminal=True,
        debug_file=True,
        message_terminal=True,
        message_file=True,
        error_terminal=True,
        error_file=True,
    )

    # Tests echo method for both backends
    console.echo("Test debug", LogLevel.DEBUG, terminal=True, log=True)
    console.echo("Test message", LogLevel.INFO, terminal=True, log=True)
    console.echo("Test error", LogLevel.ERROR, terminal=True, log=True)

    captured = capsys.readouterr()
    if backend == LogBackends.LOGURU:
        assert "Test debug" in captured.out
        assert "Test message" in captured.out
        assert "Test error" in captured.err
    elif backend == LogBackends.CLICK:
        assert "Test message" in captured.out
        assert "Test error" in captured.err

    # Checks log files for both backends
    assert "Test debug" in debug_log.read_text()
    assert "Test message" in message_log.read_text()
    assert "Test error" in error_log.read_text()


def test_loguru_specific_functionality() -> None:
    """Verifies initialization functionality specific to loguru backend."""
    console = Console(logger_backend=LogBackends.LOGURU)
    assert console._logger is not None


def test_click_specific_functionality(capsys) -> None:
    """Verifies initialization functionality specific to click backend."""

    # Console works without adding any handles
    console = Console(logger_backend=LogBackends.CLICK)
    console.enable()
    console.echo("Click message", LogLevel.INFO)
    captured = capsys.readouterr()
    assert "Click message" in captured.out

    # Console does not have a logger instance.
    assert console._logger is None


@pytest.mark.parametrize("backend", [LogBackends.LOGURU, LogBackends.CLICK])
def test_console_enable_disable(backend) -> None:
    """Tests the functionality of the console enable / disable methods and the is_enabled property."""

    # tests enable / disable methods and is_enabled tracker
    console = Console(logger_backend=backend)
    assert not console.is_enabled
    console.enable()
    assert console.is_enabled
    console.disable()
    assert not console.is_enabled

    # Verifies that echo does not process input messages when the console is disabled
    assert not console.echo(message="Test", level=LogLevel.INFO)


@pytest.mark.parametrize("backend", [LogBackends.LOGURU, LogBackends.CLICK])
def test_console_format_message(backend) -> None:
    """Verifies that loguru and non-loguru message formatting works as expected for all backends."""
    console = Console(logger_backend=backend, line_width=120)
    message = "This is a long message that should be wrapped properly according to the specified parameters"

    # Tests non-loguru wrapping
    formatted = console.format_message(message, loguru=False)
    assert len(max(formatted.split("\n"), key=len)) <= 120

    # Tests loguru wrapping
    formatted = console.format_message(message, loguru=True)
    lines = formatted.split("\n")

    # Checks first line (should be 83 characters or fewer due to 37-character loguru header)
    assert len(lines[0]) <= 83  # 120 - 37 = 83

    # Checks subsequent lines (should be 120 characters or fewer, with at least 37 characters of indentation)
    for line in lines[1:]:
        assert len(line) <= 120
        assert line.startswith(" " * 37)

    # Ensures that the wrapped message is not empty
    assert formatted.strip() != ""

    # Ensures that the entire original message is contained within the formatted version
    # We'll use a more flexible comparison that ignores spaces and newlines
    formatted_content = re.sub(r"\s+", "", formatted)
    message_content = re.sub(r"\s+", "", message)
    assert message_content in formatted_content

    # Additional check to ensure all words are present in the correct order
    formatted_words = re.findall(r"\w+", formatted)
    message_words = re.findall(r"\w+", message)
    assert formatted_words == message_words


@pytest.mark.parametrize("backend", [LogBackends.LOGURU, LogBackends.CLICK])
def test_console_format_message_errors(backend) -> None:
    """Verifies the format_message() error-handling functionality."""
    console = Console(logger_backend=backend, line_width=120)
    with pytest.raises(ValidationError):
        # noinspection PyTypeChecker
        console.format_message(message=123)
    with pytest.raises(ValidationError):
        # noinspection PyTypeChecker,PyArgumentList
        console.format_message(loguru=None)


@pytest.mark.parametrize("backend", [LogBackends.LOGURU, LogBackends.CLICK])
def test_console_echo(backend, tmp_path, capsys):
    # Setup
    debug_log = tmp_path / "debug.log"
    message_log = tmp_path / "message.log"
    error_log = tmp_path / "error.log"

    console = Console(
        logger_backend=backend, debug_log_path=debug_log, message_log_path=message_log, error_log_path=error_log
    )
    console.enable()
    console.add_handles(
        debug_terminal=True,
        debug_file=True,
        message_terminal=True,
        message_file=True,
        error_terminal=True,
        error_file=True,
    )

    # Tests each log level
    log_levels = [
        (LogLevel.DEBUG, debug_log),
        (LogLevel.INFO, message_log),
        (LogLevel.SUCCESS, message_log),
        (LogLevel.WARNING, message_log),
        (LogLevel.ERROR, error_log),
        (LogLevel.CRITICAL, error_log),
    ]

    for level, log_file in log_levels:
        message = f"Test {level.name} message"
        result = console.echo(message, level, terminal=True, log=True)

        assert result is True  # echo should return True when successful

        captured = capsys.readouterr()

        if level in [LogLevel.ERROR, LogLevel.CRITICAL]:
            assert message in captured.err
        else:
            assert message in captured.out

        assert os.path.exists(log_file)
        with open(log_file, "r") as f:
            assert message in f.read()

    # Tests terminal-only output
    result = console.echo("Terminal only", LogLevel.INFO, terminal=True, log=False)
    assert result is True
    captured = capsys.readouterr()
    assert "Terminal only" in captured.out
    with open(message_log, "r") as f:
        assert "Terminal only" not in f.read()

    # Tests log-only output
    result = console.echo("Log only", LogLevel.INFO, terminal=False, log=True)
    assert result is True
    captured = capsys.readouterr()
    assert "Log only" not in captured.out
    with open(message_log, "r") as f:
        assert "Log only" in f.read()

    # Tests when disabled console behavior
    console.disable()
    result = console.echo("Disabled message", LogLevel.INFO, terminal=True, log=True)
    assert result is False
    captured = capsys.readouterr()
    assert "Disabled message" not in captured.out
    with open(message_log, "r") as f:
        assert "Disabled message" not in f.read()

    # Tests with a very long message
    long_message = "This is a very long message " * 20
    result = console.echo(long_message, LogLevel.INFO, terminal=True, log=True)
    assert result is False  # Because console is still disabled
    captured = capsys.readouterr()
    assert long_message not in captured.out
    with open(message_log, "r") as f:
        assert long_message not in f.read()

    # Re-enables console and tests long message again
    console.enable()
    long_message = "This is a very long message " * 20
    result = console.echo(long_message, LogLevel.INFO, terminal=True, log=True)
    assert result is True
    captured = capsys.readouterr()

    if backend == LogBackends.LOGURU:
        # Removes ANSI color codes, timestamps, and log levels
        cleaned_output = re.sub(r"\x1b\[[0-9;]*m", "", captured.out)
        cleaned_output = re.sub(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3} \| \w+\s+\| ", "", cleaned_output)
        # Remove extra spaces and newlines
        cleaned_output = " ".join(cleaned_output.split())
    else:  # CLICK
        # Removes extra spaces and newlines
        cleaned_output = " ".join(captured.out.split())

    # Removes extra spaces from long_message for comparison
    cleaned_long_message = " ".join(long_message.split())

    assert cleaned_long_message in cleaned_output

    # Checks log file
    with open(message_log, "r") as f:
        log_content = f.read()
        assert cleaned_long_message in " ".join(log_content.split())


@pytest.mark.parametrize("backend", [LogBackends.LOGURU, LogBackends.CLICK])
def test_console_echo_errors(backend, tmp_path, capsys):
    """Verifies the echo() error-handling functionality."""
    console = Console(
        logger_backend=backend,
        debug_log_path=tmp_path / "debug.log",
        message_log_path=tmp_path / "message.log",
        error_log_path=tmp_path / "error.log",
    )
    console.enable()
    console.add_handles()

    # Tests invalid message type
    with pytest.raises(ValidationError):
        # noinspection PyTypeChecker
        console.echo(message=123, level=LogLevel.INFO)

    # Tests invalid level type
    with pytest.raises(ValidationError):
        # noinspection PyTypeChecker
        console.echo(message="Test message", level="INFO")

    # Tests invalid, but bool-convertible terminal flag type
    # noinspection PyTypeChecker
    result = console.echo(message="Test message", level=LogLevel.INFO, terminal="True")
    assert result is True  # Assuming "True" is converted to True

    # Tests invalid, but bool-convertible log flag type
    # noinspection PyTypeChecker
    result = console.echo(message="Test message", level=LogLevel.INFO, log="True")
    assert result is True  # Assuming "True" is converted to True

    # Tests non-boolean invalid flag handling
    with pytest.raises(ValidationError):
        # noinspection PyTypeChecker
        console.echo(message="Test message", level=LogLevel.INFO, log="123")

    # Tests error when using Loguru backend without handles
    if backend == LogBackends.LOGURU:
        console._logger.remove()  # Remove all handlers
        message = (
            f"Unable to echo the requested message: {'Test message'}. The Console class is configured to use the "
            f"loguru backend, but it does not have any handles. Call add_handles() method to add "
            f"handles or disable() to disable Console operation."
        )
        with pytest.raises(RuntimeError, match=error_format(message)):
            console.echo("Test message", LogLevel.INFO)

        console.add_handles()  # Re-adds handles for the tests below work

    # Tests behavior when console is disabled
    console.disable()
    result = console.echo("Test message", LogLevel.INFO)
    assert result is False

    # Re-enables and test valid call (should not raise any exception)
    console.enable()
    try:
        result = console.echo("Test message", LogLevel.INFO)
        assert result is True
    except Exception as e:
        pytest.fail(f"Valid echo call raised an unexpected exception: {e}")

    # Capture and check the output
    captured = capsys.readouterr()
    if backend == LogBackends.LOGURU:
        assert "Test message" in captured.out
    else:  # CLICK
        assert "Test message" in captured.out

    # Clear captured output
    capsys.readouterr()


@pytest.mark.parametrize("backend", [LogBackends.LOGURU, LogBackends.CLICK])
def test_console_error(backend, tmp_path, capsys):
    """Verifies that the error() console method functions as expected for all backends."""
    console = Console(logger_backend=backend, error_log_path=tmp_path / "error.log")
    console.enable()
    console.add_handles(error_terminal=True, error_file=True)

    # Tests successful error raising and logging
    with pytest.raises(RuntimeError, match="Test error"):
        console.error("Test error", RuntimeError, terminal=True, log=True)

    captured = capsys.readouterr()
    assert "Test error" in captured.err
    assert os.path.exists(tmp_path / "error.log")
    with open(tmp_path / "error.log", "r") as f:
        assert "Test error" in f.read()

    # Tests error without reraise
    console.error("No reraise error", ValueError, terminal=True, log=True, reraise=False)
    captured = capsys.readouterr()
    assert "No reraise error" in captured.err
    with open(tmp_path / "error.log", "r") as f:
        assert "No reraise error" in f.read()

    # Tests custom exception
    class CustomError(Exception):
        pass

    with pytest.raises(CustomError):
        console.error("Custom error", CustomError, terminal=True, log=True)

    # Capture and check the output
    captured = capsys.readouterr()
    assert "Custom error" in captured.err

    # Tests callback (only for Loguru backend)
    if backend == LogBackends.LOGURU:
        callback_called = False

        def callback_func(_error):
            nonlocal callback_called
            callback_called = True
            print("Callback executed", file=sys.stderr)

        # noinspection PyTypeChecker
        console.error("Callback error", ValueError, callback=callback_func, terminal=True, log=True, reraise=False)
        captured = capsys.readouterr()
        assert "Callback error" in captured.err
        assert "Callback executed" in captured.err
        assert callback_called

    # Checks that all errors were logged
    with open(tmp_path / "error.log", "r") as f:
        log_content = f.read()
        assert "Test error" in log_content
        assert "No reraise error" in log_content
        assert "Custom error" in log_content
        if backend == LogBackends.LOGURU:
            assert "Callback error" in log_content


@pytest.mark.parametrize("backend", [LogBackends.LOGURU, LogBackends.CLICK])
def test_console_error_output_options(backend, tmp_path, capsys):
    """Verifies that different error logging destinations work as expected."""
    error_log = tmp_path / "error.log"
    console = Console(logger_backend=backend, error_log_path=error_log)
    console.enable()
    console.add_handles(error_terminal=True, error_file=True)

    # Tests terminal only
    console.error("Terminal only", RuntimeError, terminal=True, log=False, reraise=False)
    captured = capsys.readouterr()
    assert "Terminal only" in captured.err

    # Loguru automatically creates an empty log file, click backend does not create the file
    if backend == LogBackends.LOGURU:
        assert error_log.read_text() == ""
    else:
        assert not os.path.exists(error_log)

    # Tests log only
    console.error("Log only", RuntimeError, terminal=False, log=True, reraise=False)
    captured = capsys.readouterr()
    assert captured.err == ""
    with open(tmp_path / "error.log", "r") as f:
        assert "Log only" in f.read()

    # Tests neither terminal nor log
    console.error("Neither", RuntimeError, terminal=False, log=False, reraise=False)
    captured = capsys.readouterr()
    assert captured.err == ""
    with open(tmp_path / "error.log", "r") as f:
        assert "Neither" not in f.read()


@pytest.mark.parametrize("backend", [LogBackends.LOGURU, LogBackends.CLICK])
def test_console_error_handling(backend, tmp_path):
    """Verifies error-handling functionality for the error() method."""
    console = Console(logger_backend=backend, error_log_path=tmp_path / "error.log")
    console.enable()
    console.add_handles(error_terminal=True, error_file=True)

    # Tests disabled console. Disabled console is still expected to raise the error itself, but should not do any
    # additional processing.
    console.disable()
    with pytest.raises(RuntimeError, match=error_format("Disabled error")):
        console.error("Disabled error", RuntimeError, terminal=True, log=True)
    if backend == LogBackends.LOGURU:
        assert Path(tmp_path / "error.log").read_text() == ""
    else:
        assert not os.path.exists(tmp_path / "error.log")

    # Re-enables console for further tests
    console.enable()

    # Tests error handling
    with pytest.raises(ValidationError):
        # noinspection PyTypeChecker
        console.error(123, RuntimeError)  # Invalid message type

    with pytest.raises(ValidationError):
        # noinspection PyTypeChecker
        console.error("Test", "Not a callable")  # Invalid error type

    # Tests Loguru-specific error (no handles)
    if backend == LogBackends.LOGURU:
        console._logger.remove()
        message = (
            f"Unable to properly log the requested error ({RuntimeError}) with message {'No handles error'}. The "
            f"Console class is configured to use the loguru backend, but it does not have any handles. "
            f"Call add_handles() method to add handles or disable() to disable Console operation."
        )
        with pytest.raises(RuntimeError, match=error_format(message)):
            console.error("No handles error", RuntimeError)
