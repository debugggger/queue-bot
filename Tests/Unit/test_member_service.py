import pytest
from Entities.Member import Member
from Services.MemberService import MemberService

from db import Database

@pytest.fixture
def database():
    return Database()

def test_add_member(database):
    member_name = "tets"
    member_tgnum = "123456"
    MemberService.addMember(database, member_name, member_tgnum)
    assert MemberService.isMemberExistByTgNum(database, int(member_tgnum))

def test_delete_member(database):
    member_tgnum = "123456"
    MemberService.deleteMember(database, member_tgnum)
    assert not MemberService.isMemberExistByTgNum(database, int(member_tgnum))

def test_get_members_count(database):
    count = MemberService.getMembersCount(database)
    assert isinstance(count, int)

def test_get_members(database):
    members = MemberService.getMembers(database)
    assert isinstance(members, list)
    for member in members:
        assert isinstance(member, Member)

def test_get_member_by_tgnum(database):
    tgnum = 123456
    member = MemberService.getMemberByTgNum(database, tgnum)
    assert isinstance(member, Member)

def test_get_member_by_id(database):
    member_id = 1
    member = MemberService.getMemberById(database, member_id)
    assert isinstance(member, Member)

def test_is_member_exist_by_tgnum(database):
    tgnum = 123456
    assert MemberService.isMemberExistByTgNum(database, tgnum)