"""Tests for the quiz mode strategies and the quiz mode factory.

Tests cover the Strategy Pattern implementations (Sequential, Random,
Adaptive) and the Factory Pattern for mode creation.
"""

import pytest

from utils.data_loader import Flashcard
from utils.quiz_engine import QuizEngine, QuizModeFactory, VALID_MODES
from utils.quiz_modes import (
    AdaptiveMode,
    RandomMode,
    SequentialMode,
)


def sample_cards() -> list[Flashcard]:
    """Create a sample list of flashcards for testing.

    Returns:
        A list of three sample Flashcard objects.
    """
    return [
        Flashcard(front="Q1", back="A1"),
        Flashcard(front="Q2", back="A2"),
        Flashcard(front="Q3", back="A3"),
    ]


class TestQuizModeFactory:
    """Tests for the QuizModeFactory."""

    def test_quiz_mode_factory_sequential(self) -> None:
        """Test that the factory returns a SequentialMode instance."""
        cards = sample_cards()
        mode = QuizModeFactory.create("sequential", cards)
        assert isinstance(mode, SequentialMode)

    def test_quiz_mode_factory_random(self) -> None:
        """Test that the factory returns a RandomMode instance."""
        cards = sample_cards()
        mode = QuizModeFactory.create("random", cards)
        assert isinstance(mode, RandomMode)

    def test_quiz_mode_factory_adaptive(self) -> None:
        """Test that the factory returns an AdaptiveMode instance."""
        cards = sample_cards()
        mode = QuizModeFactory.create("adaptive", cards)
        assert isinstance(mode, AdaptiveMode)

    def test_quiz_mode_factory_case_insensitive(self) -> None:
        """Test that the factory handles case-insensitive mode names."""
        cards = sample_cards()
        mode = QuizModeFactory.create("SEQUENTIAL", cards)
        assert isinstance(mode, SequentialMode)

    def test_quiz_mode_factory_with_whitespace(self) -> None:
        """Test that the factory strips whitespace from mode names."""
        cards = sample_cards()
        mode = QuizModeFactory.create("  random  ", cards)
        assert isinstance(mode, RandomMode)

    def test_quiz_mode_factory_invalid_mode(self) -> None:
        """Test that the factory raises ValueError for unknown modes."""
        cards = sample_cards()
        with pytest.raises(ValueError, match="Unknown quiz mode"):
            QuizModeFactory.create("nonexistent", cards)

    def test_valid_modes_list(self) -> None:
        """Test that VALID_MODES contains the expected modes."""
        assert "sequential" in VALID_MODES
        assert "random" in VALID_MODES
        assert "adaptive" in VALID_MODES


class TestSequentialMode:
    """Tests for SequentialMode."""

    def test_sequential_order(self) -> None:
        """Test that cards are returned in sequential order."""
        cards = sample_cards()
        mode = SequentialMode(cards)
        results = []
        while not mode.is_complete():
            card = mode.get_next_card()
            if card is not None:
                results.append(card)
                mode.report_answer(card, True)
        assert results == cards

    def test_sequential_returns_none_when_complete(self) -> None:
        """Test that get_next_card returns None after all cards."""
        cards = sample_cards()
        mode = SequentialMode(cards)
        for _ in range(len(cards)):
            mode.get_next_card()
        assert mode.get_next_card() is None

    def test_sequential_is_complete(self) -> None:
        """Test that is_complete returns True after all cards shown."""
        cards = sample_cards()
        mode = SequentialMode(cards)
        assert not mode.is_complete()
        for _ in range(len(cards)):
            mode.get_next_card()
        assert mode.is_complete()

    def test_sequential_reset(self) -> None:
        """Test that reset allows replaying from the start."""
        cards = sample_cards()
        mode = SequentialMode(cards)
        mode.get_next_card()
        mode.get_next_card()
        mode.reset()
        card = mode.get_next_card()
        assert card == cards[0]


class TestRandomMode:
    """Tests for RandomMode."""

    def test_random_returns_all_cards(self) -> None:
        """Test that all cards are returned regardless of order."""
        cards = sample_cards()
        mode = RandomMode(cards)
        results = []
        while not mode.is_complete():
            card = mode.get_next_card()
            if card is not None:
                results.append(card)
        assert set(c.front for c in results) == set(c.front for c in cards)
        assert len(results) == len(cards)

    def test_random_returns_none_when_complete(self) -> None:
        """Test that get_next_card returns None after all cards."""
        cards = sample_cards()
        mode = RandomMode(cards)
        for _ in range(len(cards)):
            mode.get_next_card()
        assert mode.get_next_card() is None

    def test_random_does_not_modify_original(self) -> None:
        """Test that RandomMode does not modify the original card list."""
        cards = sample_cards()
        original_order = list(cards)
        RandomMode(cards)
        assert cards == original_order

    def test_random_is_complete(self) -> None:
        """Test that is_complete works for RandomMode."""
        cards = sample_cards()
        mode = RandomMode(cards)
        assert not mode.is_complete()
        for _ in range(len(cards)):
            mode.get_next_card()
        assert mode.is_complete()


