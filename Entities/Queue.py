from datetime import datetime
from typing import List

class QueueMember:
    def __init__(self, memberId: int = 0, entryTime: datetime = '', placeNumber: int=0, entryType: str=''):
        self.memberId: int = memberId
        self.entryTime: datetime = entryTime
        self.placeNumber: int = placeNumber
        self.entryType: str = entryType

class Queue:
    
    def __init__(self, id: int = 0, subjectId: int = 0, isLast: bool = False):
        self.id : int = id
        self.subjectId: int = subjectId
        self.isLast: bool = isLast
        self.members: List[QueueMember] = []