import pytest
import re
from datetime import datetime
from utils import checkSubjectTitle, removeBlank, formQueueText, checkNumPlace
from Entities.Member import Member
from Entities.Queue import Queue, QueueMember
from Entities.Subject import Subject


# removeBlank

@pytest.mark.unit
def test_removeBlank_noBlank():
    inp = "teststring"
    assert removeBlank(inp) == inp

@pytest.mark.unit
def test_removeBlank_single_space():
    inp = "Hello World"
    assert removeBlank(inp) == inp

@pytest.mark.unit
def test_removeBlank_multipleSpaces():
    inp = "   qwerty   asdfgh   zxcvbn   "
    expected = "qwerty asdfgh zxcvbn"
    result = removeBlank(inp)
    assert result == expected

@pytest.mark.unit
def test_removeBlank_mixedSpaces():
    inp = "  qwe asd   qwerty   zxcvbn  "
    expected = "qwe asd qwerty zxcvbn"
    result = removeBlank(inp)
    assert result == expected

@pytest.mark.unit
def test_removeBlank_emptyString():
    inp = ""
    assert removeBlank(inp) == inp


# checkName

@pytest.mark.unit
def test_checkName_validTitle():
    titles = [
        "Сети и телекоммуникации",
        "Защита информации",
        "Нейронные сети",
    ]
    for title in titles:
        assert checkSubjectTitle(title)

@pytest.mark.unit
def test_checkName_titleTooLong():
    titles = [
        "A" * 31,
        "qwer ytuiop asdfghj klzxcvbnmqwerty asdzxcfghvbnjklm",
    ]
    for title in titles:
        assert not checkSubjectTitle(title)

@pytest.mark.unit
def test_checkName_invalidCharacters():
    titles = [
        "Title @ title",
        "Title 123",
        "qwerty * qwerty",
    ]
    for title in titles:
        assert not checkSubjectTitle(title)

@pytest.mark.unit
def test_checkName_withMultipleSpaces():
    assert not checkSubjectTitle('Title   with Multiple     Spaces')

@pytest.mark.unit
def test_checkName_empty():
    assert not checkSubjectTitle("")

@pytest.mark.unit
def test_checkName_blank():
    assert not checkSubjectTitle("     ")

@pytest.mark.unit
def test_checkName_withPunctuation():
    assert not checkSubjectTitle('Title, with. punctuation')

@pytest.mark.unit
def test_checkName_withNewline():
    assert not checkSubjectTitle('Title\nwithNewline')


# formQueueText

# (1) Формирование текста для пустой очереди
@pytest.mark.unit
def test_form_queue_text_empty():
    queue = Queue(id=1, subject=Subject(id=1, title="trkpo"), isLast=True, members=[])
    assert formQueueText(queue) == "Очередь по trkpo:\n"


# (2) Формирование текста для очереди с одним участником
@pytest.mark.unit
def test_form_queue_text_single_member():
    member = Member(id=1, name="chel", tgNum=123)
    queue_member = QueueMember(member=member, entryTime=datetime.now(), placeNumber=1, entryType="Type")
    queue = Queue(id=1, subject=Subject(id=1, title="trkpo"), isLast=True, members=[queue_member])
    assert formQueueText(queue) == "Очередь по trkpo:\n1 - chel\n"


# (3) Формирование текста для очереди с несколькими участниками
@pytest.mark.unit
def test_form_queue_text_multiple_members():
    member1 = Member(id=1, name="chel", tgNum=123)
    member2 = Member(id=2, name="chel2", tgNum=456)
    member3 = Member(id=3, name="chel3", tgNum=789)
    queue_members = [
        QueueMember(member=member1, entryTime=datetime.now(), placeNumber=3, entryType="Type"),
        QueueMember(member=member2, entryTime=datetime.now(), placeNumber=1, entryType="Type"),
        QueueMember(member=member3, entryTime=datetime.now(), placeNumber=2, entryType="Type")
    ]
    queue = Queue(id=1, subject=Subject(id=1, title="trkpo"), isLast=True, members=queue_members)
    assert formQueueText(queue) == "Очередь по trkpo:\n1 - chel2\n2 - chel3\n3 - chel\n"