class TestAdaptiveMode:
    """Tests for AdaptiveMode."""

    def test_adaptive_mode_behavior(self) -> None:
        """Test that adaptive mode repeats incorrect cards.

        When the user answers a card incorrectly, it should appear
        again in a subsequent round.
        """
        cards = sample_cards()
        mode = AdaptiveMode(cards)

        card1 = mode.get_next_card()
        assert card1 is not None
        mode.report_answer(card1, True)

        card2 = mode.get_next_card()
        assert card2 is not None
        mode.report_answer(card2, False)

        card3 = mode.get_next_card()
        assert card3 is not None
        mode.report_answer(card3, True)

        assert not mode.is_complete()

        repeated = mode.get_next_card()
        assert repeated is not None
        assert repeated == card2
        mode.report_answer(repeated, True)

        assert mode.is_complete()

    def test_adaptive_all_correct(self) -> None:
        """Test that adaptive mode completes after all correct answers."""
        cards = sample_cards()
        mode = AdaptiveMode(cards)
        for _ in range(len(cards)):
            card = mode.get_next_card()
            assert card is not None
            mode.report_answer(card, True)
        assert mode.is_complete()

    def test_adaptive_all_incorrect_repeats(self) -> None:
        """Test that adaptive mode repeats all cards when all wrong."""
        cards = sample_cards()
        mode = AdaptiveMode(cards)

        for _ in range(len(cards)):
            card = mode.get_next_card()
            assert card is not None
            mode.report_answer(card, False)

        assert not mode.is_complete()

        repeated_count = 0
        while not mode.is_complete():
            card = mode.get_next_card()
            if card is not None:
                repeated_count += 1
                mode.report_answer(card, True)

        assert repeated_count == len(cards)

    def test_adaptive_multiple_rounds(self) -> None:
        """Test that adaptive mode can handle multiple rounds of retries."""
        cards = [Flashcard(front="Q1", back="A1")]
        mode = AdaptiveMode(cards)

        card = mode.get_next_card()
        assert card is not None
        mode.report_answer(card, False)

        card = mode.get_next_card()
        assert card is not None
        mode.report_answer(card, False)

        card = mode.get_next_card()
        assert card is not None
        mode.report_answer(card, True)

        assert mode.is_complete()


class TestQuizEngine:
    """Tests for the QuizEngine."""

    def test_engine_check_answer_correct(self) -> None:
        """Test that check_answer returns True for correct answers."""
        cards = sample_cards()
        mode = SequentialMode(cards)
        engine = QuizEngine(mode)
        card = engine.get_next_card()
        assert card is not None
        assert engine.check_answer(card, "A1") is True

    def test_engine_check_answer_case_insensitive(self) -> None:
        """Test that answer checking is case-insensitive."""
        cards = sample_cards()
        mode = SequentialMode(cards)
        engine = QuizEngine(mode)
        card = engine.get_next_card()
        assert card is not None
        assert engine.check_answer(card, "a1") is True

    def test_engine_check_answer_with_whitespace(self) -> None:
        """Test that answer checking strips whitespace."""
        cards = sample_cards()
        mode = SequentialMode(cards)
        engine = QuizEngine(mode)
        card = engine.get_next_card()
        assert card is not None
        assert engine.check_answer(card, "  A1  ") is True

    def test_engine_check_answer_incorrect(self) -> None:
        """Test that check_answer returns False for wrong answers."""
        cards = sample_cards()
        mode = SequentialMode(cards)
        engine = QuizEngine(mode)
        card = engine.get_next_card()
        assert card is not None
        assert engine.check_answer(card, "wrong") is False

    def test_engine_stats_tracking(self) -> None:
        """Test that the engine tracks statistics correctly."""
        cards = sample_cards()
        mode = SequentialMode(cards)
        engine = QuizEngine(mode)

        card1 = engine.get_next_card()
        assert card1 is not None
        engine.check_answer(card1, "A1")

        card2 = engine.get_next_card()
        assert card2 is not None
        engine.check_answer(card2, "wrong")

        assert engine.stats.total_questions == 2
        assert engine.stats.correct_answers == 1
        assert engine.stats.incorrect_answers == 1
        assert engine.stats.accuracy == 50.0

    def test_engine_is_complete(self) -> None:
        """Test that is_complete delegates to the quiz mode."""
        cards = sample_cards()
        mode = SequentialMode(cards)
        engine = QuizEngine(mode)
        assert not engine.is_complete()
        for _ in range(len(cards)):
            card = engine.get_next_card()
            if card:
                engine.check_answer(card, "A1")
        assert engine.is_complete()


class TestSessionStats:
    """Tests for SessionStats via QuizEngine."""

    def test_stats_accuracy_zero_questions(self) -> None:
        """Test accuracy is 0.0 when no questions answered."""
        cards = sample_cards()
        mode = SequentialMode(cards)
        engine = QuizEngine(mode)
        assert engine.stats.accuracy == 0.0

    def test_stats_missed_cards_no_duplicates(self) -> None:
        """Test that missed cards list does not contain duplicates."""
        cards = sample_cards()
        mode = SequentialMode(cards)
        engine = QuizEngine(mode)
        card = engine.get_next_card()
        assert card is not None
        engine.check_answer(card, "wrong")
        engine.stats.record_answer(card, False)
        assert len(engine.stats.missed_cards) == 1

    def test_stats_perfect_score(self) -> None:
        """Test stats when user gets everything right."""
        cards = sample_cards()
        mode = SequentialMode(cards)
        engine = QuizEngine(mode)
        for _ in range(len(cards)):
            card = engine.get_next_card()
            assert card is not None
            engine.check_answer(card, card.back)
        assert engine.stats.accuracy == 100.0
        assert len(engine.stats.missed_cards) == 0
