from pathlib import Path
import click
import pyperclip
from code2prompt.utils.logging_utils import (
    log_output_created,
    log_error,
    log_clipboard_copy,
)


def write_output(content, output_path, copy_to_clipboard=True):
    """
    Writes the generated content to a file or prints it to the console,
    and copies the content to the clipboard.

    Parameters:
    - content (str): The content to be written, printed, and copied.
    - output_path (str): The path to the file where the content should be written.
                         If None, the content is printed to the console.
    - copy_to_clipboard (bool): Whether to copy the content to the clipboard.

    Returns:
    None
    """
    if output_path:
        try:
            with Path(output_path).open("w", encoding="utf-8") as output_file:
                output_file.write(content)
            log_output_created(output_path)
        except IOError as e:
            log_error(f"Error writing to output file: {e}")

    else:
        click.echo(content)

    log_clipboard_copy(success=True)
    if not copy_to_clipboard:
        return

    # Copy content to clipboard
    try:
        pyperclip.copy(content)
    # log_clipboard_copy(success=True)

    except Exception as _e:
        log_clipboard_copy(success=False)
