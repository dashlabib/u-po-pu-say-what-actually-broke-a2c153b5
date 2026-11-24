#!/usr/bin/env python3
"""Publish the one-line error message for the make.fun bounty
"Say What Actually Broke".

``entry.txt`` beside this file holds the message. This program reads
it, checks the bounty gate (a single line of UTF-8 text, 1 to 200
characters, with something in it), and writes those exact bytes to
``entry.txt`` under the output directory. A read-back comparison
guards the write: if the published file is not byte-for-byte the
entry, the program exits non-zero instead of claiming success.

The destination is ``$MAKEFUN_OUTPUT_DIR`` if set, else ``/output``.
Pass ``--output-dir <dir>`` to choose it on the command line, or
``--verify-only`` to check the message without writing anything.
Standard library only; nothing is fetched, nothing depends on the
clock, and nothing is random, so repeated runs are identical.
"""

import argparse
import os
import sys
from pathlib import Path

MAX_LENGTH = 200


def load_message() -> str:
    path = Path(__file__).resolve().parent / "entry.txt"
    return path.read_text(encoding="utf-8").strip()


def validate_message(text: str) -> None:
    if text == "":
        raise SystemExit("error message is empty")
    if len(text) > MAX_LENGTH:
        raise SystemExit(
            f"error message is {len(text)} characters; max is {MAX_LENGTH}"
        )
    if "\n" in text or "\r" in text:
        raise SystemExit("error message must be a single line")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=None,
                        help="directory to write entry.txt into")
    parser.add_argument("--verify-only", action="store_true",
                        help="validate the message without writing it")
    return parser.parse_args(argv)


def write_message(text: str, output_dir=None) -> Path:
    out_dir = Path(output_dir or os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    destination = out_dir / "entry.txt"
    destination.write_text(text, encoding="utf-8")
    if destination.read_text(encoding="utf-8") != text:
        raise SystemExit("verification failed: output differs from entry")
    return destination


def main(argv=None) -> int:
    args = parse_args(argv)
    message = load_message()
    validate_message(message)
    if args.verify_only:
        print(f"Valid: {len(message)}-character error message")
        return 0
    destination = write_message(message, args.output_dir)
    print(f"Wrote {len(message)}-character error message to {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
