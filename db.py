import psycopg2
from dotenv import load_dotenv
import os

# TODO: add other queries and functions for this

class BotDB:

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

    def add_member(self, member_name, member_tgnum):
        with self.connection.cursor() as cur:
            cur.execute("INSERT INTO MEMBERS (\"Name\", \"TgNum\") VALUES (%s, %s) "
                        "ON CONFLICT (\"TgNum\") DO UPDATE SET \"Name\" = EXCLUDED.\"Name\"",
                        (member_name, member_tgnum))

    def getMembersCount(self):
        with self.connection.cursor() as cur:
            cur.execute("select count(\"IdMember\") from members")
            res = cur.fetchall()
            for row in res:
                count = row[0]
        return count

    def checkPlace(self, num, queueId):
        with self.connection.cursor() as cur:
            count = cur.execute("select count(\"MemberId\") from QueueMembers "
                                "where \"QueueId\" = " + str(queueId) + " and \"PlaceNumber\" = " + str(num))
            res = cur.fetchall()
            for row in res:
                count = row[0]

        if count == 0:
            return 1
        else:
            return 0


    def close(self):
        self.connection.close()
        print("[INFO] Close connection with DB")
