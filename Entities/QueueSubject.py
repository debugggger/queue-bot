
class QueueMember:
    def __init__(self, id: int, subject_id: int, is_last: bool):
        self.id: int = id
        self.subject_id: int = subject_id
        self.is_last: bool = is_last
