from set_ings import SettingsError, Property, isTrue
from set_ings import Settings as SettingsBase
import pytest
import os


def test_property_is_true():
    assert isTrue('1')
    assert isTrue('true')
    assert isTrue('True')
    assert isTrue('YES')
    assert not isTrue('0')
    assert not isTrue('false')
    assert not isTrue('foo')


def test_property_cast_value():
    assert Property().castValue('foo', 'key') == 'foo'
    assert Property(cast=int).castValue('12', 'key') == 12
    assert Property(cast=bool).castValue('1', 'key') is True
    with pytest.raises(SettingsError):
        Property(cast=int).castValue('foo', 'key')


def test_property_default():
    assert Property(default=1).fromRaw(None, 'key') == 1

    assert Property(default=lambda _: 1).fromRaw(None, 'key') == 1

    with pytest.raises(SettingsError):
        Property().fromRaw(None, 'key')


def test_property_list():
    assert Property(isList=True).fromRaw('foo,bar', 'key') == ['foo', 'bar']
    assert Property(cast=int, isList=True).fromRaw('10,11', 'key') == [10, 11]
    assert Property(isList=True).fromRaw('', 'key') == ['']


def test_property():
    assert Property().fromRaw('foo', 'key') == 'foo'
    assert Property(cast=float).fromRaw('1.2', 'key') == 1.2


def test_settings():
    class Settings(SettingsBase):
        _PREFIX = 'PRE'

        FOO = Property()
        BAR = Property(cast=int, default=10)

    os.environ['PRE_FOO'] = 'fooval'

    settings = Settings()

    assert settings.FOO == 'fooval'
    assert settings.BAR == 10
