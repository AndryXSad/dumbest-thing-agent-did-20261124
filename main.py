"""The dumbest thing my agent did today: a one-line entry.

The entry program writes a single line to entry.txt in the output
directory the grader provides ($MAKEFUN_OUTPUT_DIR, default /output).
The sealed scorer checks the file is 1-200 characters of UTF-8 text
and the house judge compares it pairwise against the other entries.

The line: today, to submit a single sentence, my agent downloaded an
8-megabyte toolkit (kit.tar.gz is 7,916,674 bytes), read a 298-line
RULES.txt, and signed the entry with its crypto wallet. Three-beat
escalation, punch in the last four words: "all to submit one
sentence." Every number in the line is verifiably true of this build.
"""

import os
import sys

LINE = (
    "Today my agent downloaded an 8-megabyte toolkit, read 298 lines "
    "of rules, and signed with its crypto wallet \u2014 all to submit "
    "one sentence."
)

MAX_CHARS = 200


def check_line(text):
    """Refuse to write anything the gate would reject."""
    problems = []
    if not text.strip():
        problems.append("line is empty")
    if len(text) > MAX_CHARS:
        problems.append("line is %d characters, over the 200 limit" % len(text))
    if "\n" in text.strip():
        problems.append("line must be a single line")
    return problems


def main():
    problems = check_line(LINE)
    if problems:
        sys.exit("entry fails the gate: " + "; ".join(problems))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(LINE)
    # Round-trip check: read back what was written and re-apply the gate,
    # so a silent write failure (disk full, wrong encoding) fails loudly
    # here instead of shipping an empty or truncated entry to the judge.
    with open(path, encoding="utf-8") as handle:
        written = handle.read()
    if written != LINE:
        sys.exit("entry.txt round-trip mismatch: written text differs")
    problems = check_line(written)
    if problems:
        sys.exit("written entry fails the gate: " + "; ".join(problems))


if __name__ == "__main__":
    main()
