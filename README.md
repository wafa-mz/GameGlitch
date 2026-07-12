# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

### Game Purpose
The game is a number guessing game where the player selects a difficulty (Easy, Normal, Hard) and tries to guess a secret number within a limited number of attempts. The game tracks the player's score and provides hints (Too High/Too Low) after each guess.

### Bugs Found

**Bug 1: Secret Number Wrong Range**
- **Issue**: On Easy mode, the secret number was 53 (outside the 1-20 range)
- **Cause**: The secret was stored in session state and not regenerated when difficulty changed
- **Fix**: Changed `new_game` to use `random.randint(low, high)` instead of `random.randint(1, 100)`
- **Location**: app.py line ~142

**Bug 2: Attempts Counter Off by One**
- **Issue**: "Attempts left" showed 1 instead of 6 on Easy mode
- **Cause**: `st.session_state.attempts` was initialized to 1 instead of 0
- **Fix**: Changed initialization to `attempts = 0`
- **Location**: app.py line ~102

**Bug 3: Score Goes Negative**
- **Issue**: Score could go to -15 after wrong guesses
- **Cause**: No minimum score check in `update_score` function
- **Fix**: Added `max(0, new_score)` to prevent negative scores
- **Location**: logic_utils.py line ~51-56

**Bug 4: Info Box Wrong Range**
- **Issue**: Info box always showed "between 1 and 100"
- **Cause**: Hardcoded value instead of using difficulty range
- **Fix**: Changed to `f"Guess a number between {low} and {high}. "`
- **Location**: app.py line ~119

### Fixes Applied

1. **Secret Range Fix**: Updated `new_game` to use `random.randint(low, high)` 
2. **Attempts Fix**: Changed `st.session_state.attempts = 1` to `= 0`
3. **Score Fix**: Added `max(0, new_score)` to prevent negative scores
4. **Info Box Fix**: Changed hardcoded "1 and 100" to `{low} and {high}`
5. **Refactoring**: Moved all logic functions to `logic_utils.py`
6. **FIXME Comments**: Added comments documenting bug locations and fixes
7. **Testing**: Created 13 pytest tests to verify all functionality

## 📸 Demo Walkthrough

Here is a step-by-step walkthrough of a complete game session:

### Starting the Game

1. **Launch the game:**
   ```bash
   python3 -m streamlit run app.py
   Game opens in browser with title "Game Glitch Investigator"

Sidebar shows: Difficulty = "Normal", Range = "1 to 100", Attempts = 8

Select Difficulty - Easy Mode:

User changes difficulty to "Easy" in the sidebar

Sidebar updates to: Range = "1 to 20", Attempts allowed = 6

Info box shows: "Guess a number between 1 and 20. Attempts left: 6"

Gameplay Walkthrough
First Guess - Too Low:

User enters guess: "10"

Game returns hint: "Too Low 📉 Go LOWER!"

Score decreases by 5 points

Attempts left now shows: 5

Second Guess - Too High:

User enters guess: "18"

Game returns hint: "Too High 📈 Go HIGHER!"

Score decreases by 5 points

Attempts left now shows: 4

Third Guess - Correct!

User enters guess: "15"

Game returns: "Win 🎉 Correct!"

Balloons appear on screen

Score calculates: 80 points (100 - 10*(attempt_number+1))

Game shows: "You won! The secret was 15. Final score: 80"

New Game
Starting Over:

User clicks "New Game" button

Game resets with a new secret number in the same difficulty range

Attempts reset to 0

Score resets to 0

Invalid Input Handling
Invalid Input:

User guesses "abc"

Game returns error: "That is not a number"

No score change, no attempt counted
## 🧪 Test Results

All tests passed successfully:
============= test session starts ==============
platform darwin -- Python 3.13.3, pytest-9.1.0, pluggy-1.6.0
rootdir: /Users/wafaalzahrani/Desktop/GameGlitch
collected 13 items

tests/test_game_logic.py::test_get_range_for_difficulty_easy PASSED [ 7%]
tests/test_game_logic.py::test_get_range_for_difficulty_normal PASSED [ 15%]
tests/test_game_logic.py::test_get_range_for_difficulty_hard PASSED [ 23%]
tests/test_game_logic.py::test_check_guess_too_high PASSED [ 30%]
tests/test_game_logic.py::test_check_guess_too_low PASSED [ 38%]
tests/test_game_logic.py::test_check_guess_win PASSED [ 46%]
tests/test_game_logic.py::test_update_score_win PASSED [ 53%]
tests/test_game_logic.py::test_update_score_too_high_no_negative PASSED [ 61%]
tests/test_game_logic.py::test_update_score_too_low_no_negative PASSED [ 69%]
tests/test_game_logic.py::test_parse_guess_valid_number PASSED [ 76%]
tests/test_game_logic.py::test_parse_guess_decimal PASSED [ 84%]
tests/test_game_logic.py::test_parse_guess_non_number PASSED [ 92%]
tests/test_game_logic.py::test_parse_guess_empty PASSED [100%]

============== 13 passed in 0.10s ==============
### Test Results Summary

| Status | Count |
|--------|-------|
| ✅ PASSED | 13 tests |
| ❌ FAILED | 0 tests |
| ⏱️ Time | 0.10 seconds |

### What the Tests Verify

| Test Category | What It Tests | Status |
|---------------|---------------|--------|
| `get_range_for_difficulty` | Difficulty ranges (Easy: 1-20, Normal: 1-100, Hard: 1-50) | ✅ PASSED |
| `check_guess` | Correct guess returns "Win", wrong guesses return "Too High"/"Too Low" | ✅ PASSED |
| `update_score` | Score calculation and prevention of negative scores | ✅ PASSED |
| `parse_guess` | Handling of valid numbers, decimals, non-numbers, and empty input | ✅ PASSED |

## 🔧 How to Run Tests

To run the tests yourself:

```bash
# Install pytest
pip install pytest

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_game_logic.py -v
## 📁 Project Structure
GameGlitch/
├── app.py # Main Streamlit application
├── logic_utils.py # Game logic functions (refactored)
├── tests/
│ └── test_game_logic.py # Pytest test suite (13 passing)
├── reflection.md # Project reflection
├── README.md # This file
├── requirements.txt # Python dependencies
├── ai_interactions.md # AI interaction log
└── .gitignore # Git ignore file

## 📚 Reflection

Working on this project taught me several important lessons about AI-generated code:

1. **AI Code Looks Correct But Can Be Wrong**: The code ran without syntax errors but had serious logic bugs that only showed up during gameplay

2. **Testing is Essential**: Pytest tests helped verify each fix worked correctly and prevented regressions

3. **Session State Matters**: Streamlit's session state persists across reruns and difficulty changes, requiring careful management

4. **AI is a Tool**: AI suggestions need to be reviewed and verified; they're not always correct

5. **Documentation Helps**: Clear FIXME comments and reflections help track what was fixed and why

6. **Refactoring Benefits**: Separating logic from UI code makes testing and debugging significantly easier

## 🎯 Summary of Fixes

| Bug | Original Behavior | Fixed Behavior |
|-----|-------------------|----------------|
| Secret Range | Secret was 53 on Easy (1-20 range) | Secret is always within difficulty range |
| Attempts Counter | Showed 1 instead of 6 on Easy | Shows correct number of attempts |
| Score | Went negative (-15) | Stays at 0 or above |
| Info Box | Always showed "1-100" | Shows correct difficulty range |
| Tests | No tests existed | 13 passing tests |