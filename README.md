# Flashcard Quizzer CLI Application

A command-line tool for studying flashcards with multiple quiz modes. Built using AI-assisted development with the Strategy and Factory design patterns.

## Features

- **Three Quiz Modes:**
  - **Sequential:** Cards presented in order (1 to N)
  - **Random:** Cards shuffled for varied practice
  - **Adaptive:** Prioritizes cards you got wrong — keeps quizzing until mastered
- **JSON Data Loading:** Supports both array and object format flashcard files
- **Input Validation:** Graceful error messages for missing files, malformed JSON, and invalid data
- **Colored Output:** Green for correct answers, red for incorrect (using colorama)
- **Session Statistics:** Accuracy percentage, total questions, and missed terms summary
- **Graceful Exit:** Type "exit" or press Ctrl+C to quit without errors

## Project Structure

```
flashcard-quizzer/
├── main.py                    # CLI entry point with argparse
├── utils/
│   ├── __init__.py
│   ├── data_loader.py         # JSON loading and validation
│   ├── quiz_modes.py          # Strategy Pattern (Sequential, Random, Adaptive)
│   ├── quiz_engine.py         # Factory Pattern and session management
│   └── ui.py                  # Colored terminal display logic
├── tests/
│   ├── __init__.py
│   ├── test_flashcard_loader.py  # Data loader unit tests
│   ├── test_quiz_modes.py        # Quiz mode and engine tests
│   └── test_integration.py       # Full session integration tests
├── data/
│   ├── glossary.json           # Tech acronyms (array format)
│   └── python_basics.json      # Python basics (object format)
├── docs/
│   ├── ai_edit_log.md          # AI interaction documentation
│   ├── final_report.md         # Project report (1000-1500 words)
│   └── prompts.md              # Prompt log
├── requirements.txt
└── README.md
```

## Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd flashcard-quizzer
```

2. Create and activate a virtual environment:
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Commands

```bash
# Display help and available flags
python main.py --help

# Sequential mode (default)
python main.py -f data/glossary.json -m sequential

# Random mode
python main.py --file data/python_basics.json --mode random

# Adaptive mode with detailed stats
python main.py -f data/python_basics.json -m adaptive --stats
```

### Command-Line Flags

| Flag | Short | Description | Default |
|------|-------|-------------|---------|
| `--file` | `-f` | Path to JSON flashcard file (required) | — |
| `--mode` | `-m` | Quiz mode: sequential, random, adaptive | sequential |
| `--stats` | — | Show detailed statistics on exit | off |

### JSON File Formats

**Array Format** (`data/glossary.json`):
```json
[
  {"front": "API", "back": "Application Programming Interface"},
  {"front": "CLI", "back": "Command Line Interface"}
]
```

**Object Format** (`data/python_basics.json`):
```json
{
  "cards": [
    {"front": "What keyword defines a function?", "back": "def"},
    {"front": "What data type stores True/False?", "back": "bool"}
  ]
}
```

## Running Tests

```bash
# Run all tests with coverage report
pytest --cov=. --cov-report=term-missing -v

# Generate HTML coverage report
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_flashcard_loader.py -v
```

**Current Coverage:** 98% (68 tests passing)

## Code Quality

```bash
# Format code with black
black .

# Lint with flake8
flake8 --max-line-length=99 main.py utils/ tests/

# Type check with mypy
mypy main.py utils/
```

## Design Patterns

### Strategy Pattern (Quiz Modes)
The `QuizMode` abstract base class defines the interface for card selection. Three concrete strategies (`SequentialMode`, `RandomMode`, `AdaptiveMode`) implement different algorithms. This allows adding new modes without modifying existing code.

### Factory Pattern (Mode Selection)
The `QuizModeFactory` creates the appropriate `QuizMode` instance from a string identifier, decoupling mode creation from usage.

## Dependencies

- **colorama** (>=0.4.6) — Cross-platform colored terminal output
- **pytest** (>=7.0.0) — Testing framework
- **pytest-cov** (>=4.0.0) — Code coverage reporting
- **black** (>=23.0.0) — Code formatting
- **mypy** (>=1.0.0) — Static type checking
- **flake8** (>=6.0.0) — Code linting

## License

This project was developed as part of the Udacity AI-Assisted Engineering course.
