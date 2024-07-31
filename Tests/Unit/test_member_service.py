import pytest
from Entities.Member import Member
from Services.MemberService import MemberService

from DbUtils.db import Database

from test_unit_common import *

@pytest.mark.unit
def test_add_member(databaseTest):
    member_name = "testMem"
    member_tgnum = "123456"
    MemberService.addMember(databaseTest, member_name, member_tgnum)
    assert MemberService.isMemberExistByTgNum(databaseTest, int(member_tgnum))

@pytest.mark.unit
def test_delete_member(databaseTest):
    member_name = "testMem"
    member_tgnum = "123456"
    MemberService.addMember(databaseTest, member_name, member_tgnum)
    MemberService.deleteMember(databaseTest, member_tgnum)
    assert not MemberService.isMemberExistByTgNum(databaseTest, int(member_tgnum))

@pytest.mark.unit
def test_get_members_count(databaseTest):
    count = MemberService.getMembersCount(databaseTest)
    assert isinstance(count, int)
    assert count == 3

@pytest.mark.unit
def test_get_members(databaseTest):
    members = MemberService.getMembers(databaseTest)
    assert isinstance(members, list)
    for member in members:
        assert isinstance(member, Member)

@pytest.mark.unit
def test_get_member_by_tgnum(databaseTest):
    tgnum = "123456"
    member = MemberService.getMemberByTgNum(databaseTest, tgnum)
    assert isinstance(member, Member)

@pytest.mark.unit
def test_get_member_by_id(databaseTest):
    member_id = 1
    member = MemberService.getMemberById(databaseTest, member_id)
    assert isinstance(member, Member)

@pytest.mark.unit
def test_is_member_exist_by_tgnum(databaseTest):
    tgnum = "123456"
    tgnum2 = "123"
    assert MemberService.isMemberExistByTgNum(databaseTest, tgnum)
    assert not MemberService.isMemberExistByTgNum(databaseTest, tgnum2)
