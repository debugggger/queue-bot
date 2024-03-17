import datetime
from typing import List, Dict

import telebot


# Класс, позволяющий выполнять операции в несколько этапов.
# Можно отслеживать, что вторую часть команды выполнил пользователь, который выполнил и первую часть.
class SendBarrier:
    def __init__(self):
        # {'команда': [список telegram-id пользователей]}
        self.data: Dict[str, List[int]] = {}

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
        if tgId in self.data[key]:
            self.data[key].remove(tgId)
            if (len(self.data[key]) == 0):
                self.data.pop(key)

    def checkAndRemove(self, key: str, tgId: int) -> bool:
        if not self.check(key, tgId):
            return False
        self.remove(key, tgId)
        return True


class ReplaceRequest:
    def __init__(self, fromId: int, toId: int, queueId: int):
        self.fromId: int = fromId
        self.toId: int = toId
        self.queueId: int = queueId


class TimeoutManager:
    def __init__(self, timeouts: Dict[str, datetime.timedelta]):
        '''
        self.lastUsages - словарь словарей.
            Ключ первого уровня (key) - общий ключ по команде, например, имя команды ('show').
                У всех команд этого ключа одинаковый таймаут, заданный в self.timeouts.
            Ключ второго уровня - ключ в словаре, который является значением словаря первого уровня.
                Этот ключ фильтрует различные запросы в рамках одной команды. Для этих запросов значение
                таймаута одинаковое, но существует несколько запросов (у каждого из которых таймаут исчет в свое время)
                
            Например, хотим, чтобы таймаут для команды show был не один на всю команду,
                а свой для каждой очереди. В таком случае key - 'show',
                а innerKey - название очереди (предмета по которому создана очередь)

            Предлагаю использовать ключ второго уровня (innerKey) равный None,
                когда не нужно использовать ключи второго уровня. Например, делаем для команды 'show'
                общий таймаут (один на всю команду), тогда ключ второго уровня всегда равен None и во
                втором словаре всегда только одно значение - None
        '''
        self.lastUsages: Dict[str, Dict[any, datetime.datetime]] = {k: {} for k in timeouts.keys()}
        self.timeouts: Dict[str, datetime.timedelta] = timeouts

    def getTimeout(self, key: str) -> datetime.timedelta:
        return self.timeouts[key].total_seconds()

    def checkAndUpdate(self, key: str, innerKey: any, currentDatetime: datetime.datetime) -> bool:

        # Словарь последних использований только для ключа key
        lastUsages: Dict[any, datetime.datetime] = self.lastUsages[key]

        # Если внутреннего ключа innerKey нет - создаем его
        if innerKey not in lastUsages.keys():
            self.lastUsages[key][innerKey] = currentDatetime
            return True

        # Последнее использование по обоим ключам
        lastUsage: datetime.datetime = lastUsages[innerKey]

        # Проверяем таймаут и обновляем данные
        if currentDatetime - lastUsage > self.timeouts[key]:
            self.lastUsages[key][innerKey] = currentDatetime
            return True
        else:
            return False


class RuntimeInfoManager:
    def __init__(self):
        self.sendBarrier: SendBarrier = SendBarrier()
        self.timeoutManager: TimeoutManager = TimeoutManager({
            'show': datetime.timedelta(seconds=10),
            'replaceto': datetime.timedelta(seconds=180),
        })
        self.lastQueueMessages: Dict[str, telebot.types.Message] = {}
        self.replaceRequests: List[ReplaceRequest] = []

    def getAndRemoveReplaceRequest(self, memberId) -> ReplaceRequest:
        for rr in self.replaceRequests:
            if memberId == rr.fromId or memberId == rr.toId:
                rrRet = rr
                self.replaceRequests.remove(rr)
                return rrRet

    def checkReplace(self, memberId) -> bool:
        for rr in self.replaceRequests:
            if memberId == rr.fromId or memberId == rr.toId:
                return False
        return True

    def checkAndRemove(self, memberId) -> bool:
        for i in range(len(self.replaceRequests)):
            if memberId == self.replaceRequests[i].fromId or memberId == self.replaceRequests[i].toId:
                self.replaceRequests.remove(self.replaceRequests[i])
                return True
        return False

    def removeOldReplaceRequest(self) -> None:
        for rr in self.replaceRequests:
            if rr in self.timeoutManager.lastUsages['replaceto'].keys():
                lastUsage = self.timeoutManager.lastUsages['replaceto'][rr]
                if (datetime.datetime.now() - lastUsage) > self.timeoutManager.timeouts['replaceto']:
                    self.replaceRequests.remove(rr)
