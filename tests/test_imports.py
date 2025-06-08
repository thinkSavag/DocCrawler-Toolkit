import importlib

def test_import_package():
    assert importlib.import_module('visio_handbook') is not None


def test_cli_help():
    mod = importlib.import_module('visio_handbook.cli')
    try:
        mod.main(['--help'])
    except SystemExit as e:
        assert e.code == 0
