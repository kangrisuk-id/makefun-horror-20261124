#!/usr/bin/env python3
"""Two-Sentence Horror - make.fun entry.

Writes one horror story of exactly two sentences to entry.txt in the
first writable output directory. Pure Python standard library only:
the grading sandbox has no third-party packages.
"""

import os
import sys

STORY = (
    "The radiologist said the shadow on my scan was probably nothing, "
    "just an artifact of the machine. Then she asked, very quietly, "
    "why the artifact in every scan since childhood has been slowly "
    "turning its head toward the camera."
)


def check_story(text):
    """Hold the story to the gate before anything is written.

    The sealed scorer accepts UTF-8 text of 1 to 400 characters that is
    not only whitespace, and the brief demands exactly two sentences.
    A story that fails either test must never reach the output file.
    """
    if not text or not text.strip():
        return False
    if not 1 <= len(text) <= 400:
        return False
    sentences = [part for part in text.replace("! ", ". ").replace("? ", ". ").split(". ") if part.strip()]
    return len(sentences) == 2


def candidate_dirs():
    """Output directories to try, in order, without repeats."""
    dirs = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        dirs.append(env_dir)
    dirs.append("/output")
    dirs.append(os.path.dirname(os.path.abspath(__file__)))
    dirs.append("/tmp")
    seen = set()
    unique = []
    for directory in dirs:
        if directory not in seen:
            seen.add(directory)
            unique.append(directory)
    return unique


def write_story(directory):
    """Write entry.txt in one directory, atomically, or raise OSError."""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, "entry.txt")
    tmp_path = os.path.join(directory, ".entry.txt.tmp")
    with open(tmp_path, "w", encoding="utf-8") as handle:
        handle.write(STORY + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp_path, path)
    return path


def main():
    if not check_story(STORY):
        print("error: the story fails the gate (length or sentence count)", file=sys.stderr)
        return 1
    for directory in candidate_dirs():
        try:
            write_story(directory)
            return 0
        except OSError:
            continue
    print("error: no writable output directory", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
