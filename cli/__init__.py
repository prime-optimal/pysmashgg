"""Command-line interface for pysmashgg."""

import typer
from rich.console import Console

__version__ = "0.2.0"  # Updated version for new player command

app = typer.Typer(help="Command-line interface for pysmashgg")
console = Console()

from .commands import search, results, player  # noqa
