"""Flashcard Quizzer CLI Application.

A command-line tool for studying flashcards with multiple quiz modes.
Supports sequential, random, and adaptive learning strategies.

Usage:
    python main.py -f data/glossary.json -m sequential
    python main.py --file data/python_basics.json --mode adaptive --stats
"""

import argparse
import sys

from utils.data_loader import load_flashcards
from utils.quiz_engine import QuizEngine, QuizModeFactory, VALID_MODES
from utils.ui import (
    display_correct,
    display_error,
    display_exit_message,
    display_incorrect,
    display_question,
    display_stats,
    display_welcome,
    get_user_answer,
)


def parse_arguments(args: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments for the Flashcard Quizzer.

    Args:
        args: Optional list of arguments (for testing). If None,
              sys.argv is used.

    Returns:
        Parsed argument namespace with file, mode, and stats attributes.
    """
    parser = argparse.ArgumentParser(
        prog="Flashcard Quizzer",
        description="A CLI tool for studying flashcards with multiple quiz modes.",
        epilog="Example: python main.py -f data/glossary.json -m random",
    )

    parser.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,
        help="Path to the JSON file containing flashcards.",
    )

    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        choices=VALID_MODES,
        default="sequential",
        help="Quiz mode: sequential, random, or adaptive (default: sequential).",
    )

    parser.add_argument(
        "--stats",
        action="store_true",
        default=False,
        help="Show detailed statistics at the end of the quiz.",
    )

    return parser.parse_args(args)


def run_quiz(file_path: str, mode_name: str, show_stats: bool) -> None:
    """Run a complete quiz session.

    Args:
        file_path: Path to the flashcard JSON file.
        mode_name: The quiz mode to use.
        show_stats: Whether to display detailed stats at the end.
    """
    flashcards = load_flashcards(file_path)

    try:
        mode = QuizModeFactory.create(mode_name, flashcards)
    except ValueError as e:
        display_error(str(e))
        sys.exit(1)

    engine = QuizEngine(mode)
    display_welcome(mode_name, len(flashcards))

    question_number = 0

    try:
        while not engine.is_complete():
            card = engine.get_next_card()
            if card is None:
                break

            question_number += 1
            display_question(card, question_number)
            answer = get_user_answer()

            if answer.strip().lower() == "exit":
                display_exit_message()
                if show_stats:
                    display_stats(engine.stats)
                return

            if engine.check_answer(card, answer):
                display_correct()
            else:
                display_incorrect(card.back)

    except KeyboardInterrupt:
        display_exit_message()
        if show_stats:
            display_stats(engine.stats)
        return

    display_stats(engine.stats)


def main() -> None:
    """Entry point for the Flashcard Quizzer application."""
    args = parse_arguments()
    run_quiz(args.file, args.mode, args.stats)


if __name__ == "__main__":
    main()
