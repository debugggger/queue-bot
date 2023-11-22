from typing import List

from Entities.Queue import QueueMember, Queue

class QueueService:

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
        queue.members = database.getMembersInQueue(queue.id)

        return queue

    @staticmethod
    def getQueues(database) -> List[Queue]:
        queues : List[Queue] = []
        with database.connection.cursor() as cur:
            cur.execute("select * from queuesubjects")
            for r in cur.fetchall():
                queues.append(Queue(*r))

        for q in queues:
            q.members = database.getMembersInQueue(q.id)

        return queues
