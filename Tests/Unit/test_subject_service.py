from Entities.Subject import Subject
from Services.SubjectService import SubjectService

from test_unit_common import *

@pytest.mark.unit
def test_is_subject_exist(databaseTest):
    subject_title = "newsubjj"
    assert not SubjectService.isSubjectExist(databaseTest, subject_title)
    SubjectService.addSubject(databaseTest, subject_title)
    assert SubjectService.isSubjectExist(databaseTest, subject_title)

@pytest.mark.unit
def test_get_subjects(databaseTest):
    subjects = SubjectService.getSubjects(databaseTest)
    assert isinstance(subjects, list)
    for subject in subjects:
        assert isinstance(subject, Subject)

@pytest.mark.unit
def test_get_subject_by_id(databaseTest):
    subject_id = 2
    subject = SubjectService.getSubjectById(databaseTest, subject_id)
    assert isinstance(subject, Subject)

@pytest.mark.unit
def test_get_subject_by_title(databaseTest):
    subject_title = "trkpo"
    subject = SubjectService.getSubjectByTitle(databaseTest, subject_title)
    assert isinstance(subject, Subject)

@pytest.mark.unit
def test_add_subject(databaseTest):
    subject_title = "newsubjj"
    SubjectService.addSubject(databaseTest, subject_title)
    assert SubjectService.isSubjectExist(databaseTest, subject_title)

@pytest.mark.unit
def test_remove_subject(databaseTest):
    subject_title = "newsubjj"
    SubjectService.addSubject(databaseTest, subject_title)
    SubjectService.removeSubject(databaseTest, subject_title)
    assert not SubjectService.isSubjectExist(databaseTest, subject_title)