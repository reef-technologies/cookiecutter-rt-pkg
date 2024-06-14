def test_v0_exports():
    import {{cookiecutter.package_name}}.v0 as api  # noqa

    assert sorted(name for name in dir(api) if not name.startswith("_")) == []
