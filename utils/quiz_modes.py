"""Quiz mode implementations using the Strategy Pattern.

This module defines the QuizMode abstract base class and three concrete
strategies for selecting the next flashcard:
    - SequentialMode: Cards are presented in order.
    - RandomMode: Cards are presented in a shuffled order.
    - AdaptiveMode: Cards the user got wrong are prioritized.
"""

import random
from abc import ABC, abstractmethod
from typing import Optional

from utils.data_loader import Flashcard


class QuizMode(ABC):
    """Abstract base class for quiz mode strategies.

    All quiz modes must implement the get_next_card method, which
    determines how the next flashcard is selected from the deck.
    """

    def __init__(self, cards: list[Flashcard]) -> None:
        """Initialize the quiz mode with a list of flashcards.

        Args:
            cards: The list of flashcards to quiz from.
        """
        self.cards: list[Flashcard] = cards
        self.current_index: int = 0

    @abstractmethod
    def get_next_card(self) -> Optional[Flashcard]:
        """Return the next flashcard to present to the user.

        Returns:
            The next Flashcard, or None if the quiz is complete.
        """
        pass

    @abstractmethod
    def report_answer(self, card: Flashcard, correct: bool) -> None:
        """Report whether the user answered a card correctly.

        Args:
            card: The flashcard that was answered.
            correct: True if the user's answer was correct.
        """
        pass

    @abstractmethod
    def is_complete(self) -> bool:
        """Check whether the quiz session is complete.

        Returns:
            True if all cards have been covered.
        """
        pass

    def reset(self) -> None:
        """Reset the quiz mode to start from the beginning."""
        self.current_index = 0


class SequentialMode(QuizMode):
    """Present flashcards in sequential order from first to last."""

    def __init__(self, cards: list[Flashcard]) -> None:
        """Initialize SequentialMode.

        Args:
            cards: The list of flashcards to quiz from.
        """
        super().__init__(cards)

    def get_next_card(self) -> Optional[Flashcard]:
        """Return the next card in sequential order.

        Returns:
            The next Flashcard, or None if all cards have been shown.
        """
        if self.current_index >= len(self.cards):
            return None
        card = self.cards[self.current_index]
        self.current_index += 1
        return card

    def report_answer(self, card: Flashcard, correct: bool) -> None:
        """Record the answer (no special behavior in sequential mode).

        Args:
            card: The flashcard that was answered.
            correct: True if the user's answer was correct.
        """
        pass

    def is_complete(self) -> bool:
        """Check if all cards have been presented.

        Returns:
            True if the current index has reached the end of the deck.
        """
        return self.current_index >= len(self.cards)


class RandomMode(QuizMode):
    """Present flashcards in a randomly shuffled order."""

    def __init__(self, cards: list[Flashcard]) -> None:
        """Initialize RandomMode with a shuffled copy of the card list.

        Args:
            cards: The list of flashcards to quiz from.
        """
        super().__init__(cards)
        self.shuffled_cards: list[Flashcard] = list(cards)
        random.shuffle(self.shuffled_cards)

    def get_next_card(self) -> Optional[Flashcard]:
        """Return the next card from the shuffled deck.

        Returns:
            The next shuffled Flashcard, or None if all have been shown.
        """
        if self.current_index >= len(self.shuffled_cards):
            return None
        card = self.shuffled_cards[self.current_index]
        self.current_index += 1
        return card

    def report_answer(self, card: Flashcard, correct: bool) -> None:
        """Record the answer (no special behavior in random mode).

        Args:
            card: The flashcard that was answered.
            correct: True if the user's answer was correct.
        """
        pass

    def is_complete(self) -> bool:
        """Check if all shuffled cards have been presented.

        Returns:
            True if the current index has reached the end of the shuffled deck.
        """
        return self.current_index >= len(self.shuffled_cards)


class AdaptiveMode(QuizMode):
    """Prioritize flashcards the user previously got wrong.

    In the first pass, all cards are presented sequentially. After the
    first pass, any cards answered incorrectly are re-queued for review.
    The quiz ends when all cards have been answered correctly at least once.
    """

    def __init__(self, cards: list[Flashcard]) -> None:
        """Initialize AdaptiveMode.

        Args:
            cards: The list of flashcards to quiz from.
        """
        super().__init__(cards)
        self.queue: list[Flashcard] = list(cards)
        self.incorrect_cards: list[Flashcard] = []
        self.passed_first_round: bool = False

    def get_next_card(self) -> Optional[Flashcard]:
        """Return the next card, prioritizing previously incorrect ones.

        After the initial pass through all cards, incorrect cards are
        re-queued. Returns None only when all cards have been answered
        correctly.

        Returns:
            The next Flashcard to present, or None if the quiz is complete.
        """
        if self.current_index < len(self.queue):
            card = self.queue[self.current_index]
            self.current_index += 1
            return card

        if self.incorrect_cards:
            self.queue = list(self.incorrect_cards)
            self.incorrect_cards = []
            self.current_index = 0
            self.passed_first_round = True
            card = self.queue[self.current_index]
            self.current_index += 1
            return card

        return None

    def report_answer(self, card: Flashcard, correct: bool) -> None:
        """Track incorrect answers for re-queuing.

        Args:
            card: The flashcard that was answered.
            correct: True if the user's answer was correct.
        """
        if not correct:
            self.incorrect_cards.append(card)

    def is_complete(self) -> bool:
        """Check if all cards have been answered correctly.

        Returns:
            True if the current queue is exhausted and no incorrect cards remain.
        """
        return self.current_index >= len(self.queue) and len(self.incorrect_cards) == 0
