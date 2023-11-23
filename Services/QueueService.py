from datetime import datetime
from typing import List

from Entities import Member
from Entities.Queue import QueueMember, Queue
from Services.MemberService import MemberService


class QueueService:

    @staticmethod
    def isQueueExist(database, subjId: int) -> bool:
        with database.connection.cursor() as cur:
            cur.execute("select count(id_queue) from queuesubjects where subject_id=%s", (subjId,))
            count = cur.fetchall()[0][0]
        return count != 0

    @staticmethod
    def isMemberInQueue(database, queueId: int, memberId: int) -> bool:
        with database.connection.cursor() as cur:
            cur.execute("select count(queue_id) from queuemembers where queue_id=%s and member_id=%s", (queueId, memberId))
            count = cur.fetchall()[0][0]
        return count != 0

    @staticmethod
    def deleteQueueMember(database, queueId: int, memberId: int) -> None:
        with database.connection.cursor() as cur:
            cur.execute("delete from queuemembers where queue_id=%s and member_id=%s",
                        (queueId, memberId))

    @staticmethod
    def createQueue(database, subject_id: int) -> None:
        with database.connection.cursor() as cur:
            cur.execute("update queuesubjects set is_last = false where is_last is not null; "
                        "insert into queuesubjects (subject_id, is_last) values (%s, true) ",
                        (subject_id,))

    @staticmethod
    def deleteQueue(database, id_queue: int) -> None:
        with database.connection.cursor() as cur:
            cur.execute("delete from queuesubjects where id_queue=%s", (id_queue,))

    @staticmethod
    def getMembersInQueue(database, queueId: int) -> List[QueueMember]:
        queueMembers : List[QueueMember] = []
        with database.connection.cursor() as cur:
            cur.execute("select * from queuemembers where queue_id=%s", (queueId,))
            for r in cur.fetchall():
                queueMembers.append(QueueMember(*r[1:]))
        return queueMembers

    @staticmethod
    def getMemberInQueueByPlace(database, queueId, place) -> QueueMember:
        queueMember : QueueMember = QueueMember()
        with database.connection.cursor() as cur:
            cur.execute("select * from queuemembers where queue_id = " + str(queueId) + " and place_number = " + str(place))
            result = cur.fetchall()[0]
            queueMember.memberId = result[1]
            queueMember.entryTime = result[2]
            queueMember.placeNumber = result[3]
            queueMember.entryType = result[4]

        return queueMember

    @staticmethod
    def isPlaceEmpty(database, num, queueId) -> bool:
        with database.connection.cursor() as cur:
            count = cur.execute("select count(member_id) from queuemembers "
                                "where queue_id = " + str(queueId) + " and place_number = " + str(num))
            res = cur.fetchall()
            for row in res:
                count = row[0]

        return count == 0

    @staticmethod
    def getQueueBySubjectId(database, subjectId: int) -> Queue:
        queue : Queue = Queue()
        with database.connection.cursor() as cur:
            cur.execute("select * from queuesubjects where subject_id=%s", (subjectId,))
            result = cur.fetchall()[0]
            queue.id = result[0]
            queue.subjectId = result[1]
            queue.isLast = result[2]
        queue.members = QueueService.getMembersInQueue(database, queue.id)

        return queue

    @staticmethod
    def getQueues(database) -> List[Queue]:
        queues : List[Queue] = []
        with database.connection.cursor() as cur:
            cur.execute("select * from queuesubjects")
            for r in cur.fetchall():
                queues.append(Queue(*r))

        for q in queues:
            q.members = QueueService.getMembersInQueue(database, q.id)

        return queues

    # TODO когда очередей вообще нет - эксепшн
    @staticmethod
    def getLastQueue(database) -> Queue:
        queue: Queue = Queue()
        with database.connection.cursor() as cur:
            cur.execute("select * from queuesubjects where is_last=true")
            result = cur.fetchall()[0]
            queue.id = result[0]
            queue.subjectId = result[1]
            queue.isLast = result[2]
        queue.members = QueueService.getMembersInQueue(database, queue.id)

        return queue

    @staticmethod
    def addToQueue(database, queue_id: int, tg_num: int, place: int, entry_type: int) -> None:
        with database.connection.cursor() as cur:
            dt = str(datetime.now())

            member = MemberService.getMemberByTgNum(database, tg_num)

            cur.execute("select count(member_id) from queuemembers where member_id=\'" + str(member.id) + "\' and queue_id=\'"+str(queue_id)+"\'")
            count = cur.fetchall()[0][0]

            if count != 0:
                cur.execute("delete from queuemembers where member_id=\'" + str(member.id) + "\' and queue_id=\'"+str(queue_id)+"\'")

            cur.execute("insert into queuemembers(queue_id, member_id, entry_time, place_number, entry_type) values(%s, %s, %s, %s, %s)",
                        (queue_id, member.id, dt, place, entry_type))
