"""Tests for the search syntax documentation resource."""

from anki_mcp.resources.search_syntax import get_search_syntax_docs


def test_get_search_syntax_docs_returns_string():
    """Test that the function returns a string."""
    docs = get_search_syntax_docs()
    assert isinstance(docs, str)
    assert len(docs) > 0


def test_search_syntax_docs_contains_key_sections():
    """Test that documentation contains all major sections."""
    docs = get_search_syntax_docs()

    expected_sections = [
        "# Anki Search Syntax Reference",
        "## BASIC QUERY SYNTAX",
        "## FIELD SEARCH",
        "## TAGS, DECKS, AND CARDS",
        "## CARD STATE",
        "## CARD PROPERTIES",
        "## TIMING",
        "## IDS",
        "## CUSTOM DATA",
        "## ADVANCED EXAMPLES",
        "## TIPS",
    ]

    for section in expected_sections:
        assert section in docs, f"Missing section: {section}"


def test_search_syntax_docs_contains_examples():
    """Test that documentation includes practical examples."""
    docs = get_search_syntax_docs()

    # Check for various example patterns
    assert "tag:name" in docs
    assert "deck:name" in docs
    assert "is:due" in docs
    assert "prop:ivl>=" in docs
    assert "field:term" in docs
    assert "added:" in docs
    assert "rated:" in docs


def test_search_syntax_docs_contains_operators():
    """Test that documentation covers query operators."""
    docs = get_search_syntax_docs()

    operators = [
        "or",
        "-",  # negation
        "*",  # wildcard
        ":",  # field separator
    ]

    for operator in operators:
        assert operator in docs


def test_search_syntax_docs_references_official_docs():
    """Test that documentation links to official Anki docs."""
    docs = get_search_syntax_docs()
    assert "https://docs.ankiweb.net/searching.html" in docs
