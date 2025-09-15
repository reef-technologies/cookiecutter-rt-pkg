#!/usr/bin/env python
import contextlib
import os
import pathlib
import re
import subprocess

PROJECT_ROOT = pathlib.Path().resolve()
NOXFILE_PATH = PROJECT_ROOT / "noxfile.py"


def is_django_support_enabled() -> bool:
    # COOKIECUTTER{%- if cookiecutter.is_django_package == "y" %}
    return True
    # COOKIECUTTER{%- else %}
    return False  # noqa
    # COOKIECUTTER{%- endif %}


_DJANGO_ON_FILE_MARKER = re.compile(
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
            without_marker_content = _DJANGO_ON_FILE_MARKER.sub("", content)
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
        subprocess.check_call(["uv", "sync"])
        subprocess.check_call(["uv", "lock", "--upgrade"])


if __name__ == "__main__":
    main()
