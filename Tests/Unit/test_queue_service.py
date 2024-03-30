import pytest
from datetime import datetime
from Services.QueueService import QueueService
from Entities.Queue import *
from dbTest import DatabaseTest

from test_unit_common import *

@pytest.mark.unit
def test_is_any_queue_exist(databaseTest):
    assert QueueService.isAnyQueueExist(databaseTest)

@pytest.mark.unit
def test_is_queue_exist(databaseTest):
    subj_id = 1
    assert QueueService.isQueueExist(databaseTest, subj_id)

@pytest.mark.unit
def test_is_member_in_queue(databaseTest):
    queue_id = 1
    member_id = 1
    assert QueueService.isMemberInQueue(databaseTest, queue_id, member_id)
    queue_id = 2
    member_id = 2
    assert not QueueService.isMemberInQueue(databaseTest, queue_id, member_id)

@pytest.mark.unit
def test_is_member_in_any_queue(databaseTest):
    member_id = 1
    assert QueueService.isMemberInAnyQueue(databaseTest, member_id)

@pytest.mark.unit
def test_get_place_by_member_id(databaseTest):
    queue_id = 1
    member_id = 1
    assert QueueService.getPlaceByMemberId(databaseTest, queue_id, member_id) == 1

@pytest.mark.unit
def test_get_max_place_number(databaseTest):
    queue_id = 1
    assert QueueService.getMaxPlaceNumber(databaseTest, queue_id) == 3

@pytest.mark.unit
def test_delete_member_from_all_queues(databaseTest):
    member_id = 1
    QueueService.deleteMemberFromAllQueues(databaseTest, member_id)
    assert not QueueService.isMemberInAnyQueue(databaseTest, member_id)

@pytest.mark.unit
def test_delete_queue_member(databaseTest):
    queue_id = 1
    member_id = 1
    QueueService.deleteQueueMember(databaseTest, queue_id, member_id)
    assert not QueueService.isMemberInQueue(databaseTest, queue_id, member_id)

@pytest.mark.unit
def test_create_queue(databaseTest):
    subject_id = 2
    QueueService.deleteQueue(databaseTest, 2)
    QueueService.createQueue(databaseTest, subject_id)
    assert QueueService.isQueueExist(databaseTest, subject_id)

@pytest.mark.unit
def test_delete_queue(databaseTest):
    id_queue = 1
    QueueService.deleteQueue(databaseTest, id_queue)
    assert not QueueService.isQueueExist(databaseTest, 1)

# @pytest.mark.unit
# def test_get_members_in_queue(databaseTest):

@pytest.mark.unit
def test_get_count_members_in_queue(databaseTest):
    id_queue = 1
    assert QueueService.getCountMembersInQueue(databaseTest, id_queue) == 3

@pytest.mark.unit
def test_get_members_in_queue_by_place(databaseTest):
    id_queue = 1
    place = 1
    queueMember = QueueService.getMemberInQueueByPlace(databaseTest, id_queue, place)
    assert isinstance(queueMember, QueueMember)

@pytest.mark.unit
def test_is_place_empty(databaseTest):
    id_queue = 1
    place = 1
    member_id = 3
    assert QueueService.isPlaceEmpty(databaseTest, place, id_queue, member_id) == 0

@pytest.mark.unit
def test_get_queue_by_subject_id(databaseTest):
    subject_id = 1
    queue = QueueService.getQueueBySubjectId(databaseTest, subject_id)
    assert isinstance(queue, Queue)

@pytest.mark.unit
def test_get_queue_by_id(databaseTest):
    id_queue = 3
    queue = QueueService.getQueueById(databaseTest, id_queue)
    assert isinstance(queue, Queue)

# @pytest.mark.unit
# def test_get_queues(databaseTest):

@pytest.mark.unit
def test_last_queue(databaseTest):
    id_queue = 3
    queue = QueueService.getLastQueue(databaseTest)
    assert isinstance(queue, Queue)

@pytest.mark.unit
def test_add_to_queue(databaseTest):
    queue_id = 3
    tg_num = "123456"
    place = 1
    entry_type = 0
    QueueService.addToQueue(databaseTest, queue_id, tg_num, place, entry_type)
    assert QueueService.isMemberInQueue(databaseTest, queue_id, 1)

@pytest.mark.unit
def test_set_place_by_member_id(databaseTest):
    queue_id = 2
    member_id = 1
    new_place_number = 1
    QueueService.setPlaceByMemberId(databaseTest, queue_id, member_id, new_place_number)
    assert QueueService.getPlaceByMemberId(databaseTest, queue_id, member_id) == 1

@pytest.mark.unit
def test_get_member_in_queue_by_member_id(databaseTest):
    queue_id = 1
    member_id = 1
    queueMember = QueueService.getMemberInQueueByMemberId(databaseTest, queue_id, member_id)
    assert isinstance(queueMember, QueueMember)
