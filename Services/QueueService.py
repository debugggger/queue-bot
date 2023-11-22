from typing import List

from Entities.Queue import QueueMember, Queue

class QueueService:

    @staticmethod
    def isQueueExist(database, subjId: int) -> bool:
        with database.connection.cursor() as cur:
            cur.execute("select count(id_queue) from queuesubjects where id_queue=%s", (subjId,))
            count = cur.fetchall()[0][0]
            return count != 0

    @staticmethod
    def getMembersInQueue(database, queueId: int) -> List[QueueMember]:
        queueMembers : List[QueueMember] = []
        with database.connection.cursor() as cur:
            cur.execute("select * from queuemembers where queue_id=%s", (queueId,))
            for r in cur.fetchall():
                queueMembers.append(QueueMember(*r[1:]))
        return queueMembers

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
