from datetime import datetime


class QueueMember:
    def __init__(self, queue_id: int, member_id: int, entry_time: datetime, place_number: int, entry_type: str):
        self.queue_id: int = queue_id
        self.member_id: int = member_id
        self.entry_time: datetime = entry_time
        self.place_number: int = place_number
        self.entry_type: str = entry_type
