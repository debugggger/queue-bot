
class Subject():
    def __init__(self, id: int = 0, title: str = ''):
        self.id: int = id
        self.title: str = title

    def __repr__(self):
        return f'Subject(id={self.id}, title={self.title})'
