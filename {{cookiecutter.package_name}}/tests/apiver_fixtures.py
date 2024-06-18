from __future__ import annotations

import importlib.util
import itertools
import re
from pathlib import Path

import pytest


def pytest_addoption(parser):
    group = parser.getgroup("apiver", "Test API versions.")
    group.addoption(
        "--target-package-name",
        action="store",
        dest="target_package_name",
        help="The name of the package to test API versions of.",
    )
    parser.addini(
        "target_package_name",
        help="The name of the package to test API versions of.",
        default=None,
    )


def get_package_name(config) -> str:
    package_name = config.getoption("target_package_name") or config.getini("target_package_name")
    assert package_name, "The --target-package-name CLI option or target_package_name INI option is required."
    return package_name


def get_api_versions(package_name: str) -> list[int]:
    versions = set()

    package_spec = importlib.util.find_spec(package_name)
    if not package_spec:
        raise ValueError(f"Package {package_name=!r} not found. Possibly `--target-package-name` is incorrect.")
    assert package_spec.origin
    package_path = Path(package_spec.origin).parent

    for apiver_package_path in itertools.chain(
        package_path.glob("v*/__init__.py"),
        package_path.glob("v*.py"),
    ):
        match = re.search(r"/_?v(\d+)(:?\.py|/__init__\.py)$", str(apiver_package_path))
        if match:
            versions.add(int(match.group(1)))
    assert versions, f"No API versions found in {package_path!r}"
    return sorted(versions)


def pytest_generate_tests(metafunc):
    if "apiver" in metafunc.fixturenames:
        versions = metafunc.config.cache.get("apivers", None)
        if versions is None:
            package_name = get_package_name(metafunc.config)
            versions = get_api_versions(package_name)
            metafunc.config.cache.set("apivers", versions)
        markers = [mark for mark in metafunc.definition.iter_markers(name="apiver")]
        if markers:
            applicable_versions = set()
            for marker in markers:
                for version in marker.args:
                    if isinstance(version, tuple):
                        applicable_versions.update(range(version[0], version[1] + 1))
                    elif isinstance(version, int):
                        applicable_versions.add(version)
                for key, value in marker.kwargs.items():
                    if key == "from_ver":
                        applicable_versions.update(range(value, max(versions) + 1))
                    elif key == "to_ver":
                        applicable_versions.update(range(min(versions), value + 1))
            applicable_versions = sorted(applicable_versions & set(versions))
        else:
            applicable_versions = versions
        metafunc.parametrize("apiver", [f"v{ver}" for ver in applicable_versions])


@pytest.fixture(scope="session")
def apiver_tested_package_name(request):
    return get_package_name(request.config)


@pytest.fixture
def apiver_int(apiver):
    """Get apiver as an int, e.g., 2."""
    return int(apiver[1:])


@pytest.fixture
def apiver_import(apiver, apiver_tested_package_name):
    def importer(module_name: str | None = None):
        module_name = (
            f"{apiver_tested_package_name}.{apiver}.{module_name}"
            if module_name
            else f"{apiver_tested_package_name}.{apiver}"
        )
        return importlib.import_module(module_name)

    return importer


@pytest.fixture
def apiver_deps(apiver_import):
    return apiver_import()
