import pytest
import re
from utils import checkSubjectTitle, removeBlank


# removeBlank

@pytest.mark.unit
def test_removeBlank_noBlank():
    inp = "teststring"
    assert removeBlank(inp) == inp

@pytest.mark.unit
def test_removeBlank_single_space():
    inp = "Hello World"
    assert removeBlank(inp) == inp

@pytest.mark.unit
def test_removeBlank_multipleSpaces():
    inp = "   qwerty   asdfgh   zxcvbn   "
    expected = "qwerty asdfgh zxcvbn"
    result = removeBlank(inp)
    assert result == expected

@pytest.mark.unit
def test_removeBlank_mixedSpaces():
    inp = "  qwe asd   qwerty   zxcvbn  "
    expected = "qwe asd qwerty zxcvbn"
    result = removeBlank(inp)
    assert result == expected

@pytest.mark.unit
def test_removeBlank_emptyString():
    inp = ""
    assert removeBlank(inp) == inp


# checkName

@pytest.mark.unit
def test_checkName_validTitle():
    titles = [
        "Сети и телекоммуникации",
        "Защита информации",
        "Нейронные сети",
    ]
    for title in titles:
        assert checkSubjectTitle(title)

@pytest.mark.unit
def test_checkName_titleTooLong():
    titles = [
        "A" * 31,
        "qwer ytuiop asdfghj klzxcvbnmqwerty asdzxcfghvbnjklm",
    ]
    for title in titles:
        assert not checkSubjectTitle(title)

@pytest.mark.unit
def test_checkName_invalidCharacters():
    titles = [
        "Title @ title",
        "Title 123",
        "qwerty * qwerty",
    ]
    for title in titles:
        assert not checkSubjectTitle(title)

@pytest.mark.unit
def test_checkName_withMultipleSpaces():
    assert not checkSubjectTitle('Title   with Multiple     Spaces')

@pytest.mark.unit
def test_checkName_empty():
    assert not checkSubjectTitle("")

@pytest.mark.unit
def test_checkName_blank():
    assert not checkSubjectTitle("     ")

@pytest.mark.unit
def test_checkName_withPunctuation():
    assert not checkSubjectTitle('Title, with. punctuation')

@pytest.mark.unit
def test_checkName_withNewline():
    assert not checkSubjectTitle('Title\nwithNewline')
