from typing import List
import psycopg2
from dotenv import load_dotenv
import os
from datetime import datetime

from Entities.Member import Member
from Entities.Subject import Subject
from Services.MemberService import MemberService


class DatabaseTest:
    def __init__(self):
        load_dotenv()
        self.connection = psycopg2.connect(
            host="127.0.0.1",
            user="queue_db_admin",
            password="raBOTyaga",
            database="queue_db",
            port=5432
        )
        self.connection.autocommit = True
        with self.connection.cursor() as cur:
            cur.execute("select version();")
            print(f"server vers:  {cur.fetchone()}")

    def close(self):
        self.connection.rollback()
        self.connection.close()
        print("[INFO] Close connection with DB_TEST")
