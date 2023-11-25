from datetime import datetime
from typing import List

from Entities import Member
from Entities.Queue import QueueMember, Queue
from Services.MemberService import MemberService
from Services.SubjectService import SubjectService


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
    def deleteMemberFromAllQueues(database, memberId: int) -> None:
        with database.connection.cursor() as cur:
            cur.execute("delete from queuemembers where member_id=%s",
                        (memberId,))

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
                member = MemberService.getMemberById(database, r[1])
                queueMembers.append(QueueMember(member, *r[2:]))
        return queueMembers

    @staticmethod
    def getMemberInQueueByPlace(database, queueId, place) -> QueueMember:
        with database.connection.cursor() as cur:
            cur.execute("select * from queuemembers where queue_id = " + str(queueId) + " and place_number = " + str(place))
            result = cur.fetchall()[0]
            member = MemberService.getMemberById(database, result[1])
            return  QueueMember(member, *result[2:])

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
        with database.connection.cursor() as cur:
            cur.execute("select * from queuesubjects where subject_id=%s", (subjectId,))
            result = cur.fetchall()[0]
            return Queue(result[0],
                         SubjectService.getSubjectById(database, result[1]),
                         result[2],
                         QueueService.getMembersInQueue(database, result[0]))

    @staticmethod
    def getQueueById(database, id: int) -> Queue:
        with database.connection.cursor() as cur:
            cur.execute("select * from queuesubjects where id_queue=%s", (id,))
            result = cur.fetchall()[0]
            return Queue(result[0],
                         SubjectService.getSubjectById(database, result[1]),
                         result[2],
                         QueueService.getMembersInQueue(database, result[0]))

    @staticmethod
    def getQueues(database) -> List[Queue]:
        queues : List[Queue] = []
        with database.connection.cursor() as cur:
            cur.execute("select * from queuesubjects")
            for r in cur.fetchall():
                queues.append(Queue(r[0],
                         SubjectService.getSubjectById(database, r[1]),
                         r[2],
                         QueueService.getMembersInQueue(database, r[0])))

        for q in queues:
            q.members = QueueService.getMembersInQueue(database, q.id)

        return queues

    @staticmethod
    def getLastQueue(database) -> Queue:
        with database.connection.cursor() as cur:
            cur.execute("select * from queuesubjects where is_last=true")
            result = cur.fetchall()[0]
            return Queue(result[0],
                         SubjectService.getSubjectById(database, result[1]),
                         result[2],
                         QueueService.getMembersInQueue(database, result[0]))

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
