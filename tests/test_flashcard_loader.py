"""Tests for the flashcard data loader module.

Tests cover JSON loading, validation, error handling,
and support for both array and object JSON formats.
"""

import json
import os
import tempfile

import pytest

from utils.data_loader import (
    Flashcard,
    _extract_cards_list,
    _validate_card_data,
    load_flashcards,
)


class TestFlashcard:
    """Tests for the Flashcard dataclass."""

    def test_flashcard_creation(self) -> None:
        """Test that a Flashcard can be created with front and back values."""
        card = Flashcard(front="What is Python?", back="A programming language")
        assert card.front == "What is Python?"
        assert card.back == "A programming language"

    def test_flashcard_repr(self) -> None:
        """Test the string representation of a Flashcard."""
        card = Flashcard(front="Q1", back="A1")
        assert "Q1" in repr(card)
        assert "A1" in repr(card)

    def test_flashcard_equality(self) -> None:
        """Test equality comparison between Flashcard objects."""
        card1 = Flashcard(front="Q", back="A")
        card2 = Flashcard(front="Q", back="A")
        card3 = Flashcard(front="Q", back="B")
        assert card1 == card2
        assert card1 != card3

    def test_flashcard_equality_with_non_flashcard(self) -> None:
        """Test that comparing a Flashcard to a non-Flashcard returns NotImplemented."""
        card = Flashcard(front="Q", back="A")
        assert card != "not a flashcard"


class TestValidateCardData:
    """Tests for the _validate_card_data function."""

    def test_valid_card(self) -> None:
        """Test that a valid card passes validation."""
        _validate_card_data({"front": "Q", "back": "A"}, 0)

    def test_card_not_dict(self) -> None:
        """Test that a non-dict card raises ValueError."""
        with pytest.raises(ValueError, match="not a valid object"):
            _validate_card_data("not a dict", 0)

    def test_missing_front_field(self) -> None:
        """Test that a card missing 'front' raises ValueError."""
        with pytest.raises(ValueError, match="missing the required 'front' field"):
            _validate_card_data({"back": "A"}, 0)

    def test_missing_back_field(self) -> None:
        """Test that a card missing 'back' raises ValueError."""
        with pytest.raises(ValueError, match="missing the required 'back' field"):
            _validate_card_data({"front": "Q"}, 0)

    def test_load_missing_required_field(self) -> None:
        """Test that a card without a 'back' field is rejected."""
        with pytest.raises(ValueError, match="missing the required 'back' field"):
            _validate_card_data({"front": "Q"}, 0)

    def test_empty_front_field(self) -> None:
        """Test that an empty 'front' field raises ValueError."""
        with pytest.raises(ValueError, match="invalid 'front' field"):
            _validate_card_data({"front": "", "back": "A"}, 0)

    def test_empty_back_field(self) -> None:
        """Test that an empty 'back' field raises ValueError."""
        with pytest.raises(ValueError, match="invalid 'back' field"):
            _validate_card_data({"front": "Q", "back": ""}, 0)

    def test_whitespace_only_front(self) -> None:
        """Test that a whitespace-only 'front' field raises ValueError."""
        with pytest.raises(ValueError, match="invalid 'front' field"):
            _validate_card_data({"front": "   ", "back": "A"}, 0)

    def test_non_string_front(self) -> None:
        """Test that a non-string 'front' field raises ValueError."""
        with pytest.raises(ValueError, match="invalid 'front' field"):
            _validate_card_data({"front": 123, "back": "A"}, 0)


class TestExtractCardsList:
    """Tests for the _extract_cards_list function."""

    def test_array_format(self) -> None:
        """Test extraction from array format JSON."""
        data = [{"front": "Q1", "back": "A1"}]
        result = _extract_cards_list(data)
        assert result == [{"front": "Q1", "back": "A1"}]

    def test_object_format(self) -> None:
        """Test extraction from object format JSON with 'cards' key."""
        data = {"cards": [{"front": "Q1", "back": "A1"}]}
        result = _extract_cards_list(data)
        assert result == [{"front": "Q1", "back": "A1"}]

    def test_invalid_format_no_cards_key(self) -> None:
        """Test that an object without 'cards' key raises ValueError."""
        with pytest.raises(ValueError, match="Invalid JSON format"):
            _extract_cards_list({"other": "data"})

    def test_invalid_cards_not_list(self) -> None:
        """Test that 'cards' field that is not a list raises ValueError."""
        with pytest.raises(ValueError, match="must be a list"):
            _extract_cards_list({"cards": "not a list"})

    def test_invalid_format_string(self) -> None:
        """Test that a string input raises ValueError."""
        with pytest.raises(ValueError, match="Invalid JSON format"):
            _extract_cards_list("just a string")


