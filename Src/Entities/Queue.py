from datetime import datetime
from typing import List

from Entities.Member import Member
from Entities.Subject import Subject

class QueueMember:
    def __init__(self, member: Member, entryTime: datetime, placeNumber: int, entryType: str):
        self.member: Member = member
        self.entryTime: datetime = entryTime
        self.placeNumber: int = placeNumber
        self.entryType: str = entryType

    def __repr__(self):
        return f'QueueMember(member={self.member}, placeNumber={self.placeNumber})'

class Queue:
    def __init__(self, id: int, subject: Subject, isLast: bool, members: List[QueueMember]):
        self.id : int = id
        self.subject: Subject = subject
        self.isLast: bool = isLast
        self.members: List[QueueMember] = members

    def __repr__(self):
        return f'Queue(id={self.id}, subject={self.subject}, isLast={self.isLast}, members={self.members})'