import pytest
from Requests.RuntimeInfoManager import RuntimeInfoManager, ReplaceRequest
import datetime

@pytest.fixture
def runtime_info_manager():
    return RuntimeInfoManager()

@pytest.mark.unit
def test_get_and_remove_replace_request(runtime_info_manager):
    rr1 = ReplaceRequest("id1", "id2", 1)
    runtime_info_manager.replaceRequests.append(rr1)
    assert runtime_info_manager.getAndRemoveReplaceRequest("id1") == rr1
    assert len(runtime_info_manager.replaceRequests) == 0

@pytest.mark.unit
def test_check_replace(runtime_info_manager):
    rr1 = ReplaceRequest("id1", "id2", 1)
    runtime_info_manager.replaceRequests.append(rr1)
    assert not runtime_info_manager.checkReplace("id1")

@pytest.mark.unit
def test_check_and_remove(runtime_info_manager):
    rr1 = ReplaceRequest("id1", "id2", 1)
    runtime_info_manager.replaceRequests.append(rr1)
    assert runtime_info_manager.checkAndRemove("id1")
    assert len(runtime_info_manager.replaceRequests) == 0

@pytest.mark.unit
def test_remove_old_replace_request(runtime_info_manager):
    rr1 = ReplaceRequest("id1", "id2", 1)
    runtime_info_manager.replaceRequests.append(rr1)
    runtime_info_manager.timeoutManager.lastUsages['replaceto'][rr1] = datetime.datetime.now() - datetime.timedelta(seconds=200)
    runtime_info_manager.removeOldReplaceRequest()
    assert len(runtime_info_manager.replaceRequests) == 0

@pytest.mark.unit
def test_invalid_get_and_remove_replace_request(runtime_info_manager):
    rr1 = ReplaceRequest("id1", "id2", 1)
    runtime_info_manager.replaceRequests.append(rr1)
    assert runtime_info_manager.getAndRemoveReplaceRequest("id3") == None

@pytest.mark.unit
def test_invalid_check_replace(runtime_info_manager):
    rr1 = ReplaceRequest("id1", "id2", 1)
    runtime_info_manager.replaceRequests.append(rr1)
    assert runtime_info_manager.checkReplace("id3")

@pytest.mark.unit
def test_invalid_check_and_remove(runtime_info_manager):
    rr1 = ReplaceRequest("id1", "id2", 1)
    runtime_info_manager.replaceRequests.append(rr1)
    assert not runtime_info_manager.checkAndRemove("id3")

@pytest.mark.unit
def test_invalid_remove_old_replace_request(runtime_info_manager):
    rr1 = ReplaceRequest("id1", "id2", 1)
    runtime_info_manager.replaceRequests.append(rr1)
    runtime_info_manager.timeoutManager.lastUsages['replaceto'][rr1] = datetime.datetime.now() - datetime.timedelta(seconds=100)
    runtime_info_manager.removeOldReplaceRequest()
    assert len(runtime_info_manager.replaceRequests) == 1