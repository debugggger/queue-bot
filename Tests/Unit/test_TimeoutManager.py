import datetime
import pytest
from Src.Requests.RuntimeInfoManager import TimeoutManager


# (1) Инициализация TimeoutManager
@pytest.mark.unit
def test_timeout_manager_init():
    timeouts = {'command1': datetime.timedelta(seconds=10), 'command2': datetime.timedelta(minutes=1)}
    timeout_manager = TimeoutManager(timeouts)
    assert timeout_manager.timeouts == timeouts
    assert timeout_manager.lastUsages == {'command1': {}, 'command2': {}}


# (2) Инициализация TimeoutManager без передачи таймаутов
@pytest.mark.unit
def test_timeout_manager_init_without_timeouts():
    with pytest.raises(TypeError):
        TimeoutManager()


# (3) Получение таймаута
@pytest.mark.unit
def test_get_timeout():
    timeouts = {'command1': datetime.timedelta(seconds=10), 'command2': datetime.timedelta(minutes=1)}
    timeout_manager = TimeoutManager(timeouts)
    assert timeout_manager.getTimeout('command1') == 10
    assert timeout_manager.getTimeout('command2') == 60


# (4) Получение таймаута с неправильным ключом
@pytest.mark.unit
def test_get_timeout_with_invalid_key():
    timeouts = {'command1': datetime.timedelta(seconds=10)}
    timeout_manager = TimeoutManager(timeouts)

    with pytest.raises(KeyError):
        timeout_manager.getTimeout('invalid_command')


# (5) Получение таймаута для пустого словаря таймаутов
@pytest.mark.unit
def test_get_timeout_with_empty_timeouts():
    timeout_manager = TimeoutManager({})

    with pytest.raises(KeyError):
        timeout_manager.getTimeout('command1')


# (6) Получение таймаута с нулевым значением
@pytest.mark.unit
def test_get_timeout_with_zero_timeout():
    timeouts = {'command1': datetime.timedelta(seconds=0)}
    timeout_manager = TimeoutManager(timeouts)

    assert timeout_manager.getTimeout('command1') == 0


# (7) Проверка и обновление с внутренним ключом
@pytest.mark.unit
def test_check_and_update_with_inner_key():
    timeouts = {'command1': datetime.timedelta(seconds=10)}
    timeout_manager = TimeoutManager(timeouts)

    assert timeout_manager.checkAndUpdate('command1', 'inner_key', datetime.datetime.now())
    assert not timeout_manager.checkAndUpdate('command1', 'inner_key',
                                              datetime.datetime.now() + datetime.timedelta(seconds=5))
    assert timeout_manager.checkAndUpdate('command1', 'inner_key',
                                          datetime.datetime.now() + datetime.timedelta(seconds=15))


# (8) Проверка и обновление с внутренним ключом None
@pytest.mark.unit
def test_check_and_update_with_inner_key_none():
    timeouts = {'command1': datetime.timedelta(seconds=10)}
    timeout_manager = TimeoutManager(timeouts)

    assert timeout_manager.checkAndUpdate('command1', None, datetime.datetime.now())
    assert not timeout_manager.checkAndUpdate('command1', None, datetime.datetime.now() + datetime.timedelta(seconds=9))
    assert timeout_manager.checkAndUpdate('command1', None, datetime.datetime.now() + datetime.timedelta(seconds=11))


# (9) Проверка и обновление с неправильным ключом команды
@pytest.mark.unit
def test_check_and_update_with_invalid_command_key():
    timeouts = {'command1': datetime.timedelta(seconds=10), 'command2': datetime.timedelta(minutes=1)}
    timeout_manager = TimeoutManager(timeouts)

    with pytest.raises(KeyError):
        timeout_manager.checkAndUpdate('invalid_command', None, datetime.datetime.now())


# (10) Проверка и обновление с разными таймаутами
@pytest.mark.unit
def test_check_and_update_with_different_timeouts():
    timeouts = {'command1': datetime.timedelta(seconds=10), 'command2': datetime.timedelta(minutes=1)}
    timeout_manager = TimeoutManager(timeouts)

    assert timeout_manager.checkAndUpdate('command1', None, datetime.datetime.now())
    assert timeout_manager.checkAndUpdate('command2', None, datetime.datetime.now())
    assert not timeout_manager.checkAndUpdate('command1', None, datetime.datetime.now() + datetime.timedelta(seconds=5))
    assert not timeout_manager.checkAndUpdate('command2', None,
                                              datetime.datetime.now() + datetime.timedelta(seconds=30))


# (11) Проверка и обновление с нулевым таймаутом
@pytest.mark.unit
def test_check_and_update_with_zero_timeout():
    timeouts = {'command1': datetime.timedelta(seconds=0)}
    timeout_manager = TimeoutManager(timeouts)

    assert timeout_manager.checkAndUpdate('command1', None, datetime.datetime.now())
    assert timeout_manager.checkAndUpdate('command1', None, datetime.datetime.now() + datetime.timedelta(seconds=1))
