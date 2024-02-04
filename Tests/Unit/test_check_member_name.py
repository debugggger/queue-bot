import pytest
import re
from utils import checkMemberName

def test_valid_member_name():
    valid_names = [
        "Ayudhbdn",
        "Агнвапрг",
        "Ашоао-втаоива",
        "АРгщивор'sdbfjsdb"
    ]
    for name in valid_names:
        assert checkMemberName(name)

def test_invalid_member_name():
    invalid_names = [
        "1234",
        "",
        "   ",
        "АРгщивор'sdbfjsdbshdufgduihsdidhcgesnjbchjbnxznbchjbjkzbbcvhjsncbhjshhchsbsncbhjbdjah",
        "tet%",
        "sdhfj)"
    ]
    for name in invalid_names:
        assert not checkMemberName(name)

