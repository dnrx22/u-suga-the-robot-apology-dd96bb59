#!/usr/bin/env python3
"""The Robot Apology: a robot apologizes for one small, exact mistake.

Writes exactly two lines to entry.txt in the output directory
(MAKEFUN_OUTPUT_DIR, or /output when that is unset). Line 1 is the
apology for watering a plastic plant; line 2 is the lesson it learned
and what it will do differently. Deterministic, stdlib only, no
network, no reads outside this repo.
"""

import hashlib
import os
import sys

MAX_CHARS = 200

LINES = (
    "I'm sorry — I watered the plastic ficus every morning for three "
    "weeks, then filed a maintenance report about its refusal to grow.",
    "I learned that a plant that never wilts is not thriving, so from "
    "now on I will read the care tag before I water anything.",
)


def validate(lines) -> None:
    """Enforce the competition rules for the two lines."""
    if len(lines) != 2:
        raise ValueError(f"expected exactly 2 lines, got {len(lines)}")
    if lines[0] == lines[1]:
        raise ValueError("the two lines must be different")
    for i, line in enumerate(lines, start=1):
        if not line:
            raise ValueError(f"line {i} is empty")
        if line != line.strip():
            raise ValueError(
                f"line {i} must not have leading or trailing whitespace"
            )
        if "\n" in line or "\r" in line:
            raise ValueError(
                f"line {i} must be a single line (no newline characters)"
            )
        if line.count(".") != 1 or not line.endswith("."):
            raise ValueError(
                f"line {i} must be exactly one sentence ending with a period"
            )
        if len(line) > MAX_CHARS:
            raise ValueError(
                f"line {i} is {len(line)} characters, "
                f"over the {MAX_CHARS} limit"
            )


def main() -> int:
    validate(LINES)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = ("\n".join(LINES) + "\n").encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    # Round-trip check: what landed on disk must be exactly the lines.
    with open(path, "rb") as fh:
        if fh.read() != data:
            raise RuntimeError("written entry.txt does not match the lines")
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {len(data)} bytes to {path}")
    for i, line in enumerate(LINES, start=1):
        print(f"line {i} characters: {len(line)}")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