# (4) Формирование текста для очереди с несколькими участниками на местах не подряд
@pytest.mark.unit
def test_form_queue_text_multiple_members_not_a_row():
    member1 = Member(id=1, name="chel", tgNum=123)
    member2 = Member(id=2, name="chel2", tgNum=456)
    member3 = Member(id=3, name="chel3", tgNum=789)
    queue_members = [
        QueueMember(member=member1, entryTime=datetime.now(), placeNumber=1, entryType="Type"),
        QueueMember(member=member2, entryTime=datetime.now(), placeNumber=3, entryType="Type"),
        QueueMember(member=member3, entryTime=datetime.now(), placeNumber=12, entryType="Type")
    ]
    queue = Queue(id=1, subject=Subject(id=1, title="trkpo"), isLast=True, members=queue_members)
    assert formQueueText(queue) == "Очередь по trkpo:\n1 - chel\n3 - chel2\n12 - chel3\n"


# (5) Формирование текста для очереди с участниками без мест
@pytest.mark.unit
def test_form_queue_text_empty_spots():
    member1 = Member(id=1, name="chel", tgNum=123)
    member3 = Member(id=3, name="chel2", tgNum=789)
    queue_members = [
        QueueMember(member=member1, entryTime=datetime.now(), placeNumber=1, entryType="Type")
    ]
    queue = Queue(id=1, subject=Subject(id=1, title="trkpo"), isLast=True, members=queue_members)
    assert formQueueText(queue) == "Очередь по trkpo:\n1 - chel\n"


# (6) Формирование текста для очереди с разными предметами
@pytest.mark.unit
def test_form_queue_text_different_subjects():
    member1 = Member(id=1, name="chel", tgNum=123)
    member2 = Member(id=2, name="chel2", tgNum=456)
    member3 = Member(id=3, name="chel3", tgNum=789)
    queue1 = Queue(id=1, subject=Subject(id=1, title="trkpo"), isLast=True, members=[QueueMember(member=member1, entryTime=datetime.now(), placeNumber=1, entryType="Type")])
    queue2 = Queue(id=2, subject=Subject(id=2, title="opkppim"), isLast=True, members=[QueueMember(member=member2, entryTime=datetime.now(), placeNumber=1, entryType="Type")])
    queue3 = Queue(id=3, subject=Subject(id=3, title="pdpu"), isLast=True, members=[QueueMember(member=member3, entryTime=datetime.now(), placeNumber=1, entryType="Type")])
    assert formQueueText(queue1) == "Очередь по trkpo:\n1 - chel\n"
    assert formQueueText(queue2) == "Очередь по opkppim:\n1 - chel2\n"
    assert formQueueText(queue3) == "Очередь по pdpu:\n1 - chel3\n"


# (7) Формирование текста для очереди с большим количеством участников
@pytest.mark.unit
def test_form_queue_text_many_members():
    members = [Member(id=i, name=f"Member {i}", tgNum=i) for i in range(1, 101)]
    queue_members = [QueueMember(member=member, entryTime=datetime.now(), placeNumber=i, entryType="Type") for i, member in enumerate(members, start=1)]
    queue = Queue(id=1, subject=Subject(id=1, title="trkpo"), isLast=True, members=queue_members)
    expected_text = "Очередь по trkpo:\n" + "\n".join([f"{i} - Member {i}" for i in range(1, 101)]) + "\n"
    assert formQueueText(queue) == expected_text


# (8) Формирование текста для очереди с длинным именем предмета
@pytest.mark.unit
def test_form_queue_text_long_subject_name():
    subject_title = "qwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjklzxcvbnm"
    queue = Queue(id=1, subject=Subject(id=1, title=subject_title), isLast=True, members=[])
    assert formQueueText(queue) == "Очередь по qwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjklzxcvbnm:\n"


