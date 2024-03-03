import pytest
import re
from Src.utils import checkMemberName

@pytest.mark.unit
def test_valid_member_name():
    valid_names = [
        "Ayudhbdn",
        "Агнвапрг",
        "Ашоао-втаои ва",
        "АРгщивор'sdbfjsdb"
    ]
    for name in valid_names:
        assert checkMemberName(name)

@pytest.mark.unit
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

