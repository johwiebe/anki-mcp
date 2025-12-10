"""Tests for the language learning prompt."""

import pytest
from anki_mcp.prompts.language_learning import (
    get_create_language_cards_prompt,
    create_language_cards_prompt,
)


def test_get_create_language_cards_prompt_returns_string():
    """Test that the prompt function returns a string."""
    prompt = get_create_language_cards_prompt(
        target_language="Spanish",
        focus="common verbs"
    )
    assert isinstance(prompt, str)
    assert len(prompt) > 0


def test_prompt_includes_target_language():
    """Test that the prompt includes the target language."""
    prompt = get_create_language_cards_prompt(
        target_language="French",
        focus="food vocabulary"
    )
    assert "French" in prompt


def test_prompt_includes_focus():
    """Test that the prompt includes the focus area."""
    prompt = get_create_language_cards_prompt(
        target_language="German",
        focus="past tense verbs"
    )
    assert "past tense verbs" in prompt


def test_prompt_includes_proficiency_level():
    """Test that the prompt includes the proficiency level."""
    prompt = get_create_language_cards_prompt(
        target_language="Italian",
        focus="greetings",
        proficiency_level="A2"
    )
    assert "A2" in prompt


def test_prompt_uses_default_values():
    """Test that the prompt uses correct default values."""
    prompt = get_create_language_cards_prompt(
        target_language="Spanish",
        focus="verbs"
    )
    # Check defaults
    assert "English" in prompt  # default source_language
    assert "B1" in prompt  # default proficiency_level
    assert "Default" in prompt  # default target_deck


def test_prompt_custom_source_language():
    """Test that custom source language is used."""
    prompt = get_create_language_cards_prompt(
        target_language="Spanish",
        focus="verbs",
        source_language="Portuguese"
    )
    assert "Portuguese" in prompt


def test_prompt_custom_target_deck():
    """Test that custom target deck is used."""
    prompt = get_create_language_cards_prompt(
        target_language="Japanese",
        focus="kanji",
        target_deck="MyDeck"
    )
    assert "MyDeck" in prompt


def test_prompt_contains_workflow_section():
    """Test that the prompt includes workflow guidance."""
    prompt = get_create_language_cards_prompt(
        target_language="Spanish",
        focus="vocabulary"
    )
    assert "Workflow" in prompt
    assert "get-collection-overview" in prompt
    assert "add-or-update-notes" in prompt


def test_prompt_contains_guidelines():
    """Test that the prompt includes card creation guidelines."""
    prompt = get_create_language_cards_prompt(
        target_language="Spanish",
        focus="vocabulary"
    )
    assert "Guidelines" in prompt
    assert "cloze" in prompt.lower()
    assert "short" in prompt.lower()


def test_prompt_mentions_tagging():
    """Test that the prompt mentions tagging cards for review."""
    prompt = get_create_language_cards_prompt(
        target_language="Spanish",
        focus="vocabulary"
    )
    assert "needs-review" in prompt or "need-review" in prompt or "tag" in prompt.lower()


def test_create_language_cards_prompt_direct():
    """Test the internal create_language_cards_prompt function."""
    prompt = create_language_cards_prompt(
        target_language="Mandarin",
        focus="numbers",
        source_language="English",
        proficiency_level="A1",
        target_deck="Chinese"
    )
    assert "Mandarin" in prompt
    assert "numbers" in prompt
    assert "A1" in prompt
    assert "Chinese" in prompt
