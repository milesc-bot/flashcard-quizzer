"""User interface module for the Flashcard Quizzer CLI.

Handles all terminal display logic including colored output,
quiz prompts, and session statistics display.
"""

from colorama import Fore, Style, init

from utils.data_loader import Flashcard
from utils.quiz_engine import SessionStats

init(autoreset=True)


def display_welcome(mode: str, card_count: int) -> None:
    """Display a welcome message at the start of a quiz session.

    Args:
        mode: The name of the quiz mode being used.
        card_count: The total number of cards in the deck.
    """
    print(f"\n{Style.BRIGHT}{'=' * 50}")
    print(f"  Flashcard Quizzer - {mode.capitalize()} Mode")
    print(f"  {card_count} cards loaded")
    print(f"{'=' * 50}{Style.RESET_ALL}")
    print("Type your answer and press Enter.")
    print("Type 'exit' or press Ctrl+C to quit at any time.\n")


def display_question(card: Flashcard, question_number: int) -> None:
    """Display a flashcard question to the user.

    Args:
        card: The flashcard to display.
        question_number: The current question number.
    """
    print(f"{Style.BRIGHT}Question {question_number}:{Style.RESET_ALL}")
    print(f"  {card.front}")


def get_user_answer() -> str:
    """Prompt the user for their answer.

    Returns:
        The user's input string, or 'exit' if they want to quit.
    """
    try:
        answer = input("\n  Your answer: ")
        return answer
    except EOFError:
        return "exit"


def display_correct() -> None:
    """Display a 'Correct!' message in green."""
    print(f"  {Fore.GREEN}{Style.BRIGHT}Correct!{Style.RESET_ALL}\n")


def display_incorrect(correct_answer: str) -> None:
    """Display an 'Incorrect' message in red with the correct answer.

    Args:
        correct_answer: The correct answer to display.
    """
    print(
        f"  {Fore.RED}{Style.BRIGHT}Incorrect.{Style.RESET_ALL} "
        f"The answer is: {Style.BRIGHT}{correct_answer}{Style.RESET_ALL}\n"
    )


def display_stats(stats: SessionStats) -> None:
    """Display the session statistics summary table.

    Args:
        stats: The SessionStats object containing quiz results.
    """
    print(f"\n{Style.BRIGHT}{'=' * 50}")
    print("  Quiz Complete - Session Summary")
    print(f"{'=' * 50}{Style.RESET_ALL}")
    print(f"  Total Questions:  {stats.total_questions}")
    print(f"  Correct Answers:  {stats.correct_answers}")
    print(f"  Incorrect Answers: {stats.incorrect_answers}")
    print(f"  Accuracy:         {stats.accuracy:.1f}%")

    if stats.missed_cards:
        print(f"\n{Style.BRIGHT}  Terms You Missed:{Style.RESET_ALL}")
        print(f"  {'-' * 40}")
        print(f"  {'Front':<25} {'Correct Answer'}")
        print(f"  {'-' * 40}")
        for card in stats.missed_cards:
            print(f"  {card.front:<25} {card.back}")
    else:
        print(
            f"\n  {Fore.GREEN}{Style.BRIGHT}Perfect score! "
            f"You got every card right!{Style.RESET_ALL}"
        )
    print(f"\n{'=' * 50}\n")


def display_exit_message() -> None:
    """Display a message when the user exits the quiz early."""
    print(f"\n{Style.BRIGHT}Quiz ended early.{Style.RESET_ALL}")
    print("Thanks for studying! See you next time.\n")


def display_error(message: str) -> None:
    """Display an error message in red.

    Args:
        message: The error message to display.
    """
    print(f"{Fore.RED}Error: {message}{Style.RESET_ALL}")
