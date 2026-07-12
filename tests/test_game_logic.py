import pytest
from logic_utils import (
    get_range_for_difficulty,
    check_guess,
    update_score,
    parse_guess
)

# ============================================
# Tests for get_range_for_difficulty
# ============================================

def test_get_range_for_difficulty_easy():
    """Test Easy mode returns correct range 1-20"""
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_get_range_for_difficulty_normal():
    """Test Normal mode returns correct range 1-100"""
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100

def test_get_range_for_difficulty_hard():
    """Test Hard mode returns correct range 1-50"""
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 50

# ============================================
# Tests for check_guess
# ============================================

def test_check_guess_too_high():
    """Test that guessing above secret returns 'Too High'"""
    outcome, message = check_guess(75, 50)
    assert outcome == "Too High"
    assert "HIGHER" in message

def test_check_guess_too_low():
    """Test that guessing below secret returns 'Too Low'"""
    outcome, message = check_guess(25, 50)
    assert outcome == "Too Low"
    assert "LOWER" in message

def test_check_guess_win():
    """Test that correct guess returns 'Win'"""
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message

# ============================================
# Tests for update_score - FIXED: No negative scores!
# ============================================

def test_update_score_win():
    """Test winning score calculation"""
    score = update_score(0, "Win", 1)
    assert score >= 0
    # First attempt win: 100 - 10*(1+1) = 80
    assert score == 80

def test_update_score_too_high_no_negative():
    """Test that score never goes below 0 for 'Too High'"""
    score = update_score(0, "Too High", 1)
    assert score >= 0  # Should be 0, not negative

def test_update_score_too_low_no_negative():
    """Test that score never goes below 0 for 'Too Low'"""
    score = update_score(0, "Too Low", 1)
    assert score >= 0  # Should be 0, not negative

# ============================================
# Tests for parse_guess
# ============================================

def test_parse_guess_valid_number():
    """Test parsing a valid number"""
    ok, value, error = parse_guess("42")
    assert ok == True
    assert value == 42
    assert error is None

def test_parse_guess_decimal():
    """Test parsing a decimal number"""
    ok, value, error = parse_guess("45.7")
    assert ok == True
    assert value == 45  # Should convert to int

def test_parse_guess_non_number():
    """Test parsing non-number input"""
    ok, value, error = parse_guess("abc")
    assert ok == False
    assert value is None
    assert error == "That is not a number."

def test_parse_guess_empty():
    """Test parsing empty input"""
    ok, value, error = parse_guess("")
    assert ok == False
    assert value is None
    assert error == "Enter a guess."