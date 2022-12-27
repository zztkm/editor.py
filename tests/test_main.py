def test_version():
    from src.main import __version__

    assert __version__ == "0.1.0"
