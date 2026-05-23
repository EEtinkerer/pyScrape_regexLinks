#!/usr/bin/env python3

import argparse
import os
import re
import sys
from urllib.parse import urlparse


def convert_url_to_regex(url: str) -> str | None:
    url = url.strip()
    if not url:
        return None

    parsed = urlparse(url)

    domain = parsed.netloc if parsed.netloc else parsed.path.split("/")[0]
    path = parsed.path.strip("/") if parsed.netloc else "/".join(parsed.path.split("/")[1:])

    if not domain:
        raise ValueError("URL has no domain")

    domain_escaped = re.escape(domain)
    regex_str = rf"https?://{domain_escaped}"

    if path:
        segments = [seg for seg in path.split("/") if seg]
        regex_segments = []

        for i, seg in enumerate(segments):
            if i == len(segments) - 1 and "." in seg:
                regex_segments.append(r"[\w-]+\.\w+")
            else:
                regex_segments.append(r"[\w-]+")

        regex_str += "/" + "/".join(regex_segments)
    else:
        regex_str += r"/?"

    return rf"r'{regex_str}'"


def read_urls_from_file(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert sample URLs into generalized Python regex URL patterns."
    )

    parser.add_argument(
        "-u", "--url",
        action="append",
        default=[],
        help="URL to convert. Can be used multiple times."
    )

    parser.add_argument(
        "-i", "--input",
        action="append",
        default=[],
        help="Text file containing URLs, one per line. Can be used multiple times."
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Output file. If omitted, writes to stdout."
    )

    line_group = parser.add_mutually_exclusive_group()
    line_group.add_argument("--win", action="store_true", help="Use CRLF line endings.")
    line_group.add_argument("--unix", action="store_true", help="Use LF line endings.")

    err_group = parser.add_mutually_exclusive_group()
    err_group.add_argument("--skiponerror", action="store_true", default=True)
    err_group.add_argument("--stoponerror", action="store_true")

    args = parser.parse_args()

    if not args.url and not args.input:
        parser.error("You must provide at least one URL with -u or input file with -i.")

    urls = list(args.url)

    for file_path in args.input:
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(file_path)

            urls.extend(read_urls_from_file(file_path))

        except Exception as e:
            msg = f"Error reading input file {file_path}: {e}"
            if args.stoponerror:
                print(msg, file=sys.stderr)
                return 1
            print(f"Warning: {msg}. Skipping.", file=sys.stderr)

    output_lines = []

    for url in urls:
        try:
            pattern = convert_url_to_regex(url)
            if pattern:
                output_lines.append(pattern)

        except Exception as e:
            msg = f"Error parsing URL [{url}]: {e}"
            if args.stoponerror:
                print(msg, file=sys.stderr)
                return 1
            print(f"Warning: {msg}. Skipping.", file=sys.stderr)

    newline = "\r\n" if args.win else "\n" if args.unix else os.linesep
    output_content = newline.join(output_lines) + newline

    if args.output:
        mode = "wb" if args.win or args.unix else "w"

        try:
            if "b" in mode:
                with open(args.output, mode) as f:
                    f.write(output_content.encode("utf-8"))
            else:
                with open(args.output, mode, encoding="utf-8") as f:
                    f.write(output_content)

            print(f"[✓] Wrote patterns to {args.output}")

        except OSError as e:
            print(f"Fatal write error: {e}", file=sys.stderr)
            return 1
    else:
        sys.stdout.write(output_content)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
