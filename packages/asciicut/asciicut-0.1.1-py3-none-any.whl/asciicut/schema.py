"""Pydantic Models and Dataclasses representing .cast files."""

from __future__ import annotations

from pydantic import BaseModel
from dataclasses import dataclass
import orjson


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
