
from pathlib import Path

from ..src.toml_config import TomlConfig
from ..src.constants import STATUS_OK

CONFIG_ATTRS = {
    'month': [int],
    'payment_bbo': [int, float],
    'period_months': [int],
}
ANSI_COLOR_RED = "\x1b[31m"
ANSI_COLOR_RESET = "\x1b[0m"
ANSI_COLOR_RED = ""
ANSI_COLOR_RESET = ""


def test_config_structure():
    path = Path('tests', 'test_data', 'config.toml')
    config = TomlConfig(path)
    assert isinstance(config.config, dict)
    assert len(config.config) == 3


def test_config_missing(capsys):
    path = Path('tests', 'test_data', 'not_a_file.toml')
    err_msg = f'The config file is not in the expected location: {path}'
    TomlConfig(path)
    captured = capsys.readouterr()
    assert captured.out.strip() == f'{ANSI_COLOR_RED}{err_msg}{ANSI_COLOR_RESET}'


def test_config_invalid_attrs(capsys):
    path = Path('tests', 'test_data', 'config_invalid_attrs.toml')
    err_msg = "Corrupt config file. month not of type [<class 'int'>]"
    TomlConfig(path, CONFIG_ATTRS)
    captured = capsys.readouterr()
    assert captured.out.strip() == f'{ANSI_COLOR_RED}{err_msg}{ANSI_COLOR_RESET}'


def test_config_invalid_json(capsys):
    path = Path('tests', 'test_data', 'config_invalid_toml.toml')
    err_msg = f"Invalid toml format in {path}"
    TomlConfig(path)
    captured = capsys.readouterr()
    assert captured.out.strip() == f'{ANSI_COLOR_RED}{err_msg}{ANSI_COLOR_RESET}'


def test_config_missing_attr(capsys):
    path = Path('tests', 'test_data', 'config_missing_attr.toml')
    err_msg = "Corrupt config file. Missing attribute: payment_bbo"
    TomlConfig(path, CONFIG_ATTRS)
    captured = capsys.readouterr()
    assert captured.out.strip() == f'{ANSI_COLOR_RED}{err_msg}{ANSI_COLOR_RESET}'


def test_config_save_status():
    path = Path('tests', 'test_data', 'config.toml')
    config = TomlConfig(path)
    saved = config.save()
    assert saved == STATUS_OK


def test_config_save_invalid_path():
    path = Path('tests', 'test_data', 'config.toml')
    err_msg = "Could not save"
    config = TomlConfig(path)
    config.path = Path('tests', 'test_data_not_a_directory', 'not_a_file.toml')
    saved = config.save()
    err_msg = f"[Errno 2] No such file or directory: '{str(config.path)}'"
    assert str(saved) == err_msg
