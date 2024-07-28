from Entities.Subject import *
from Entities.Queue import *

s = Subject(1, 'subjj')
m1 = Member(1, 'memeber', 123)
m2 = Member(2, 'memeberrrrrr', 1234)
queue: Queue = Queue(1, s, True, [QueueMember(m1, 0, 3, ''), QueueMember(m2, 0, 2, '')])

print(len(list(filter(lambda m: m.member.tgNum == 123 and m.placeNumber == 3, queue.members))))


