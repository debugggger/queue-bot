import pytest
from Requests.RuntimeInfoManager import SendBarrier


# SendBarrier

@pytest.fixture
def send_barrier():
    return SendBarrier()

@pytest.mark.unit
def test_SendBarrier_add(send_barrier):
    send_barrier.add("member", 1)
    assert send_barrier.data == {"member": [1]}

    send_barrier.add("member", 2)
    assert send_barrier.data == {"member": [1, 2]}

    send_barrier.add("subject", 3)
    assert send_barrier.data == {"member": [1, 2], "subject": [3]}

@pytest.mark.unit
def test_SendBarrier_addExists(send_barrier):
    send_barrier.add("member", 1)
    assert send_barrier.data == {"member": [1]}

    send_barrier.add("member", 1)
    assert send_barrier.data == {"member": [1]}

    send_barrier.add("member", 2)
    assert send_barrier.data == {"member": [1, 2]}

    send_barrier.add("subject", 3)
    assert send_barrier.data == {"member": [1, 2], "subject": [3]}

    send_barrier.add("member", 2)
    assert send_barrier.data == {"member": [1, 2], "subject": [3]}

@pytest.mark.unit
def test_SendBarrier_addExistsAnotherCommand(send_barrier):
    send_barrier.add("member", 1)
    assert send_barrier.data == {"member": [1]}

    send_barrier.add("member", 2)
    assert send_barrier.data == {"member": [1, 2]}

    send_barrier.add("subject", 1)
    assert send_barrier.data == {"member": [2], "subject": [1]}

@pytest.mark.unit
def test_SendBarrier_check(send_barrier):
    send_barrier.add("member", 1)
    assert send_barrier.check("member", 1) == True
    assert send_barrier.check("member", 2) == False
    assert send_barrier.check("subject", 1) == False

@pytest.mark.unit
def test_SendBarrier_remove(send_barrier):
    send_barrier.add("member", 1)
    send_barrier.remove("member", 1)
    assert send_barrier.data == {}

    send_barrier.add("member", 1)
    send_barrier.add("member", 2)
    send_barrier.add("subject", 3)

    send_barrier.remove("member", 1)
    assert send_barrier.data == {"member": [2], "subject": [3]}

@pytest.mark.unit
def test_SendBarrier_removeNotExists(send_barrier):
    send_barrier.add("member", 1)
    send_barrier.remove("member", 2)
    assert send_barrier.data == {"member": [1]}
    
@pytest.mark.unit
def test_SendBarrier_checkAndRemove(send_barrier):
    send_barrier.add("member", 1)
    assert send_barrier.checkAndRemove("member", 1) == True
    assert send_barrier.data == {}

    send_barrier.add("member", 1)
    send_barrier.add("member", 2)
    assert send_barrier.checkAndRemove("member", 1) == True
    assert send_barrier.data == {"member": [2]}

@pytest.mark.unit
def test_SendBarrier_checkAndRemoveNotExists(send_barrier):
    send_barrier.add("member", 2)
    assert send_barrier.checkAndRemove("member", 1) == False
    assert send_barrier.data == {"member": [2]}
