"""Main typer application."""

import typer
from .utils import find_casts
from .schema import AsciiCast

app = typer.Typer(
    name="Asciicut",
    short_help="Slice and dice .cast files",
    no_args_is_help=True,
)


@app.command()
def ls():
    """Load in and print the file."""
    find_casts()


@app.command()
def drop(filename: str, time_s: float):
    """Drop the first n seconds for an ascii cast."""
    cast = AsciiCast.from_file(filename)
    out = cast.shave_time_beginning(time_s)
    out_file = f"{filename[:-5]}_drop_{time_s:0.5}.cast"

    out.write(filename_out=out_file)
    find_casts()
