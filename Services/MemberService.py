from typing import List

from Entities.Member import Member

class MemberService:

    @staticmethod
    def addMember(database, member_name: str, member_tgnum: str) -> None:
        with database.connection.cursor() as cur:
            cur.execute("insert into members (name, tg_num) values (%s, %s) "
                        "on conflict (tg_num) do update set name = excluded.name",
                        (member_name, member_tgnum))

    @staticmethod
    def deleteMember(database, member_tgnum: str) -> None:
        with database.connection.cursor() as cur:
            cur.execute("delete from members where tg_num=%s",
                        (member_tgnum,))

    @staticmethod
    def getMembersCount(database) -> int:
        with database.connection.cursor() as cur:
            cur.execute("select count(id_member) from members")
            res = cur.fetchall()
            for row in res:
                count = row[0]
        return count

    @staticmethod
    def getMembers(database) -> List[Member]:
        with database.connection.cursor() as cur:
            cur.execute("select * from members")
            return list(map(lambda m: Member(*m), cur.fetchall()))

    @staticmethod
    def getMemberByTgNum(database, tgNum: int) -> Member:
        with database.connection.cursor() as cur:
            cur.execute("select * from members where tg_num=%s", (str(tgNum),))
            result = cur.fetchall()[0]
            return Member(*result)

    @staticmethod
    def getMemberById(database, id: int) -> Member:
        with database.connection.cursor() as cur:
            cur.execute("select * from members where id_member=%s", (str(id),))
            result = cur.fetchall()[0]
            return Member(*result)


    def isMemberExistByTgNum(database, tgNum: int) -> bool:
        with database.connection.cursor() as cur:
            cur.execute("select count(id_member) from members where tg_num=%s", (str(tgNum),))
            count = cur.fetchall()[0][0]
        return count != 0
