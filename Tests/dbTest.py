from typing import List
import psycopg2
from dotenv import load_dotenv
import os
from datetime import datetime

from Src.Entities.Member import Member
from Src.Entities.Subject import Subject
from Src.Services.MemberService import MemberService


class DatabaseTest:
    def __init__(self):
        load_dotenv()
        self.connection = psycopg2.connect(
            host=os.getenv('hostTest'),
            user=os.getenv('userTest'),
            password=os.getenv('passwordTest'),
            database=os.getenv('db_nameTest'),
            port=os.getenv('portTest')
        )
        # self.connection.autocommit = True
        with self.connection.cursor() as cur:
            cur.execute("select version();")
            print(f"server vers:  {cur.fetchone()}")

    def close(self):
        self.connection.rollback()
        self.connection.close()
        print("[INFO] Close connection with DB_TEST")
