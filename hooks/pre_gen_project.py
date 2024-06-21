#!/usr/bin/env python
import os
import pathlib
import re

PROJECT_ROOT = pathlib.Path().resolve()
NOXFILE_PATH = PROJECT_ROOT / "noxfile.py"

PACKAGE_NAME = "{{ cookiecutter.package_name }}"
REPOSITORY_URL = "{{ cookiecutter.repository_github_url }}"

EXIT_ON_VALIDATION_ERROR = os.getenv("ERROR_ON_VALIDATION", "1") == "1"


def error_on_validation():
    if EXIT_ON_VALIDATION_ERROR:
        print("Exiting due to validation error. Set ERROR_ON_VALIDATION=0 env var to disable this behavior.")
        exit(1)


def validate_package_name():
    if not re.match(r"^[a-z][a-z0-9_]*$", PACKAGE_NAME):
        print(
            f"ERROR: {PACKAGE_NAME!r} is not a valid Python package name! "
            f"Please use a valid snake_case name and try again."
        )
        error_on_validation()
    expected_repository_name = PACKAGE_NAME.replace("_", "-")
    repository_name = REPOSITORY_URL.split("/")[-1]
    if repository_name != expected_repository_name:
        print(
            f"ERROR: Repository name {repository_name!r} does not match expected name {expected_repository_name!r}. "
            "Please correct the 'repository_github_url' value and try again."
        )
        error_on_validation()


def main():
    validate_package_name()


if __name__ == "__main__":
    main()
