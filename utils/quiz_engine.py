"""Quiz engine module implementing the Factory Pattern for quiz mode selection.

This module contains the QuizEngine class which manages the quiz session,
and the QuizModeFactory which creates the appropriate quiz mode strategy
based on user input.
"""

from typing import Optional

from utils.data_loader import Flashcard
from utils.quiz_modes import (
    AdaptiveMode,
    QuizMode,
    RandomMode,
    SequentialMode,
)

VALID_MODES: list[str] = ["sequential", "random", "adaptive"]


class QuizModeFactory:
    """Factory class for creating quiz mode strategy instances.

    Uses the Factory Pattern to instantiate the correct QuizMode
    subclass based on a string identifier provided by the user.
    """

    @staticmethod
    def create(mode_name: str, cards: list[Flashcard]) -> QuizMode:
        """Create and return a QuizMode instance based on the mode name.

        Args:
            mode_name: The name of the quiz mode ('sequential', 'random',
                       or 'adaptive').
            cards: The list of flashcards to use in the quiz.

        Returns:
            An instance of the appropriate QuizMode subclass.

        Raises:
            ValueError: If the mode_name is not recognized.
        """
        mode_name = mode_name.lower().strip()

        if mode_name == "sequential":
            return SequentialMode(cards)
        elif mode_name == "random":
            return RandomMode(cards)
        elif mode_name == "adaptive":
            return AdaptiveMode(cards)
        else:
            raise ValueError(
                f"Unknown quiz mode: '{mode_name}'. "
                f"Valid modes are: {', '.join(VALID_MODES)}"
            )


class SessionStats:
    """Tracks and computes statistics for a quiz session."""

    def __init__(self) -> None:
        """Initialize session statistics."""
        self.total_questions: int = 0
        self.correct_answers: int = 0
        self.missed_cards: list[Flashcard] = []

    def record_answer(self, card: Flashcard, correct: bool) -> None:
        """Record the result of a single answer.

        Args:
            card: The flashcard that was answered.
            correct: True if the user answered correctly.
        """
        self.total_questions += 1
        if correct:
            self.correct_answers += 1
        else:
            if card not in self.missed_cards:
                self.missed_cards.append(card)

    @property
    def incorrect_answers(self) -> int:
        """Return the number of incorrect answers."""
        return self.total_questions - self.correct_answers

    @property
    def accuracy(self) -> float:
        """Calculate and return the accuracy percentage.

        Returns:
            The accuracy as a percentage (0.0 to 100.0).
            Returns 0.0 if no questions have been answered.
        """
        if self.total_questions == 0:
            return 0.0
        return (self.correct_answers / self.total_questions) * 100


class QuizEngine:
    """Manages the quiz session using a given quiz mode strategy.

    The QuizEngine coordinates between the quiz mode (strategy),
    session statistics, and answer checking logic.
    """

    def __init__(self, mode: QuizMode) -> None:
        """Initialize the QuizEngine with a quiz mode strategy.

        Args:
            mode: The QuizMode strategy to use for card selection.
        """
        self.mode: QuizMode = mode
        self.stats: SessionStats = SessionStats()

    def get_next_card(self) -> Optional[Flashcard]:
        """Get the next flashcard from the current quiz mode.

        Returns:
            The next Flashcard, or None if the quiz is complete.
        """
        return self.mode.get_next_card()

    def check_answer(self, card: Flashcard, user_answer: str) -> bool:
        """Check whether the user's answer matches the card's back.

        The comparison is case-insensitive and strips leading/trailing
        whitespace from both sides.

        Args:
            card: The flashcard being answered.
            user_answer: The user's text input.

        Returns:
            True if the answer matches (case-insensitive).
        """
        correct = user_answer.strip().lower() == card.back.strip().lower()
        self.stats.record_answer(card, correct)
        self.mode.report_answer(card, correct)
        return correct

    def is_complete(self) -> bool:
        """Check whether the quiz session is complete.

        Returns:
            True if the quiz mode reports completion.
        """
        return self.mode.is_complete()
