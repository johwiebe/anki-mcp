import pytest

from anki_mcp.tools.add_or_update_notes import Note, add_or_update_notes, update_note, add_note


@pytest.mark.asyncio
async def test_add_note_success(monkeypatch):
    # Prepare test data
    test_note = Note(
        name="Test Note",
        id=None,
        deck="Test Deck",
        model="Basic",
        fields={"Front": "Test Question", "Back": "Test Answer"},
        tags=["test", "example"]
    )
    
    # Mock successful response
    async def mock_anki_request(action, **kwargs):
        assert action == "addNote"
        assert kwargs["note"]["deckName"] == "Test Deck"
        assert kwargs["note"]["modelName"] == "Basic"
        assert kwargs["note"]["fields"] == {"Front": "Test Question", "Back": "Test Answer"}
        assert kwargs["note"]["tags"] == ["test", "example"]
        return {"success": True, "result": 1234}
    
    monkeypatch.setattr("anki_mcp.tools.add_or_update_notes.make_anki_request", mock_anki_request)
    
    result = await add_note(test_note)
    
    assert result["success"] is True
    assert result["result"] == 1234


@pytest.mark.asyncio
async def test_add_note_no_fields_failure(monkeypatch):
    # Prepare test data with empty fields
    test_note = Note(
        name="Empty Note",
        id=None,
        deck="Test Deck",
        model="Basic",
        fields={},
        tags=["test"]
    )
    
    # Mock should not be called
    async def mock_anki_request(action, **kwargs):
        pytest.fail("make_anki_request should not be called")
    
    monkeypatch.setattr("anki_mcp.tools.add_or_update_notes.make_anki_request", mock_anki_request)
    
    result = await add_note(test_note)
    
    assert result["success"] is False
    assert result["error"] == "Note has no fields"


@pytest.mark.asyncio
async def test_add_note_failure(monkeypatch):
    # Prepare test data
    test_note = Note(
        name="Test Note",
        id=None,
        deck="Test Deck",
        model="Basic",
        fields={"Front": "Test Question", "Back": "Test Answer"},
        tags=None
    )
    
    # Mock failure response
    async def mock_anki_request(action, **kwargs):
        assert action == "addNote"
        return {"success": False, "error": "Model not found"}
    
    monkeypatch.setattr("anki_mcp.tools.add_or_update_notes.make_anki_request", mock_anki_request)
    
    result = await add_note(test_note)
    
    assert result["success"] is False
    assert result["error"] == "Model not found"


@pytest.mark.asyncio
async def test_update_note_success(monkeypatch):
    # Prepare test data
    test_note = Note(
        name="Test Note",
        id=5678,
        deck="Test Deck",
        model="Basic",
        fields={"Front": "Updated Question", "Back": "Updated Answer"},
        tags=["updated", "test"]
    )
    
    # Mock successful response
    async def mock_anki_request(action, **kwargs):
        assert action == "updateNote"
        assert kwargs["note"]["id"] == 5678
        assert kwargs["note"]["fields"] == {"Front": "Updated Question", "Back": "Updated Answer"}
        assert kwargs["note"]["tags"] == ["updated", "test"]
        return {"success": True, "result": None}
    
    monkeypatch.setattr("anki_mcp.tools.add_or_update_notes.make_anki_request", mock_anki_request)
    
    result = await update_note(test_note)
    
    assert result["success"] is True


@pytest.mark.asyncio
async def test_update_note_fields_only(monkeypatch):
    # Prepare test data with fields only
    test_note = Note(
        name="Fields Only Note",
        id=5678,
        deck="Test Deck",
        model="Basic",
        fields={"Front": "Updated Question", "Back": "Updated Answer"},
        tags=None
    )
    
    # Mock successful response
    async def mock_anki_request(action, **kwargs):
        assert action == "updateNote"
        assert kwargs["note"]["id"] == 5678
        assert kwargs["note"]["fields"] == {"Front": "Updated Question", "Back": "Updated Answer"}
        assert "tags" not in kwargs["note"]
        return {"success": True, "result": None}
    
    monkeypatch.setattr("anki_mcp.tools.add_or_update_notes.make_anki_request", mock_anki_request)
    
    result = await update_note(test_note)
    
    assert result["success"] is True


@pytest.mark.asyncio
async def test_update_note_tags_only(monkeypatch):
    # Prepare test data with tags only
    test_note = Note(
        name="Tags Only Note",
        id=5678,
        deck="Test Deck",
        model="Basic",
        fields={},
        tags=["updated", "test"]
    )
    
    # Mock successful response
    async def mock_anki_request(action, **kwargs):
        assert action == "updateNote"
        assert kwargs["note"]["id"] == 5678
        assert "fields" not in kwargs["note"]
        assert kwargs["note"]["tags"] == ["updated", "test"]
        return {"success": True, "result": None}
    
    monkeypatch.setattr("anki_mcp.tools.add_or_update_notes.make_anki_request", mock_anki_request)
    
    result = await update_note(test_note)
    
    assert result["success"] is True


@pytest.mark.asyncio
async def test_update_note_empty_failure(monkeypatch):
    # Prepare test data with empty fields and no tags
    test_note = Note(
        name="Empty Note",
        id=5678,
        deck="Test Deck",
        model="Basic",
        fields={},
        tags=None
    )
    
    # Mock should not be called
    async def mock_anki_request(action, **kwargs):
        pytest.fail("make_anki_request should not be called")
    
    monkeypatch.setattr("anki_mcp.tools.add_or_update_notes.make_anki_request", mock_anki_request)
    
    result = await update_note(test_note)
    
    assert result["success"] is False
    assert "Either fields or tags must be provided" in result["error"]


