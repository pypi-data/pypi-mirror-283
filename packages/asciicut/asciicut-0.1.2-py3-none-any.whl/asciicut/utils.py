"""Utilities."""

import orjson
import os

from .schema import Event, AsciiCast
from rich import print as rprint
from rich.table import Table


def get_lines(filename: str, drop_header: bool = False) -> list[list]:
    """Load all json lines in as a list."""
    with open(filename) as file:
        if drop_header:
            objects = [orjson.loads(l) for l in file.readlines()[:-1]]
        else:
            objects = [orjson.loads(l) for l in file.readlines()]

    return objects


def get_events(filename: str) -> list[Event]:
    """Retrieve the individual events in a .cast file."""
    lines = get_lines(filename, drop_header=True)
    events_out = []

    for l in lines:
        timestamp, event_type, chars = l
        events_out.append(Event(timestamp, event_type, chars))

    return events_out


def write_cast(filename_out: str, events: list[Event], header: dict):
    """Write a list of events and a header to an out file."""


def find_casts():
    """Print all * .cast files to the terminal."""
    cast_files = [f for f in os.listdir() if f.endswith(".cast")]
    ascii_casts = [AsciiCast.from_file(f) for f in cast_files]
    table = summarize_casts(cast_files, ascii_casts)
    rprint(table)


def summarize_casts(
    filenames: str,
    casts: list[AsciiCast],
    title: str = "Ascii Casts",
) -> Table:
    """Retrieve a table with information like file name, duration, and number of events."""

    table = Table(title=title)
    table.add_column("File")
    table.add_column("Start time")
    table.add_column("Duration (s)")
    table.add_column("Events")

    for file, cast in zip(filenames, casts):
        table.add_row(
            file,
            f"{cast.start_time():0.5}",
            f"{cast.duration():0.5}",
            str(cast.n_events()),
        )

    return table
