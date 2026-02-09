"""Data loader module for loading and validating flashcard data from JSON files."""

import json
import sys
from pathlib import Path
from typing import Any


class Flashcard:
    """Represents a single flashcard with a front and back side."""

    def __init__(self, front: str, back: str) -> None:
        """Initialize a Flashcard.

        Args:
            front: The question or prompt displayed to the user.
            back: The correct answer.
        """
        self.front: str = front
        self.back: str = back

    def __repr__(self) -> str:
        """Return a string representation of the flashcard."""
        return f"Flashcard(front='{self.front}', back='{self.back}')"

    def __eq__(self, other: object) -> bool:
        """Check equality between two flashcards."""
        if not isinstance(other, Flashcard):
            return NotImplemented
        return self.front == other.front and self.back == other.back


def _validate_card_data(card: Any, index: int) -> None:
    """Validate that a card dictionary has the required fields.

    Args:
        card: The card data to validate.
        index: The index of the card in the list (for error messages).

    Raises:
        ValueError: If the card is missing required fields or has invalid types.
    """
    if not isinstance(card, dict):
        raise ValueError(
            f"Card at index {index} is not a valid object. "
            f"Each card must be a JSON object with 'front' and 'back' fields."
        )

    if "front" not in card:
        raise ValueError(
            f"Card at index {index} is missing the required 'front' field."
        )

    if "back" not in card:
        raise ValueError(f"Card at index {index} is missing the required 'back' field.")

    if not isinstance(card["front"], str) or not card["front"].strip():
        raise ValueError(
            f"Card at index {index} has an invalid 'front' field. "
            f"It must be a non-empty string."
        )

    if not isinstance(card["back"], str) or not card["back"].strip():
        raise ValueError(
            f"Card at index {index} has an invalid 'back' field. "
            f"It must be a non-empty string."
        )


def _extract_cards_list(data: Any) -> list[dict[str, str]]:
    """Extract the list of card dictionaries from parsed JSON data.

    Supports two formats:
        - Array format: [{"front": "...", "back": "..."}, ...]
        - Object format: {"cards": [{"front": "...", "back": "..."}, ...]}

    Args:
        data: The parsed JSON data.

    Returns:
        A list of card dictionaries.

    Raises:
        ValueError: If the data format is not recognized.
    """
    if isinstance(data, list):
        return data
    elif isinstance(data, dict) and "cards" in data:
        if not isinstance(data["cards"], list):
            raise ValueError("The 'cards' field must be a list of flashcard objects.")
        return data["cards"]
    else:
        raise ValueError(
            "Invalid JSON format. Expected either:\n"
            '  - An array of objects: [{"front": "...", "back": "..."}]\n'
            '  - An object with a "cards" key: {"cards": [...]}'
        )


def load_flashcards(file_path: str) -> list[Flashcard]:
    """Load and validate flashcards from a JSON file.

    Args:
        file_path: Path to the JSON file containing flashcard data.

    Returns:
        A list of validated Flashcard objects.

    Raises:
        SystemExit: If the file cannot be loaded or validated.
    """
    path = Path(file_path)

    if not path.exists():
        print(f"Error: File not found: '{file_path}'")
        print("Please check the file path and try again.")
        sys.exit(1)

    if not path.suffix.lower() == ".json":
        print(f"Error: '{file_path}' is not a JSON file.")
        print("Please provide a file with a .json extension.")
        sys.exit(1)

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: The file '{file_path}' contains invalid JSON.")
        print(f"Details: {e}")
        sys.exit(1)

    try:
        cards_data = _extract_cards_list(data)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if not cards_data:
        print("Error: The flashcard file contains no cards.")
        sys.exit(1)

    flashcards: list[Flashcard] = []
    for i, card in enumerate(cards_data):
        try:
            _validate_card_data(card, i)
            flashcards.append(Flashcard(front=card["front"], back=card["back"]))
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

    return flashcards