@pytest.mark.asyncio
async def test_update_note_failure(monkeypatch):
    # Prepare test data
    test_note = Note(
        name="Test Note",
        id=5678,
        deck="Test Deck",
        model="Basic",
        fields={"Front": "Updated Question", "Back": "Updated Answer"},
        tags=["updated", "test"]
    )
    
    # Mock failure response
    async def mock_anki_request(action, **kwargs):
        assert action == "updateNote"
        return {"success": False, "error": "Note not found"}
    
    monkeypatch.setattr("anki_mcp.tools.add_or_update_notes.make_anki_request", mock_anki_request)
    
    result = await update_note(test_note)
    
    assert result["success"] is False
    assert result["error"] == "Note not found"


@pytest.mark.asyncio
async def test_add_or_update_notes_empty_list():
    # Test with empty list
    with pytest.raises(ValueError, match="No notes provided"):
        await add_or_update_notes([])


@pytest.mark.asyncio
async def test_add_or_update_notes_all_success(monkeypatch):
    # Prepare test data
    test_notes = [
        Note(
            name="New Note",
            id=None,
            deck="Test Deck",
            model="Basic",
            fields={"Front": "Question 1", "Back": "Answer 1"},
            tags=["test"]
        ),
        Note(
            name="Existing Note",
            id=5678,
            deck="Test Deck",
            model="Basic",
            fields={"Front": "Question 2", "Back": "Answer 2"},
            tags=["test", "updated"]
        )
    ]
    
    # Mock successful responses
    async def mock_add_note(note):
        if note.id is None:
            return {"success": True, "result": 1234}
        else:
            pytest.fail("add_note should not be called for notes with IDs")
    
    async def mock_update_note(note):
        if note.id is not None:
            return {"success": True, "result": None}
        else:
            pytest.fail("update_note should not be called for notes without IDs")
    
    monkeypatch.setattr("anki_mcp.tools.add_or_update_notes.add_note", mock_add_note)
    monkeypatch.setattr("anki_mcp.tools.add_or_update_notes.update_note", mock_update_note)
    
    result = await add_or_update_notes(test_notes)
    
    assert len(result) == 1
    text_content = result[0].text
    
    assert "Added note 'New Note' with ID 1234" in text_content
    assert "Updated note 'Existing Note' with ID 5678" in text_content


@pytest.mark.asyncio
async def test_add_or_update_notes_mixed_results(monkeypatch):
    # Prepare test data
    test_notes = [
        Note(
            name="Success Note",
            id=None,
            deck="Test Deck",
            model="Basic",
            fields={"Front": "Question 1", "Back": "Answer 1"},
            tags=["test"]
        ),
        Note(
            name="Failed Note",
            id=None,
            deck="Test Deck",
            model="Invalid",
            fields={"Front": "Question 2", "Back": "Answer 2"},
            tags=["test"]
        ),
        Note(
            name="Success Update",
            id=5678,
            deck="Test Deck",
            model="Basic",
            fields={"Front": "Question 3", "Back": "Answer 3"},
            tags=["test", "updated"]
        )
    ]
    
    # Mock mixed responses
    async def mock_add_note(note):
        if note.name == "Success Note":
            return {"success": True, "result": 1234}
        else:
            return {"success": False, "error": "Model not found"}
    
    async def mock_update_note(note):
        return {"success": True, "result": None}
    
    monkeypatch.setattr("anki_mcp.tools.add_or_update_notes.add_note", mock_add_note)
    monkeypatch.setattr("anki_mcp.tools.add_or_update_notes.update_note", mock_update_note)
    
    result = await add_or_update_notes(test_notes)
    
    assert len(result) == 1
    text_content = result[0].text
    
    assert "Added note 'Success Note' with ID 1234" in text_content
    assert "Failed to add note 'Failed Note': Model not found" in text_content
    assert "Updated note 'Success Update' with ID 5678" in text_content


@pytest.mark.asyncio
async def test_add_or_update_notes_all_failure(monkeypatch):
    # Prepare test data
    test_notes = [
        Note(
            name="Failed Note 1",
            id=None,
            deck="Test Deck",
            model="Invalid",
            fields={"Front": "Question 1", "Back": "Answer 1"},
            tags=["test"]
        ),
        Note(
            name="Failed Note 2",
            id=9999,
            deck="Test Deck",
            model="Basic",
            fields={"Front": "Question 2"},
            tags=["test"]
        )
    ]
    
    # Mock all failure responses
    async def mock_add_note(note):
        return {"success": False, "error": "Model not found"}
    
    async def mock_update_note(note):
        return {"success": False, "error": "Note not found"}
    
    monkeypatch.setattr("anki_mcp.tools.add_or_update_notes.add_note", mock_add_note)
    monkeypatch.setattr("anki_mcp.tools.add_or_update_notes.update_note", mock_update_note)
    
    result = await add_or_update_notes(test_notes)
    
    assert len(result) == 1
    text_content = result[0].text
    
    assert "Failed to add note 'Failed Note 1': Model not found" in text_content
    assert "Failed to update note 'Failed Note 2' with ID 9999: Note not found" in text_content