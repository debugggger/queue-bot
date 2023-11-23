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

    def close(self):
        self.connection.close()
        print("[INFO] Close connection with DB")
