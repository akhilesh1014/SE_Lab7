"""Property tests for valid data and predictable validation errors."""

import string

import pytest
from hypothesis import example, given, strategies as st

from library_fines import parse_member_id, shelf_code, total_fine


letters = st.text(alphabet=string.ascii_letters, min_size=1, max_size=12)
day_counts = st.lists(st.integers(0, 10000), min_size=1, max_size=20)
non_text = st.none() | st.integers() | st.booleans()


@given(letters, st.integers(0, 10**12), st.integers(0, 4))
def test_parse_valid_member_id(prefix, number, padding):
    raw = f" {prefix}-{'0' * padding}{number} "
    assert parse_member_id(raw) == (prefix.upper(), number)


@given(non_text | letters | letters.map(lambda prefix: f"{prefix}-"))
@example(None)
def test_reject_invalid_member_id(value):
    with pytest.raises(ValueError):
        parse_member_id(value)


@given(day_counts)
@example([14, 15, 30])
def test_total_fine_matches_overdue_days(days):
    raw = " , ".join(map(str, days))
    expected = sum((day - 14) * 2 for day in days if day > 14)
    assert total_fine(raw) == expected


@given(
    non_text
    | st.sampled_from(["", " ", "1,,3", "1,", "1.5", "10,two"])
    | st.integers(-10000, -1).map(lambda day: f"14,{day}")
)
@example("14,-1")
@example(None)
def test_reject_invalid_days(value):
    with pytest.raises(ValueError):
        total_fine(value)


@given(st.lists(letters, min_size=2, max_size=8), st.sampled_from([" ", "\t"]))
@example(["The", "Hobbit"], " ")
def test_shelf_code_uses_first_two_initials(words, separator):
    raw = f"  {separator.join(words)} "
    assert shelf_code(raw) == f"{words[0][0]}{words[1][0]}".upper()


@given(non_text | letters | st.sampled_from(["", " ", "\t\n"]))
@example("Dune")
@example(None)
def test_reject_invalid_title(value):
    with pytest.raises(ValueError):
        shelf_code(value)
