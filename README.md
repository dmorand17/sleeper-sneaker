# Sleeper Sneeker

Sleeper API docs: https://docs.sleeper.com/

## Prerequisites

- Python3

## Getting Started

## Usage

Help info

```
Usage: main.py [OPTIONS]

Options:
  -l, --league TEXT   League ID to query
  -u, --user TEXT     User names/ids to query
  -y, --year INTEGER  Year to query, defaults to current year
  -v, --verbose       Print debug messages
  --help              Show this message and exit.
```

Query by league id

```bash
python3 sleeper_sneaker/main.py --league <league_id>
```

Query by username or user_id

```bash
python3 sleeper_sneaker/main.py --user <username>
```

## Development

Create and launch virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```
