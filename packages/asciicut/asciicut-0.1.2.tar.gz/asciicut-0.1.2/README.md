# Asciicut

Simple CLI for trimming [asciinema](https://asciinema.org/) [`.cast`](https://docs.asciinema.org/manual/asciicast/v2/) files.

## Installation

Prefer to install using `pipx`:

```
pipx install asciicut
```

## Usage

List all casts in the current directory:

```
asciicut ls
```

```
                      Ascii Casts                       
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ File                         ┃ Duration (s) ┃ Events ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━┩
│ api2agent-chat-test.cast     │ 5.872736     │ 25     │
│ api2agent-human-manager.cast │ 8.275829     │ 22     │
└──────────────────────────────┴──────────────┴────────┘
```

Drop the first 3 seconds of a given cast

```
asciicut drop api2agent-chat-test.cast 3
```

```
                         Ascii Casts                         
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ File                              ┃ Duration (s) ┃ Events ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━┩
│ api2agent-chat-test.cast          │ 5.872736     │ 25     │
│ api2agent-chat-test_drop_3.0.cast │ 8.872736     │ 9      │
└───────────────────────────────────┴──────────────┴────────┘
```
