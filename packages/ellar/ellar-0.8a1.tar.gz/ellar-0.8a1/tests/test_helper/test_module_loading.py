import pytest
from ellar.core import conf
from ellar.utils.module_loading import module_dir


def test_module_dir():
    module_path = module_dir(conf)
    assert "ellar/core/conf" in module_path


def test_invalid_module_check():
    with pytest.raises(ValueError):
        module_dir({})
