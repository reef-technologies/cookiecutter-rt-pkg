# cookiecutter-rt-pkg

Opinionated cookiecutter for Python packages.

# Features

Packages created from this template get following features:

- CI with GitHub Actions
- Trusted Publishing to PyPI with GitHub Actions
- Signed release files using sigstore
- Pre-configured nox for testing (pytest), autoformatting and auto linting (ruff)
- Testing against multiple Python versions, operating systems, and optionally, Django versions
- Testing utils for testing ApiVer interfaces
- Package layout and release process with SemVer & ApiVer in mind
- Towncrier for conflict free changelogs

## Template features

- CI for cookiecutter template itself

## Planned features

- [ ] CD should require CI tests to pass first
- [ ] excluding some django-python combos in nox test matrix (allow to test of Django5+Python3.12 and Django4+Python3.9 but not Django5+Python3.9)
- [ ] Contributing guidelines
- [ ] PR templates
- [ ] ability to build binary & python version-specific wheels

## Usage

[cruft](https://github.com/cruft/cruft) is used to manage the template, you can install it with:

```sh
pip install cruft
```

### To generate a new package:

1. Setup empty repository on GitHub
2. Run:

```sh
cruft create https://github.com/reef-technologies/cookiecutter-rt-pkg
```

3. Configure Trusted Publishers to allow GitHub Actions to publish to PyPI, follow instructions in [{{cookiecutter.package\_name}}/.github/workflows/publish.yml](.github/workflows/publish.yml)

### When you wish to update your project to the latest version of the template:

```sh
cruft update
```

Before committing make sure to review changes listed in [docs/3rd\_party/cookiecutter-rt-pkg/CHANGELOG.md](docs/3rd_party/cookiecutter-rt-pkg/CHANGELOG.md).

### Linking an existing repository

If you have an existing repo, you can link it to the template by running:

```sh
cruft link https://github.com/reef-technologies/cookiecutter-rt-pkg
```

# Contributing

When proposing new features or changes, make sure to consider the context of the application template [cookiecutter-rt-django](https://github.com/reef-technologies/cookiecutter-rt-django) as well.
It is important we do not try to solve the same problem in two different ways.

## License

This project is licensed under the terms of the [BSD-3 License](/LICENSE)

## Changelog

Breaking changes are documented in the [CHANGELOG]({{cookiecutter.package_name}}/docs/3rd_party/cookiecutter-rt-pkg/CHANGELOG.md)
