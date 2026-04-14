# {{cookiecutter.package_name}}
&nbsp;[![Continuous Integration]({{cookiecutter.repository_github_url}}/workflows/Continuous%20Integration/badge.svg)]({{cookiecutter.repository_github_url}}/actions?query=workflow%3A%22Continuous+Integration%22)&nbsp;[![License](https://img.shields.io/pypi/l/{{cookiecutter.package_name}}.svg?label=License)](https://pypi.python.org/pypi/{{cookiecutter.package_name}})&nbsp;[![python versions](https://img.shields.io/pypi/pyversions/{{cookiecutter.package_name}}.svg?label=python%20versions)](https://pypi.python.org/pypi/{{cookiecutter.package_name}})&nbsp;[![PyPI version](https://img.shields.io/pypi/v/{{cookiecutter.package_name}}.svg?label=PyPI%20version)](https://pypi.python.org/pypi/{{cookiecutter.package_name}})

## Usage

> [!IMPORTANT]
> This package uses [ApiVer](#versioning), make sure to import `{{cookiecutter.package_name}}.v1`.

## Development

Pre-requisites:
- [uv](https://docs.astral.sh/uv/)
- [nox](https://nox.thea.codes/en/stable/) - may be installed as `uv tool install --with pyyaml --exclude-newer "14 days" nox`
- [docker](https://www.docker.com/) and [docker compose plugin](https://docs.docker.com/compose/)

Ideally, you should run `nox -s format lint` before every commit to ensure that the code is properly formatted and linted.
Before submitting a PR, make sure that tests pass as well, you can do so using:

```sh
nox -t check  # equivalent to `nox -s format lint test`
```

If you wish to install dependencies into `.venv` so your IDE can pick them up, you can do so using:

```sh
uv sync --all-extras --dev
```

### Python {% if cookiecutter.django_versions %} / django {% endif %} version compatibility

Use cruft questionnaire to add/remove supported versions: `cruft update --cookiecutter-input`

### Versioning

This package uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html) and [Conventional Commits](https://www.conventionalcommits.org/).

[Commitizen](https://commitizen-tools.github.io/commitizen/) may be used to generate commit messages:

```sh
uv tool install "commitizen==4.13.9"
git add ...
cz commit
```

Additionally, this package uses [ApiVer](https://www.youtube.com/watch?v=FgcoAKchPjk) to further reduce the risk of breaking changes.
This means, the public API of this package is explicitly versioned, e.g. `{{cookiecutter.package_name}}.v1`, and will not change in a backwards-incompatible way even when `{{cookiecutter.package_name}}.v2` is released.

Internal packages, i.e. prefixed by `{{cookiecutter.package_name}}._` do not share these guarantees and may change in a backwards-incompatible way at any time even in patch releases.

### Release process

Releases are prepared explicitly *by developers* with help of Commitizen. Run `cz bump` which will:
- update the changelog
- make the bump commit and tag it

Then push the commit & tag to the repository, which will trigger the release workflow:
```sh
git push origin HEAD --follow-tags
```

- `alpha`, `beta` and `rc` releases are published to TestPyPI (use `cz bump --prerelease alpha|beta|rc` to create them)
- regular ones are published to PyPI
