from typing import List, Dict


# Класс, позволяющий выполнять операции в несколько этапов.
# Можно отслеживать, что вторую часть команды выполнил пользователь, который выполнил и первую часть.
class SendBarrier:
    def __init__(self):
        # {'команда': [список telegram-id пользователей]}
        self.data : Dict[str, List[int]] = {}

    def add(self, key: str, tgId: int) -> None:
        for item in self.data.values():
            if tgId in item:
                item.remove(tgId)
        if key in self.data:
            self.data[key].append(tgId)
        else:
            self.data[key] = [tgId]

    def check(self, key: str, tgId: int) -> bool:
        if key not in self.data:
            return False
        return tgId in self.data[key]

    def remove(self, key: str, tgId: int) -> None:
        self.data[key].remove(tgId)

    def checkAndRemove(self, key: str, tgId: int) -> bool:
        if not self.check(key, tgId):
            return False
        self.remove(key, tgId)
        return True

class RuntimeInfoManager:
    def __init__(self):
        self.sendBarrier : SendBarrier = SendBarrier()
        # тут добавим переменные для таймаутов и всего остального, что не будет храниться в БД
