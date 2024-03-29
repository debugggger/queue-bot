import pytest

import time
import os

import telebot
from telebot import types
from pyrogram import Client
from dotenv import load_dotenv

from Services.MemberService import MemberService
from Services.SubjectService import SubjectService
from Services.QueueService import QueueService
from Src.Entities import Queue

from test_common import *
from utils import formReplaceRequest


# 12
@pytest.mark.system
def test_create_cancel(client):
    checkResponce(client, '/create', 'По какому предмету ты хочешь создать очередь?')
    checkResponce(client, '❌ Отмена', 'Команда отменена')

# 13
@pytest.mark.system
def test_create_correct(client):
    sendAndWaitAny(client, '/subject')
    sendAndWaitAny(client, 'subject for create')

    subject = SubjectService.getSubjectByTitle('subject for create')

    assert not QueueService.isQueueExist(subject.id)

    checkResponce(client, '/create', 'По какому предмету ты хочешь создать очередь?')
    checkResponce(client, 'subject for create', 'Создана очередь по subject for create')

    assert QueueService.isQueueExist(databaseTest, subject.id)

# 14
@pytest.mark.system
def test_join_last(client, client2, databaseTest):
    createMember(client)
    createMember(client2)
    create_test_queue(client)

    count = MemberService.getMembersCount(databaseTest)

    checkResponce(client, '/join', 'Выбрана очередь по subjj:\nВыбери место для записи')
    expected = f'Ты записан на {count} место'
    id1 = checkResponce(client, 'Последнее свободное', expected)

    checkResponce(client2, '/join', 'Выбрана очередь по subjj:\nВыбери место для записи')
    expected = f'Ты записан на {count - 1} место'
    id2 = checkResponce(client2, 'Последнее свободное', expected)

    # TODO не работает
    queue: Queue = QueueService.getQueueBySubjectTitle(databaseTest, 'subjj')
    assert 1 == queue.members[0].member.tgNum
    assert len(list(filter(lambda m: m.member.tgNum == id1 and m.placeNumber == count, queue.members))) == 1
    assert len(list(filter(lambda m: m.member.tgNum == id2 and m.placeNumber == count-1, queue.members))) == 1


# 15
@pytest.mark.system
def test_join_first(client, client2, databaseTest):
    create_test_queue(client)

    checkResponce(client, '/join', 'Выбрана очередь по subjj:\nВыбери место для записи')
    checkResponce(client, 'Первое свободное', 'Ты записан на 1 место')

    checkResponce(client2, '/join', 'Выбрана очередь по subjj:\nВыбери место для записи')
    checkResponce(client2, 'Первое свободное', 'Ты записан на 2 место')

    delete_test_subj(client)

# 16
@pytest.mark.system
def test_join_num(client, client2):
    create_test_queue(client)

    checkResponce(client, '/join', 'Выбрана очередь по subjj:\nВыбери место для записи')
    checkResponce(client, 'Определенное', 'Введи место для записи')
    checkResponce(client, '2', 'Ты записан на 2 место')

    checkResponce(client2, '/join', 'Выбрана очередь по subjj:\nВыбери место для записи')
    checkResponce(client2, 'Определенное', 'Введи место для записи')
    checkResponce(client2, '2', 'Желаемое место уже занято или превышает количество человек, которые живут очередями. Ты записан на 3 место')

    delete_test_subj(client)


# 17 (возможно не работает)
@pytest.mark.system
def test_confirm(client, client2):
    create_test_queue(client)

    sendAndWaitAny(client, '/join')
    sendAndWaitAny(client, 'Определенное')
    msg1: types.Message = sendAndWaitAny(client, '1')

    sendAndWaitAny(client2, '/join')
    sendAndWaitAny(client2, 'Определенное')
    msg2: types.Message = sendAndWaitAny(client2, '2')

    replaceRequestText = formReplaceRequest(msg1.from_user.username, msg2.from_user.username, 'subjj', 1, 2)
    checkResponce(client2, '/replace', 'Выбрана очередь по subjj:\nВведи место с которым хочешь поменяться')
    checkResponce(client2, '1', replaceRequestText)

    checkResponce(client, '/confirm', 'Смена мест произошла успешно!')

    delete_test_subj(client)
