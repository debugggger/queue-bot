from typing import List
import psycopg2
from dotenv import load_dotenv
import os

from Entities.Subject import Subject

# TODO: add other queries and functions for this

class Database:
    def __init__(self):
        load_dotenv()
        self.connection = psycopg2.connect(
            host=os.getenv('host'),
            user=os.getenv('user'),
            password=os.getenv('password'),
            database=os.getenv('db_name'),
            port=os.getenv('port')
        )
        self.connection.autocommit = True
        with self.connection.cursor() as cur:
            cur.execute("select version();")
            print(f"server vers:  {cur.fetchone()}")

    def addMember(self, member_name: str, member_tgnum: str) -> None:
        with self.connection.cursor() as cur:
            cur.execute("insert into members (name, tg_num) values (%s, %s) "
                        "on conflict (tg_num) do update set name = excluded.name",
                        (member_name, member_tgnum))

    def deleteMember(self, member_tgnum: str) -> None:
        with self.connection.cursor() as cur:
            cur.execute("delete from members where tg_num=%s",
                        (member_tgnum))

    def getMembersCount(self) -> int:
        with self.connection.cursor() as cur:
            cur.execute("select count(id_member) from members")
            res = cur.fetchall()
            for row in res:
                count = row[0]
        return count

    def getQueue(self, title: str) -> int:
        with self.connection.cursor() as cur:
            cur.execute("select id_queue from queuesubjects inner join subjects on queuesubjects.subject_id = "
                        "subjects.id_subject where subjects.title=%s",
                        (title))

    def createQueue(self, subject_id: int) -> None:
        with self.connection.cursor() as cur:
            cur.execute("update queuesubjects set is_last = false;"
                        "insert into queuesubjects (subject_id, is_last) values (%i, 1) ",
                        (subject_id))

    def deleteQueue(self, id_queue: int) -> None:
        with self.connection.cursor() as cur:
            cur.execute("delete from queuesubjects where id_queue=%i",
                        (id_queue))

    def checkPlace(self, num, queueId):
        with self.connection.cursor() as cur:
            count = cur.execute("select count(member_id) from queuemembers "
                                "where queue_id = " + str(queueId) + " and place_number = " + str(num))
            res = cur.fetchall()
            for row in res:
                count = row[0]

        if count == 0:
            return 1
        else:
            return 0

    def getSubjects(self) -> List[Subject]:
        with self.connection.cursor() as cur:
            cur.execute("select * from subjects")
            return list(map(lambda s: Subject(s[0], s[1]), cur.fetchall()))

    def isSubjectExist(self, title: str) -> bool:
        with self.connection.cursor() as cur:
            cur.execute("select count(id_subject) from subjects where title=%s", (title, ))
            count = cur.fetchall()[0][0]
            return count != 0
            
    def addSubject(self, title: str) -> None:
        with self.connection.cursor() as cur:
            cur.execute("insert into subjects(title) values(%s)",
                        (title, ))

    def removeSubject(self, title: str) -> None:
        with self.connection.cursor() as cur:
            cur.execute("delete from subjects where title=%s",
                        (title, ))

    def close(self):
        self.connection.close()
        print("[INFO] Close connection with DB")
