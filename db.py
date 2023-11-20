from typing import List
import psycopg2
from dotenv import load_dotenv
import os
from datetime import datetime

from Entities.Member import Member
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
                        title)

    def createQueue(self, subject_id: int) -> None:
        with self.connection.cursor() as cur:
            cur.execute("update queuesubjects set is_last = false where true; "
                        "commit;" 
                        "insert into queuesubjects (subject_id, is_last) values (%s, true) ",
                        subject_id)

    def deleteQueue(self, id_queue: int) -> None:
        with self.connection.cursor() as cur:
            cur.execute("delete from queuesubjects where id_queue=%s",
                        (str(id_queue)))

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

    def getMembers(self) -> List[Member]:
        with self.connection.cursor() as cur:
            cur.execute("select * from members")
            return list(map(lambda m: Member(m[0], m[1], m[2]), cur.fetchall()))

    def getMemberByTgNum(self, tgNum: int) -> Member:
        with self.connection.cursor() as cur:
            cur.execute("select * from members where tg_num=%s", (str(tgNum),))
            result = cur.fetchall()[0]
            return Member(result[0], result[1], result[2])


    def addToQueue(self, queue_id: int, tg_num: int, place: int, entry_type: int) -> None:
        with self.connection.cursor() as cur:
            dt = str(datetime.now())

            member = self.getMemberByTgNum(tg_num)

            cur.execute("select count(member_id) from queuemembers where member_id=\'" + str(member.id) + "\'")
            count = cur.fetchall()[0][0]

            if count != 0:
                cur.execute("delete from queuemembers where member_id=\'" + str(member.id) + "\'")

            cur.execute("insert into queuemembers(queue_id, member_id, entry_time, place_number, entry_type) values(%s, %s, %s, %s, %s)",
                        (queue_id, member.id, dt, place, entry_type))

    def close(self):
        self.connection.close()
        print("[INFO] Close connection with DB")
