"""Anki search syntax documentation resource."""

SEARCH_SYNTAX_DOCS = """# Anki Search Syntax Reference

This comprehensive guide covers the query syntax for searching cards and notes in Anki.

## BASIC QUERY SYNTAX

**Combining Terms:**
- `term1 term2`: Implicit AND - matches items containing both terms
- `term1 or term2`: Matches items containing either term
- `-term`: Negation - excludes items containing this term
- `"exact phrase"`: Exact match for multi-word phrases
- `t*rm`: Wildcard matching (matches "term", "transform", etc.)
- `(term1 or term2) term3`: Grouping for precedence control
- `w:term`: Word boundary match - matches whole words only

**Examples:**
- `cat dog`: Cards with both "cat" AND "dog"
- `cat or dog`: Cards with either "cat" OR "dog"
- `cat -dog`: Cards with "cat" but not "dog"
- `"the cat"`: Cards with exact phrase "the cat"
- `cat*`: Cards with "cat", "cats", "category", etc.

## FIELD SEARCH

**Field-Specific Searches:**
- `field:term`: Exact match in the specified field
- `field:*term*`: Contains match (partial matching)
- `field:`: Empty field (field has no content)
- `field:_*`: Non-empty field (field has any content)
- `fr*:term`: Fields starting with "fr" (e.g., "french", "from")

**Examples:**
- `Front:bonjour`: Cards where Front field exactly matches "bonjour"
- `Back:*hello*`: Cards where Back field contains "hello"
- `Tags:`: Cards with empty Tags field
- `Example:_*`: Cards where Example field is not empty

## TAGS, DECKS, AND CARDS

**Tags:**
- `tag:name`: Match tag and all subtags (hierarchical)
- `tag:none`: Cards with no tags
- `tag:re:^parent$`: Regex tag match (exact "parent" tag only)
- `-tag:name`: Exclude cards with this tag

**Decks:**
- `deck:name`: Match deck and all subdecks
- `deck:name -deck:name::*`: Match deck but exclude subdecks
- `deck:"name with spaces"`: Deck names containing spaces
- `deck:current`: Current deck
- `deck:filtered`: All filtered decks

**Card Types:**
- `card:name`: Card type by template name
- `card:1`: Card type by number (1 = first template)
- `note:name`: Note type (e.g., "Basic", "Cloze")

**Examples:**
- `tag:language::french`: All cards tagged with french (including subtags)
- `deck:Spanish -deck:Spanish::Verbs::*`: Spanish deck but not Verbs subdecks
- `note:Cloze`: All cloze deletion cards

## CARD STATE

**Review State:**
- `is:due`: Cards due for review now
- `is:new`: New (unseen) cards
- `is:learn`: Cards in learning phase
- `is:review`: Cards in review phase
- `is:suspended`: Suspended cards

**Buried Cards:**
- `is:buried`: All buried cards
- `is:buried-sibling`: Buried sibling cards
- `is:buried-manually`: Manually buried cards

**Flags:**
- `flag:1`: Red flag
- `flag:2`: Orange flag
- `flag:3`: Green flag
- `flag:4`: Blue flag
- `flag:5`: Pink flag
- `flag:6`: Turquoise flag
- `flag:7`: Purple flag

**Examples:**
- `is:due deck:Spanish`: Due Spanish cards
- `is:suspended tag:difficult`: Suspended cards tagged "difficult"
- `flag:1 is:review`: Flagged red cards in review

## CARD PROPERTIES

**Intervals and Scheduling:**
- `prop:ivl>=10`: Interval of 10 days or more
- `prop:ivl<=30`: Interval of 30 days or less
- `prop:due=1`: Due tomorrow (relative to today)
- `prop:due=-1`: Due yesterday (overdue by 1 day)
- `prop:due>-7`: Due within the last week or future

**Performance Metrics:**
- `prop:reps<10`: Review count less than 10
- `prop:lapses>3`: Lapsed more than 3 times
- `prop:ease!=2.5`: Ease factor not equal to 2.5 (default)

**FSRS Properties (if using FSRS scheduler):**
- `prop:s>21`: Stability greater than 21 days
- `prop:d>0.3`: Difficulty greater than 0.3
- `prop:r<0.9`: Retrievability less than 0.9

**Examples:**
- `prop:ivl>=365`: Cards with interval of 1+ years
- `prop:ease<2.0`: Cards with low ease factor
- `prop:lapses>5 is:review`: Leeches (many lapses) in review

## TIMING

**Card History:**
- `added:7`: Added in the last 7 days
- `edited:n`: Edited in the last n days
- `rated:7`: Reviewed in the last 7 days
- `rated:7:1`: Reviewed with rating 1 (Again) in last 7 days
- `prop:rated=-7`: Answered exactly 7 days ago
- `introduced:365`: First answered within the last 365 days

**Rating Values:**
- `1`: Again (failed)
- `2`: Hard
- `3`: Good
- `4`: Easy

**Examples:**
- `added:1`: Cards added today
- `rated:7:1 deck:Vocabulary`: Vocab cards failed in last week
- `edited:30`: Cards modified in last month

## IDS

**Direct ID Searches:**
- `nid:123`: Note ID 123
- `cid:123,456`: Card IDs 123 and 456
- `mid:789`: Model (note type) ID 789

**Examples:**
- `nid:1234567890123`: Specific note by ID
- `cid:1234567890123,1234567890124`: Two specific cards

## CUSTOM DATA

**Custom Data Properties (requires Anki add-ons):**
- `has-cd:v`: Has custom data property named "v"
- `prop:cdn:d>5`: Numeric custom data property "d" greater than 5
- `prop:cds:v=reschedule`: String custom data property "v" equals "reschedule"

## ADVANCED EXAMPLES

**Complex Queries:**
- `deck:Spanish tag:verb is:due prop:ivl<30`: Due Spanish verb cards with interval less than 30 days
- `(is:due or flag:1) -is:suspended`: Due or flagged cards that aren't suspended
- `rated:7:1 -rated:1:3`: Cards failed in last week but not passed today
- `note:Cloze -deck:Archived is:review prop:ease>2.5`: Well-performing cloze cards not in archive

**Finding Problem Cards:**
- `prop:lapses>5 is:review`: Leeches (cards you keep failing)
- `prop:ease<2.0 is:review`: Cards with low ease factor
- `rated:30:1 prop:ivl>30`: Mature cards failed recently
- `is:due prop:ivl>365 -is:suspended`: Due cards with long intervals (possible scheduling issues)

## TIPS

1. **Case Sensitivity**: Most searches are case-insensitive unless using regex
2. **Wildcards**: Use `*` for flexible matching, but be aware it may slow searches
3. **Parentheses**: Use for complex boolean logic and grouping
4. **Regex**: Available for advanced pattern matching with `re:` prefix
5. **Negative Searches**: `-` is powerful for excluding unwanted results
6. **Field Searches**: Most precise way to find specific content
7. **Testing**: Start with simple queries and build complexity gradually

## REFERENCE LINKS

For the most up-to-date information, see the official Anki documentation:
https://docs.ankiweb.net/searching.html
"""


def get_search_syntax_docs() -> str:
    """
    Returns comprehensive documentation for Anki's search syntax.

    This resource provides a complete reference guide for querying cards and notes
    in Anki, including basic syntax, field searches, tags, decks, card states,
    properties, timing, IDs, and advanced query examples.

    Returns:
        str: The complete search syntax documentation in markdown format
    """
    return SEARCH_SYNTAX_DOCS
