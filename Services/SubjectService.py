from typing import List

from Entities.Subject import Subject

class SubjectService:

    @staticmethod
    def isSubjectExist(database, title: str) -> bool:
        with database.connection.cursor() as cur:
            cur.execute("select count(id_subject) from subjects where title=%s", (title, ))
            count = cur.fetchall()[0][0]
            return count != 0

    @staticmethod
    def getSubjects(self) -> List[Subject]:
        with self.connection.cursor() as cur:
            cur.execute("select * from subjects")
            return list(map(lambda s: Subject(*s), cur.fetchall()))

    @staticmethod
    def addSubject(database, title: str) -> None:
        with database.connection.cursor() as cur:
            cur.execute("insert into subjects(title) values(%s)",
                        (title, ))

    @staticmethod
    def removeSubject(database, title: str) -> None:
        with database.connection.cursor() as cur:
            cur.execute("delete from subjects where title=%s",
                        (title, ))