# (9) Формирование текста для очереди с дублирующимися местами
@pytest.mark.unit
def test_form_queue_text_duplicate_spots():
    member1 = Member(id=1, name="chel", tgNum=123)
    member2 = Member(id=2, name="chel2", tgNum=456)
    member3 = Member(id=3, name="chel3", tgNum=789)
    queue_members = [
        QueueMember(member=member1, entryTime=datetime.now(), placeNumber=1, entryType="Type"),
        QueueMember(member=member2, entryTime=datetime.now(), placeNumber=1, entryType="Type"),
        QueueMember(member=member3, entryTime=datetime.now(), placeNumber=3, entryType="Type")
    ]
    queue = Queue(id=1, subject=Subject(id=1, title="trkpo"), isLast=True, members=queue_members)
    assert not formQueueText(queue) == "Очередь по trkpo:\n1 - chel\n1 - chel2\n3 - chel3\n"


# (10) Формирование текста для очереди с разными типами входа
@pytest.mark.unit
def test_form_queue_text_different_entry_types():
    member1 = Member(id=1, name="chel", tgNum=123)
    member2 = Member(id=2, name="chel2", tgNum=456)
    queue_members = [
        QueueMember(member=member1, entryTime=datetime.now(), placeNumber=1, entryType="Type1"),
        QueueMember(member=member2, entryTime=datetime.now(), placeNumber=21, entryType="Type2")
    ]
    queue = Queue(id=1, subject=Subject(id=1, title="trkpo"), isLast=True, members=queue_members)
    assert formQueueText(queue) == "Очередь по trkpo:\n1 - chel\n21 - chel2\n"


# (11) Формирование текста для очереди с разными временами входа у участников
@pytest.mark.unit
def test_form_queue_text_different_entry_times():
    member1 = Member(id=1, name="chel", tgNum=123)
    member2 = Member(id=2, name="chel2", tgNum=456)
    queue_members = [
        QueueMember(member=member1, entryTime=datetime(2024, 2, 5, 10, 30), placeNumber=1, entryType="Type"),
        QueueMember(member=member2, entryTime=datetime(2024, 2, 5, 10, 35), placeNumber=2, entryType="Type")
    ]
    queue = Queue(id=1, subject=Subject(id=1, title="trkpo"), isLast=True, members=queue_members)
    assert formQueueText(queue) == "Очередь по trkpo:\n1 - chel\n2 - chel2\n"


# (12) Формирование текста для очереди с разными временами входа, типом входа у участников
@pytest.mark.unit
def test_form_queue_text_different_entry_times_types():
    member1 = Member(id=1, name="chel", tgNum=123)
    member2 = Member(id=2, name="chel2", tgNum=456)
    queue_members = [
        QueueMember(member=member1, entryTime=datetime(2023, 2, 5, 10, 30), placeNumber=1, entryType="Type"),
        QueueMember(member=member2, entryTime=datetime.now(), placeNumber=2, entryType="Type2")
    ]
    queue = Queue(id=1, subject=Subject(id=1, title="trkpo"), isLast=True, members=queue_members)
    assert formQueueText(queue) == "Очередь по trkpo:\n1 - chel\n2 - chel2\n"


# (13) Формирование текста для очереди с пустым предметом
@pytest.mark.unit
def test_form_queue_text_empty_subject():
    member = Member(id=1, name="chel", tgNum=123)
    queue = Queue(id=1, subject=Subject(id=1, title=""), isLast=True, members=[QueueMember(member=member, entryTime=datetime.now(), placeNumber=1, entryType="Type")])
    assert formQueueText(queue) == "Очередь по :\n1 - chel\n"

@pytest.mark.unit
def test_check_place():
    assert checkNumPlace("1wefahsfsdhn") == -1
    assert checkNumPlace("-4") == -1
    assert checkNumPlace("1") == -1
