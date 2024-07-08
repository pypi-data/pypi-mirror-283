#!/usr/bin/env python3

import contextlib
import json
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import yaml

FORMAT_FIELDS = {"time", "level", "levelname", "hostname", "pid", "aio_task", "message", "exc_info", "error"}
OUTER_KEYS = ["Line"]
EXTRAS_WIDTH: int = 100
DEFAULT_PATH = "-"


def loads_dict(value: bytes | str) -> dict[str, Any]:
    result = json.loads(value)
    if not isinstance(result, dict):
        raise ValueError("Non-dict item")
    return result


def serialize_extra(data: dict[str, Any], width: int = EXTRAS_WIDTH) -> str:
    return yaml.safe_dump(data, default_flow_style=None, sort_keys=False, width=width)


def postprocess_extra(data: str, inline_indent=" " * 4, line_indent=" " * 4) -> str:
    data = data.strip()
    if not data:
        return ""
    if "\n" not in data:
        return f"{inline_indent}{data}"
    return f"\n{line_indent}" + data.strip().replace("\n", f"\n{line_indent}")


def ensure_str(value: bytes | str) -> str:
    if isinstance(value, str):
        return value
    return bytes(value).decode("utf-8", errors="replace")


def ensure_newline(value: str) -> str:
    if value.endswith("\n"):
        return value
    return f"{value}\n"


def process_line(line: bytes | str) -> str:
    try:
        item = loads_dict(line)
    except Exception:
        return ensure_str(line)

    # For handling the systems that wrap the log lines.
    for key in OUTER_KEYS:
        inner_line = item.get(key)
        if inner_line is None:
            continue
        if isinstance(inner_line, (bytes, str)):
            try:
                item = loads_dict(inner_line)
            except Exception:
                return ensure_newline(ensure_str(inner_line))

    # TODO: full-on coloredlogs-like formatting.
    # TODO: normalize the datetime value
    pieces = [
        "\u001b[36m",
        item.get("time"),
        "\u001b[0m",
        " [",
        item.get("levelname"),
        "] ",
        item.get("message"),
    ]

    extra = {key: val for key, val in item.items() if key not in FORMAT_FIELDS}
    if extra:
        extra_s = serialize_extra(extra)
        extra_s = postprocess_extra(extra_s)
        # Might or might not add a newline.
        pieces += [extra_s]

    if item.get("exc_info"):
        pieces += ["\n", item["exc_info"]]

    if isinstance(item.get("error"), dict):
        pieces += [
            "\n",
            item["error"].get("message"),
            "\n",
            item["error"].get("stack"),
        ]

    pieces += "\n"
    return "".join(str(piece) for piece in pieces if piece)


def main_inner(log: Iterable[str]) -> None:
    for line in log:
        output = process_line(line)
        if output:
            sys.stdout.write(output)


def main() -> None:
    filepath = sys.argv[1] if len(sys.argv) > 1 else "-"
    with contextlib.ExitStack() as cm:
        if filepath == "-":
            sys.stderr.write("Reading from stdin...\n")
            fileobj = sys.stdin
        else:
            fileobj = cm.enter_context(Path(filepath).open())
        main_inner(fileobj)


if __name__ == "__main__":
    main()
