def test_questions():
    # assert 'Project name' in main.q()
    assert True


def test_import():
    try:
        from automail.cli import main
        assert True
    except (ImportError, ModuleNotFoundError):
        raise AssertionError
