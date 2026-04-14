#!/usr/bin/env python
import pathlib
import subprocess

PROJECT_ROOT = pathlib.Path().resolve()


def main():
    subprocess.check_call(["uv", "sync"], cwd=PROJECT_ROOT)


if __name__ == "__main__":
    main()
