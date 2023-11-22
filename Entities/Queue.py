from datetime import datetime
from typing import List

class QueueMember:
    def __init__(self, memberId: int, entryTime: datetime, placeNumber: int, entryType: str):
        self.memberId: int = memberId
        self.entryTime: datetime = entryTime
        self.placeNumber: int = placeNumber
        self.entryType: str = entryType

class Queue:
    def __init__(self):
        self.id : int = 0
        self.subjectId: int = 0
        self.isLast: bool = False
        self.members: List[QueueMember] = []
    
    def __init__(self, id: int, subjectId: int, isLast: bool):
        self.id : int = id
        self.subjectId: int = subjectId
        self.isLast: bool = isLast
        self.members: List[QueueMember] = []