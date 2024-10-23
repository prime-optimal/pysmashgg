"""CLI package for pysmashgg."""

from typing import Optional
import typer
from rich.console import Console

app = typer.Typer(help="Fetch and display Smash.gg tournament information")
console = Console()

from .commands import search, results  # noqa

__version__ = "1.4.0"
