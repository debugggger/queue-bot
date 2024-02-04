import pytest
from Entities.Subject import Subject
from Services.SubjectService import SubjectService
from db import Database


@pytest.fixture
def database():
    return Database()

def test_is_subject_exist(database):
    subject_title = "тркпо"
    assert not SubjectService.isSubjectExist(database, subject_title)
    SubjectService.addSubject(database, subject_title)
    assert SubjectService.isSubjectExist(database, subject_title)

def test_get_subjects(database):
    subjects = SubjectService.getSubjects(database)
    assert isinstance(subjects, list)
    for subject in subjects:
        assert isinstance(subject, Subject)

def test_get_subject_by_id(database):
    subject_id = 8
    subject = SubjectService.getSubjectById(database, subject_id)
    assert isinstance(subject, Subject)

def test_get_subject_by_title(database):
    subject_title = "тркпо"
    subject = SubjectService.getSubjectByTitle(database, subject_title)
    assert isinstance(subject, Subject)

def test_add_subject(database):
    subject_title = "опркимаргшшваир"
    SubjectService.addSubject(database, subject_title)
    assert SubjectService.isSubjectExist(database, subject_title)

def test_remove_subject(database):
    subject_title = "опркимаргшшваир"
    # SubjectService.addSubject(database, subject_title)
    # assert SubjectService.isSubjectExist(database, subject_title)
    SubjectService.removeSubject(database, subject_title)
    assert not SubjectService.isSubjectExist(database, subject_title)