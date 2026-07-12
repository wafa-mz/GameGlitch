# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The first time I ran the game, it opened in my browser with a nice-looking interface. However, I immediately noticed issues when I selected "Easy" mode - the info box said "Guess a number between 1 and 100" even though the sidebar showed "Range: 1 to 20". When I opened the Developer Debug Info and checked the secret number, it was 53, which is completely outside the Easy range of 1-20. I also noticed that "Attempts left" showed only 1 attempt instead of 6, and when I made my first guess, the game immediately said "Out of attempts!" and ended. The score also went negative to -15, which seemed wrong.

**Bug 1:** Secret number uses wrong range - on Easy mode, secret should be between 1-20 but was 53 (outside range).

**Bug 2:** Info box shows "between 1 and 100" regardless of difficulty - should show the actual range.

**Bug 3:** Attempts left shows wrong number - on Easy mode, shows 1 instead of 6 attempts left.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Select "Easy" mode and check info box | Info shows "between 1 and 20", attempts: 6 | Info shows "between 1 and 100", attempts: 1 | None |
| Guess 15 on Easy mode | Secret between 1-20, get hint, continue playing | Secret was 53 (wrong range!), "Out of attempts!" after 1 guess | None |
| Make multiple wrong guesses | Score stays at 0 or above | Score went to -15 (negative) | None |
| Click "New Game" on Easy mode | Secret resets to between 1-20 | Secret resets to between 1-100 | None |
| Guess "abc" (non-number) | Error: "That is not a number" | Error: "That is not a number" appears | None |

---

## 2. How did you use AI as a teammate?

I used the Continue AI coding assistant in VS Code to help me understand the code and identify bugs. I attached `app.py` and asked about the bugs I found. The AI gave me a detailed explanation of each bug:

**Why the secret is 53 on Easy mode:**
The AI explained that the range logic itself is correct (Easy should return 1-20), but the secret is generated once and stored in `st.session_state.secret` at lines 94-95. This value is not regenerated when the difficulty changes - it only resets when the user clicks "New Game" at lines 136-140. So if I previously played Normal mode and got a secret like 53, switching to Easy reuses that old secret instead of creating a fresh one in the Easy range.

**Why "Attempts left" shows 1 instead of 6:**
The AI pointed out that the displayed value comes from lines 111-114, which calculates `attempt_limit - st.session_state.attempts`. The attempts counter is stored in session state at lines 97-98 and only resets on "New Game" at lines 136-140. Because the counter carries over across runs and difficulty changes, a prior game can leave the app with a nearly exhausted attempt count, so Easy can show something like 1 remaining instead of a fresh 6.

**Why the score drops negative on wrong guesses:**
The AI explained that the penalty logic is in the `update_score` function at lines 50-67. Wrong guesses subtract points in the "Too High" and "Too Low" branches at lines 57-65. These branches are applied on every incorrect guess at lines 170-174. Each miss lowers the score, so repeated wrong guesses can drive it down to values like -15.

**The common pattern:** The AI identified that the app relies on persistent session state for the secret, attempts, and score without resetting them properly when the game context changes (like switching difficulties).

**Example of incorrect/misleading AI suggestion:** 
The AI initially suggested that the "Show hint" checkbox wasn't working because of a logic error in the code. However, after checking the code more carefully, I realized the checkbox logic actually works correctly in the code, and the bug might have been a UI issue or I might not have tested it properly. The AI was too quick to assume there was a code bug without considering other possibilities.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed when I could reproduce the scenario multiple times and get the expected behavior consistently. For example, after fixing the attempts counter, I started a new game on Easy mode and checked that "Attempts left" showed 6, then made a guess and confirmed it showed 5 attempts left. I repeated this multiple times with different difficulty settings to ensure it worked correctly.

**Test I ran:** I tested the secret number range bug by selecting "Easy" mode and clicking "New Game", then checking the Developer Debug Info to confirm the secret was between 1-20. I repeated this test 5 times and confirmed the secret was always in the correct range. I also tested Normal mode (1-100) and Hard mode (1-50) to verify the fix worked for all difficulties.

**Test results:**
- ✅ Easy mode: Secret between 1-20, attempts left shows 6
- ✅ Normal mode: Secret between 1-100, attempts left shows 8  
- ✅ Hard mode: Secret between 1-50, attempts left shows 5
- ✅ Score never goes below 0
- ✅ Info box shows correct range for each difficulty
- ✅ "New Game" correctly resets to the difficulty range

**How I verified each fix:**

| Bug | Fix Applied | How I Tested | Result |
|-----|-------------|--------------|--------|
| Secret wrong range | Changed `random.randint(1, 100)` to `random.randint(low, high)` in New Game | Checked Debug Info on Easy mode 5 times | ✅ Secret always 1-20 |
| Info box wrong range | Changed "1 and 100" to `{low} and {high}` | Checked info box on all difficulties | ✅ Shows correct range |
| Attempts start at 1 | Changed `attempts = 1` to `attempts = 0` | Checked "Attempts left" before guessing | ✅ Shows 6 on Easy |
| Score goes negative | Added `max(0, new_score)` | Made wrong guesses repeatedly | ✅ Score stays at 0 or above |

The AI helped me design these tests by suggesting I test all difficulty levels and use the Developer Debug Info panel to verify the secret number. This was very helpful for confirming my fixes worked correctly.

---

## 4. What did you learn about Streamlit and state?

Streamlit "reruns" the entire script every time you interact with the page, like clicking a button or entering text. This means that if you don't use session state to store values, they would reset every time you interact with the app. Session state is like a memory for the app - it stores variables that persist across reruns, so the app can remember things like the secret number, how many attempts you've made, and your score. This is different from a normal Python script that runs once and exits. In Streamlit, you need to use `st.session_state` to keep track of important values that should persist between user interactions.

---

## 5. Looking ahead: your developer habits

One habit I want to reuse in future projects is documenting bugs as I find them. Instead of just trying to fix bugs immediately, I took time to write down what I observed, what I expected, and what actually happened. This made it much easier to understand the problems and systematically fix them. I also want to keep using the Developer Debug Info panel approach - having a visible display of internal state was incredibly helpful for understanding what the code was actually doing.

One thing I would do differently next time is to test the game more thoroughly before assuming I understand all the bugs. I initially found only a few bugs, but when I played with different inputs and checked the debug info, I discovered many more issues. Next time, I'll create a systematic testing plan with different inputs and scenarios to catch all bugs.

This project changed the way I think about AI-generated code because I learned that AI can write code that looks correct but has serious logic bugs. The code ran without syntax errors, but the logic was fundamentally flawed in multiple ways. I now understand that I need to carefully test and verify AI-generated code rather than assuming it works just because it runs without errors. AI is a helpful tool, but I need to take ownership of understanding and testing the code.
