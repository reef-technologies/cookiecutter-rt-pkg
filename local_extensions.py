from cookiecutter.utils import simple_filter


def parse_version(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.strip().split("."))


@simple_filter
def sort_versions(versions: list[str]) -> list[str]:
    return sorted(versions, key=parse_version)
