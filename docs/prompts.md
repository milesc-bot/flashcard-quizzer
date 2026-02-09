# Prompt Log - Flashcard Quizzer Project

This document records the specific prompts used during AI-assisted development of the Flashcard Quizzer CLI application.

---

## Prompt 1: Project Setup and Data Layer

**Prompt:**
> Build a data loader module (`utils/data_loader.py`) for a flashcard quiz application. Requirements:
> - Create a `Flashcard` class with `front` and `back` string attributes
> - Implement a `load_flashcards(file_path: str) -> list[Flashcard]` function
> - Support two JSON formats: array format `[{"front": "...", "back": "..."}]` and object format `{"cards": [...]}`
> - Validate that each card has non-empty `front` and `back` string fields
> - Handle errors gracefully: file not found, invalid JSON, missing fields — print friendly messages and exit, no stack traces
> - Use Python type hints on all functions
> - Follow PEP 8 guidelines with docstrings

**Result:** Generated complete data_loader.py with Flashcard class and validation logic.

---

## Prompt 2: Strategy Pattern - Quiz Modes

**Prompt:**
> Implement the quiz engine using the Strategy Pattern in `utils/quiz_modes.py`. Requirements:
> - Create a `QuizMode` abstract base class (using `abc.ABC`) with abstract methods: `get_next_card() -> Optional[Flashcard]`, `report_answer(card, correct)`, and `is_complete() -> bool`
> - Implement `SequentialMode`: present cards in order from 1 to N
> - Implement `RandomMode`: shuffle the deck and present in random order (don't modify the original list)
> - Implement `AdaptiveMode`: present all cards first, then re-queue any the user got wrong; repeat until all are answered correctly
> - All functions must have type hints and docstrings

**Result:** Generated quiz_modes.py with all three strategy implementations.

---

## Prompt 3: Factory Pattern and Quiz Engine

**Prompt:**
> Create `utils/quiz_engine.py` with:
> - A `QuizModeFactory` class that uses the Factory Pattern to create the correct `QuizMode` subclass from a string argument ('sequential', 'random', or 'adaptive'). Handle case-insensitivity and whitespace. Raise `ValueError` for invalid modes.
> - A `SessionStats` class tracking: total_questions, correct_answers, missed_cards list, and an accuracy property (handle division by zero)
> - A `QuizEngine` class that takes a `QuizMode`, provides `get_next_card()`, `check_answer(card, user_answer)` with case-insensitive comparison, and `is_complete()`
> - All with type hints and docstrings

**Result:** Generated quiz_engine.py with factory, stats, and engine classes.

---

## Prompt 4: CLI Interface and UI

**Prompt:**
> Build the CLI entry point (`main.py`) and UI module (`utils/ui.py`):
> - main.py: Use `argparse` with flags: `-f/--file` (required, path to JSON), `-m/--mode` (choices: sequential/random/adaptive, default: sequential), `--stats` (show detailed stats)
> - main.py: Implement `run_quiz()` function with the quiz loop, 'exit' command support, and Ctrl+C handling
> - utils/ui.py: Create display functions using `colorama` for colored output: green for correct answers, red for incorrect
> - Show a summary table at quiz end: total questions, accuracy %, and missed terms table
> - Handle both 'exit' command and Ctrl+C to quit gracefully

**Result:** Generated main.py with argparse and run_quiz, and ui.py with all display functions.

---

## Prompt 5: Comprehensive Test Suite

**Prompt:**
> Write a comprehensive pytest test suite across three files:
>
> **tests/test_flashcard_loader.py:**
> - test_load_valid_flashcards_array: Load array format JSON correctly
> - test_load_invalid_json: Handle malformed JSON gracefully
> - test_load_missing_required_field: Reject cards without 'back' field
> - Tests for: empty files, non-JSON files, whitespace-only fields, object format, both real data files
>
> **tests/test_quiz_modes.py:**
> - test_quiz_mode_factory: Factory returns correct class instances
> - test_adaptive_mode_behavior: Incorrect cards are repeated
> - Tests for: sequential order, random completeness, all-correct/all-wrong adaptive paths, engine stats, case-insensitive answers
>
> **tests/test_integration.py:**
> - test_full_session: Simulate 3 questions (2 correct, 1 wrong), verify stats
> - Tests for: CLI argument parsing, exit command, Ctrl+C handling, end-to-end file-to-quiz flow
>
> Target: >80% code coverage. Use tempfile for test JSON files, unittest.mock.patch for input simulation.

**Result:** Generated 68 tests achieving 98% code coverage.

---

## Prompt 6: Code Quality and Formatting

**Prompt:**
> Run black, flake8, and mypy on the entire codebase. Fix all issues found. Specifically:
> - Format all Python files with black
> - Fix any flake8 errors (unused imports, unnecessary f-strings, line length)
> - Ensure type hints are consistent throughout
> - Verify PEP 8 compliance

**Result:** Fixed 4 formatting issues (black), 7 flake8 errors (2 unused imports, 5 unnecessary f-strings).

---

## Prompt 7: Sample Data Files

**Prompt:**
> Create two sample flashcard JSON files in the `data/` directory:
> - `data/glossary.json`: Array format with 10 server/tech acronyms (API, CLI, DNS, HTTP, JSON, REST, SQL, SSH, TCP, URL) with full expansions as answers
> - `data/python_basics.json`: Object format `{"cards": [...]}` with 10 Python basics questions (def, bool, len, class, #, append, try, int, import, dictionary)

**Result:** Generated both data files with correct formats.

---

## Prompt 8: Production PR Guidelines Audit

**Prompt:**
> Review the entire Flashcard Quizzer codebase against the following production PR guidelines for AI-generated code:
> 1. Honor the code quality pyramid: correctness > readability > maintainability > performance
> 2. Follow review-friendly structure: separated concerns, small single-responsibility functions, matching existing patterns
> 3. Naming and clarity: descriptive names, self-documenting code, comments explain "why" not "what"
> 4. Error handling: validate inputs, handle edge cases, fail safely, surface errors for debugging
> 5. Testability: easy to unit test, minimal external dependencies in core logic, avoid tight coupling
> 6. Do not delete unrelated behavior: preserve all existing side effects unless instructed
> 7. Keep diffs small and targeted: smallest change that satisfies requirement
> 8. Avoid common red flags: functions doing too many things, deep nesting, copy-paste, hardcoded values, no error handling, unclear naming
> 9. Dependencies must be real and compatible: no invented libraries, no deprecated packages, correct signatures
> 10. Default to safe, predictable behavior: explicit over clever, prefer pure functions, avoid hidden side effects
>
> For each guideline, document whether the codebase passes, and cite specific examples from the code.

**Result:** The codebase passed all 10 guideline categories. The audit confirmed that the iterative review process (Interactions 1-6) had already addressed the key quality concerns. Specific findings were documented in ai_edit_log.md Interaction 7.

---

## Refinement Prompts

### Refinement A: Empty String Validation
> "The data loader accepts empty strings for front and back fields. Add validation that both fields must be non-empty strings (not just whitespace). Raise ValueError with a descriptive message."

### Refinement B: Adaptive Mode Completion Fix
> "The AdaptiveMode is_complete() returns True too early when there are incorrect cards that haven't been re-queued yet. Fix the logic so is_complete() only returns True when current_index >= len(queue) AND len(incorrect_cards) == 0."

### Refinement C: F-string Cleanup
> "Remove unnecessary f-strings from ui.py where there are no interpolation variables. flake8 reports F541 errors on lines 26, 27, 48, 78, 103."
