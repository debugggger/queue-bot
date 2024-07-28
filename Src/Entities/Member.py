
class Member:
    def __init__(self, id: int, name: str, tgNum: int):
        self.id: int = id
        self.name: str = name
        self.tgNum: int = tgNum

    def __repr__(self):
        return f"Member(id={self.id}, name={self.name}, tgNum={self.tgNum})"
