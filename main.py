#!/usr/bin/env python3
"""make.fun entry: world news of Friday 20 November 2026, one image.

Deterministic, stdlib only: copies the pre-rendered entry.png held in this
repository to /output/entry.png. No network, no clock, no randomness.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    with open(dst, "wb") as f:
        f.write(data)
    print("wrote /output/entry.png (%d bytes)" % len(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
