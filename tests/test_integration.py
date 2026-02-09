"""Integration tests for the Flashcard Quizzer application.

These tests simulate full quiz sessions by mocking user input
and verifying the end-to-end behavior of the application.
"""

from unittest.mock import patch

import pytest

from main import parse_arguments, run_quiz
from utils.data_loader import Flashcard, load_flashcards
from utils.quiz_engine import QuizEngine, QuizModeFactory
from utils.quiz_modes import SequentialMode


class TestParseArguments:
    """Tests for CLI argument parsing."""

    def test_parse_required_args(self) -> None:
        """Test parsing with required arguments."""
        args = parse_arguments(["-f", "data/glossary.json", "-m", "sequential"])
        assert args.file == "data/glossary.json"
        assert args.mode == "sequential"
        assert args.stats is False

    def test_parse_long_flags(self) -> None:
        """Test parsing with long-form flags."""
        args = parse_arguments(
            ["--file", "data/glossary.json", "--mode", "random", "--stats"]
        )
        assert args.file == "data/glossary.json"
        assert args.mode == "random"
        assert args.stats is True

    def test_parse_default_mode(self) -> None:
        """Test that the default mode is 'sequential'."""
        args = parse_arguments(["-f", "data/glossary.json"])
        assert args.mode == "sequential"

    def test_parse_invalid_mode(self) -> None:
        """Test that an invalid mode raises SystemExit."""
        with pytest.raises(SystemExit):
            parse_arguments(["-f", "data/glossary.json", "-m", "invalid"])

    def test_parse_missing_file(self) -> None:
        """Test that missing file argument raises SystemExit."""
        with pytest.raises(SystemExit):
            parse_arguments(["-m", "sequential"])


class TestFullSession:
    """Integration tests simulating complete quiz sessions."""

    def test_full_session(self) -> None:
        """Simulate a user answering 3 questions and check final stats.

        The user answers Q1 correctly, Q2 incorrectly, and Q3 correctly.
        Expected: 3 total questions, 2 correct, 66.7% accuracy.
        """
        cards = [
            Flashcard(front="Q1", back="A1"),
            Flashcard(front="Q2", back="A2"),
            Flashcard(front="Q3", back="A3"),
        ]
        mode = SequentialMode(cards)
        engine = QuizEngine(mode)

        card1 = engine.get_next_card()
        assert card1 is not None
        engine.check_answer(card1, "A1")

        card2 = engine.get_next_card()
        assert card2 is not None
        engine.check_answer(card2, "wrong")

        card3 = engine.get_next_card()
        assert card3 is not None
        engine.check_answer(card3, "A3")

        assert engine.stats.total_questions == 3
        assert engine.stats.correct_answers == 2
        assert engine.stats.incorrect_answers == 1
        assert abs(engine.stats.accuracy - 66.7) < 0.1
        assert len(engine.stats.missed_cards) == 1
        assert engine.stats.missed_cards[0].front == "Q2"

    def test_full_session_all_correct(self) -> None:
        """Simulate a perfect quiz session with all correct answers."""
        cards = [
            Flashcard(front="Q1", back="A1"),
            Flashcard(front="Q2", back="A2"),
        ]
        mode = SequentialMode(cards)
        engine = QuizEngine(mode)

        for _ in range(len(cards)):
            card = engine.get_next_card()
            assert card is not None
            engine.check_answer(card, card.back)

        assert engine.stats.accuracy == 100.0
        assert len(engine.stats.missed_cards) == 0

    def test_full_session_all_wrong(self) -> None:
        """Simulate a quiz session where all answers are incorrect."""
        cards = [
            Flashcard(front="Q1", back="A1"),
            Flashcard(front="Q2", back="A2"),
        ]
        mode = SequentialMode(cards)
        engine = QuizEngine(mode)

        for _ in range(len(cards)):
            card = engine.get_next_card()
            assert card is not None
            engine.check_answer(card, "wrong")

        assert engine.stats.accuracy == 0.0
        assert len(engine.stats.missed_cards) == 2

    def test_run_quiz_with_exit(self) -> None:
        """Test that typing 'exit' gracefully ends the quiz."""
        user_inputs = ["exit"]
        with patch("builtins.input", side_effect=user_inputs):
            run_quiz("data/glossary.json", "sequential", False)

    def test_run_quiz_sequential_with_answers(self) -> None:
        """Test running a quiz with some answers then exit."""
        user_inputs = [
            "Application Programming Interface",
            "wrong answer",
            "exit",
        ]
        with patch("builtins.input", side_effect=user_inputs):
            run_quiz("data/glossary.json", "sequential", True)

    def test_run_quiz_keyboard_interrupt(self) -> None:
        """Test that Ctrl+C (KeyboardInterrupt) ends the quiz gracefully."""
        with patch("builtins.input", side_effect=KeyboardInterrupt):
            run_quiz("data/glossary.json", "sequential", True)

    def test_load_and_quiz_integration(self) -> None:
        """Test full integration from file loading to quiz completion."""
        cards = load_flashcards("data/glossary.json")
        assert len(cards) > 0

        mode = QuizModeFactory.create("sequential", cards)
        engine = QuizEngine(mode)

        card = engine.get_next_card()
        assert card is not None
        assert card.front == "API"

        result = engine.check_answer(card, "Application Programming Interface")
        assert result is True
        assert engine.stats.correct_answers == 1

    def test_adaptive_session_integration(self) -> None:
        """Test a complete adaptive mode session."""
        cards = [
            Flashcard(front="Q1", back="A1"),
            Flashcard(front="Q2", back="A2"),
        ]
        mode = QuizModeFactory.create("adaptive", cards)
        engine = QuizEngine(mode)

        card1 = engine.get_next_card()
        assert card1 is not None
        engine.check_answer(card1, "A1")

        card2 = engine.get_next_card()
        assert card2 is not None
        engine.check_answer(card2, "wrong")

        assert not engine.is_complete()

        card3 = engine.get_next_card()
        assert card3 is not None
        assert card3.front == "Q2"
        engine.check_answer(card3, "A2")

        assert engine.is_complete()
