#!/usr/bin/env python
import contextlib
import importlib.util
import os
import pathlib
import re
import subprocess

PROJECT_ROOT = pathlib.Path().resolve()
NOXFILE_PATH = PROJECT_ROOT / "noxfile.py"


def is_django_support_enabled():
    """
    Check if DJANGO SUPPORT is enabled.
    """
    # Since .cruft.json is not available at this point, we need to check from noxfile.py.
    spec = importlib.util.spec_from_file_location("noxfile", NOXFILE_PATH)
    noxfile = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(noxfile)

    return hasattr(noxfile, "DJANGO_VERSIONS")


_DJANGO_ONL_FILE_MARKER = re.compile(
    r"^# cookiecutter-rt-pkg macro: requires cookiecutter.is_django_package$",
    re.MULTILINE,
)


def get_django_specific_files():
    """
    Find all files with `# cookiecutter-rt-pkg macro: requires cookiecutter.is_django_package` line.
    """
    for file_path in PROJECT_ROOT.rglob("*.py"):
        with file_path.open() as f:
            try:
                content = f.read()
            except UnicodeDecodeError:
                continue
            without_marker_content = _DJANGO_ONL_FILE_MARKER.sub("", content)
            if content != without_marker_content:
                yield file_path, content


@contextlib.contextmanager
def working_directory(path):
    """Changes working directory and returns to previous on exit."""
    prev_cwd = pathlib.Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def main():
    django_support = is_django_support_enabled()
    print(f"{django_support=!r}")
    for filepath, new_content in get_django_specific_files():
        if django_support:
            with filepath.open("w") as f:
                f.write(new_content)
        else:
            print(f"Removing django specific {filepath}")
            filepath.unlink()

    with working_directory(PROJECT_ROOT):
        subprocess.check_call(["pdm", "lock", "--update-reuse"])


if __name__ == "__main__":
    main()
