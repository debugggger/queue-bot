import pytest
from datetime import datetime
from Services.QueueService import QueueService
from db import Database


@pytest.fixture
def database():
    return Database()

@pytest.mark.unit
def test_is_any_queue_exist(database):
    assert not QueueService.isAnyQueueExist(database)

@pytest.mark.unit
def test_is_queue_exist(database):
    subj_id = 1
    assert not QueueService.isQueueExist(database, subj_id)

@pytest.mark.unit
def test_is_member_in_queue(database):
    queue_id = 1
    member_id = 1
    assert not QueueService.isMemberInQueue(database, queue_id, member_id)

@pytest.mark.unit
def test_is_member_in_any_queue(database):
    member_id = 1
    assert not QueueService.isMemberInAnyQueue(database, member_id)

@pytest.mark.unit
def test_get_place_by_member_id(database):
    queue_id = 1
    member_id = 1
    with pytest.raises(IndexError):
        QueueService.getPlaceByMemberId(database, queue_id, member_id)

@pytest.mark.unit
def test_get_max_place_number(database):
    queue_id = 1
    with pytest.raises(IndexError):
        QueueService.getMaxPlaceNumber(database, queue_id)

@pytest.mark.unit
def test_delete_member_from_all_queues(database):
    member_id = 1
    QueueService.deleteMemberFromAllQueues(database, member_id)

@pytest.mark.unit
def test_delete_queue_member(database):
    queue_id = 1
    member_id = 1
    QueueService.deleteQueueMember(database, queue_id, member_id)

@pytest.mark.unit
def test_create_queue(database):
    subject_id = 1
    QueueService.createQueue(database, subject_id)

@pytest.mark.unit
def test_delete_queue(database):
    id_queue = 1
    QueueService.deleteQueue(database, id_queue)

@pytest.mark.unit
def test_add_to_queue(database):
    queue_id = 1
    tg_num = 123456
    place = 1
    entry_type = 1
    with pytest.raises(IndexError):
        QueueService.addToQueue(database, queue_id, tg_num, place, entry_type)

@pytest.mark.unit
def test_set_place_by_member_id(database):
    queue_id = 1
    member_id = 1
    new_place_number = 5
    with pytest.raises(IndexError):
        QueueService.setPlaceByMemberId(database, queue_id, member_id, new_place_number)

@pytest.mark.unit
def test_get_member_in_queue_by_member_id(database):
    queue_id = 1
    member_id = 1
    with pytest.raises(IndexError):
        QueueService.getMemberInQueueByMemberId(database, queue_id, member_id)