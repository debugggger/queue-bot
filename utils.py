import re

def removeBlank(string: str) -> str:
    return ' '.join(string.split())

def checkSubjectTitle(title: str) -> bool:
    return bool(re.fullmatch('([A-Za-zА-Яа-яёЁ]+ ?)+', title)) and (len(title) <= 30)

def checkMemberName(name: str) -> bool:
    return bool(re.fullmatch('([A-Za-zА-Яа-яёЁ]+[ \-\']?)+', name)) and (len(name) <= 30)
