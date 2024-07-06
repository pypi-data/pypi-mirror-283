"""Facilities for slicing and dicing asciicinema files."""

from __future__ import annotations

import orjson
import typer
import os
from rich.table import Table
from rich import print as rprint
from dataclasses import dataclass
from pydantic import BaseModel

app = typer.Typer(name="Asciicut", short_help="Slice and dice .cast files")


class Env(BaseModel):
    SHELL: str
    TERM: str


# Pydantic models
class Header(BaseModel):
    version: int
    width: int
    height: int
    timestamp: int
    env: Env


@dataclass
class Event:
    """Single Asciicast event."""

    timestamp: float
    event_type: str
    chars: str

    def __iter__(self):
        yield self.timestamp
        yield self.event_type
        yield self.chars

    def to_line(self) -> str:
        """Return this event as a single line in our .cast file."""
        return orjson.dumps(list(self)).decode()

    def add_time(self, time_s: float) -> Event:
        """Create a new event with the added time."""
        return Event(self.timestamp + time_s, self.event_type, self.chars)

    @staticmethod
    def from_list(items: list) -> Event:
        timestamp, event_type, chars = items
        return Event(timestamp, event_type, chars)


@dataclass
class AsciiCast:
    """A complete ascii cast file."""

    header: Header
    events: list[Event]

    def duration(self) -> float:
        """The duration of this ascii cast."""
        return self.events[-1].timestamp

    def n_events(self) -> int:
        """The number of unique events in this cast."""
        return len(self.events)

    def shave_time_beginning(self, time_s: float) -> AsciiCast:
        """Return a new AsciiCast with the first `time_s` dropped."""
        new_events = [e.add_time(time_s) for e in self.events if e.timestamp >= time_s]
        return AsciiCast(header=self.header, events=new_events)

    def to_lines(self) -> list[str]:
        """Return this asciicast as a list of strings."""
        header_line = self.header.model_dump_json()
        body_lines = [e.to_line() for e in self.events]

        lines = [header_line]
        lines.extend(body_lines)

        return lines

    def to_str(self) -> str:
        """Return a string of this asciicasts file contents."""
        return "\n".join(self.to_lines())

    def write(self, filename_out: str):
        """Write the contents of this asciicast to disk."""
        with open(filename_out, "w") as file:
            file.write(self.to_str())

    @staticmethod
    def from_file(filename: str) -> AsciiCast:
        with open(filename) as file:
            objects = [orjson.loads(line) for line in file.readlines() if line.strip()]
            header = Header.model_validate(objects[0])
            events = [Event.from_list(lst) for lst in objects[1:]]

            return AsciiCast(header=header, events=events)


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
    table.add_column("Duration (s)")
    table.add_column("Events")

    for file, cast in zip(filenames, casts):
        table.add_row(file, str(cast.duration()), str(cast.n_events()))

    return table


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


if __name__ == "__main__":
    app()
