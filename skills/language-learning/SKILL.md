---
description: Guide for creating effective language learning flashcards in Anki using spaced repetition best practices
---

# Language Learning Flashcard Creation Guide

Use this guide when helping users create language learning flashcards with the Anki MCP tools.

## Workflow

1. **Check Collection First**: Always use `get-collection-overview` to see available note types, fields, and decks
2. **Generate Examples**: Create example sentences/words appropriate for the user's level
3. **Show for Review**: Present examples to user as a numbered list for confirmation
4. **Add to Anki**: Use `add-or-update-notes` to create confirmed cards
5. **Tag Appropriately**: Tag new cards (e.g., "needs-review") so users can verify them

## Card Quality Guidelines

### Content
- Keep sentences **short and natural** (ideally under 10 words)
- Use **conversational, everyday language** appropriate for the proficiency level
- Create a **mix**: ~30% individual words, ~70% short example sentences
- For cloze cards: Make **ONE cloze deletion per card** (on the key word/phrase being learned)
- Include **gender markers** (el/la, der/die/das, le/la, etc.) where applicable in the language

### Note Type Variety
- Use different note types from the collection (cloze, basic front/back, etc.)
- Match note type to content: cloze for context, basic for vocabulary
- Check what note types are available with `get-collection-overview` first

### Examples of Good Cards

**Cloze Example:**
- Target Language: "He {{c1::trencat}} el got sense voler."
- Source Language: "I broke the glass by accident."
- Description: "trencar (to break) - common irregular verb"

**Basic Vocabulary:**
- Front: "to wander alone"
- Back: "deambular sol"
- Word Type: "verb"

## What to Avoid

- Long, complex sentences that are hard to remember
- Multiple cloze deletions in one card (splits focus)
- Formal or literary language (unless specifically requested)
- Content that's too simple or too advanced for the user's level

## Proficiency Level Guidelines

- **A1/A2**: Very basic vocabulary, present tense, simple sentences
- **B1/B2**: Everyday situations, mixed tenses, idiomatic expressions
- **C1/C2**: Complex grammar, nuanced vocabulary, subjunctive moods

## Remember

Always adapt to the user's:
- Available note types (from collection overview)
- Target proficiency level
- Specific learning goals (vocabulary, grammar, etc.)
- Preferred deck structure

The goal is creating effective, memorable cards that work with spaced repetition - not perfect translations or comprehensive grammar lessons.
