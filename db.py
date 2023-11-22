from typing import List
import psycopg2
from dotenv import load_dotenv
import os
from datetime import datetime

from Entities.Member import Member
from Entities.Subject import Subject
from Services.MemberService import MemberService

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


    def getQueue(self, title: str) -> int:
        with self.connection.cursor() as cur:
            cur.execute("select id_queue from queuesubjects inner join subjects on queuesubjects.subject_id = "
                        "subjects.id_subject where subjects.title=%s",
                        title)

    def createQueue(self, subject_id: int) -> None:
        with self.connection.cursor() as cur:
            cur.execute("update queuesubjects set is_last = false where is_last is not null; "
                        "insert into queuesubjects (subject_id, is_last) values (%s, true) ",
                        str(subject_id))

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

    def getMemberInQueueByPlace(self, queueId, place) -> int:
        with self.connection.cursor() as cur:
            cur.execute("select member_id from queuemembers where queue_id = " + str(queueId) + " and place_number = " + str(place))
            id = cur.fetchall()[0][0]
            return id

    def getLastQueue(self) -> int:
        with self.connection.cursor() as cur:
            cur.execute("select id_queue from queuesubjects where is_last = true")
            id = cur.fetchall()[0][0]
            return id

    def getQueueIdBySubj(self, name) -> int:
        with self.connection.cursor() as cur:
            cur.execute("select id_subject from subjects where title = '" + name + "'")
            idSubj = cur.fetchall()[0][0]
            try:
                cur.execute("select id_queue from queuesubjects where subject_id = %s", (idSubj,))
                idQueue = cur.fetchall()[0][0]
            except:
                return -1
            return idQueue      

    def addToQueue(self, queue_id: int, tg_num: int, place: int, entry_type: int) -> None:
        with self.connection.cursor() as cur:
            dt = str(datetime.now())

            member = MemberService.getMemberByTgNum(self, tg_num)

            cur.execute("select count(member_id) from queuemembers where member_id=\'" + str(member.id) + "\' and queue_id=\'"+str(queue_id)+"\'")
            count = cur.fetchall()[0][0]

            if count != 0:
                cur.execute("delete from queuemembers where member_id=\'" + str(member.id) + "\' and queue_id=\'"+str(queue_id)+"\'")

            cur.execute("insert into queuemembers(queue_id, member_id, entry_time, place_number, entry_type) values(%s, %s, %s, %s, %s)",
                        (queue_id, member.id, dt, place, entry_type))

    def close(self):
        self.connection.close()
        print("[INFO] Close connection with DB")