class TestLoadFlashcards:
    """Tests for the load_flashcards function."""

    def _create_temp_json(self, data: object, suffix: str = ".json") -> str:
        """Helper to create a temporary JSON file.

        Args:
            data: The data to write as JSON.
            suffix: File suffix (default .json).

        Returns:
            The path to the temporary file.
        """
        fd, path = tempfile.mkstemp(suffix=suffix)
        with os.fdopen(fd, "w") as f:
            json.dump(data, f)
        return path

    def _create_temp_file_with_content(
        self, content: str, suffix: str = ".json"
    ) -> str:
        """Helper to create a temporary file with raw content.

        Args:
            content: The raw string content to write.
            suffix: File suffix (default .json).

        Returns:
            The path to the temporary file.
        """
        fd, path = tempfile.mkstemp(suffix=suffix)
        with os.fdopen(fd, "w") as f:
            f.write(content)
        return path

    def test_load_valid_flashcards_array(self) -> None:
        """Test loading flashcards from a valid array-format JSON file."""
        data = [
            {"front": "What is Python?", "back": "A programming language"},
            {"front": "What is 2+2?", "back": "4"},
        ]
        path = self._create_temp_json(data)
        try:
            cards = load_flashcards(path)
            assert len(cards) == 2
            assert cards[0].front == "What is Python?"
            assert cards[0].back == "A programming language"
            assert cards[1].front == "What is 2+2?"
            assert cards[1].back == "4"
        finally:
            os.unlink(path)

    def test_load_valid_flashcards_object_format(self) -> None:
        """Test loading flashcards from a valid object-format JSON file."""
        data = {"cards": [{"front": "Q1", "back": "A1"}]}
        path = self._create_temp_json(data)
        try:
            cards = load_flashcards(path)
            assert len(cards) == 1
            assert cards[0].front == "Q1"
        finally:
            os.unlink(path)

    def test_load_invalid_json(self) -> None:
        """Test that malformed JSON triggers a graceful exit."""
        path = self._create_temp_file_with_content("{invalid json content}")
        try:
            with pytest.raises(SystemExit):
                load_flashcards(path)
        finally:
            os.unlink(path)

    def test_load_missing_file(self) -> None:
        """Test that a missing file triggers a graceful exit."""
        with pytest.raises(SystemExit):
            load_flashcards("/nonexistent/path/cards.json")

    def test_load_non_json_file(self) -> None:
        """Test that a non-JSON file extension triggers a graceful exit."""
        fd, path = tempfile.mkstemp(suffix=".txt")
        os.close(fd)
        try:
            with pytest.raises(SystemExit):
                load_flashcards(path)
        finally:
            os.unlink(path)

    def test_load_empty_cards_list(self) -> None:
        """Test that an empty cards list triggers a graceful exit."""
        path = self._create_temp_json([])
        try:
            with pytest.raises(SystemExit):
                load_flashcards(path)
        finally:
            os.unlink(path)

    def test_load_card_missing_back(self) -> None:
        """Test that a card missing the 'back' field triggers a graceful exit."""
        data = [{"front": "Q1"}]
        path = self._create_temp_json(data)
        try:
            with pytest.raises(SystemExit):
                load_flashcards(path)
        finally:
            os.unlink(path)

    def test_load_actual_data_files(self) -> None:
        """Test loading the actual sample data files."""
        cards = load_flashcards("data/glossary.json")
        assert len(cards) == 10
        assert cards[0].front == "API"

    def test_load_actual_python_basics(self) -> None:
        """Test loading the python_basics.json data file."""
        cards = load_flashcards("data/python_basics.json")
        assert len(cards) == 10
        assert cards[0].front == "What keyword is used to define a function in Python?"
