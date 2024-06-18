def test_apiver_exports(apiver_deps):
    assert sorted(name for name in dir(apiver_deps) if not name.startswith("_")) == []
