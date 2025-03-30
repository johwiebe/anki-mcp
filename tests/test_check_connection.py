import pytest
from anki.tools.check_connection import check_connection


@pytest.mark.asyncio
async def test_check_connection_succeeds(monkeypatch):
    async def mockreturn(*args, **kwargs):
        return {"success": True, "result": "5.0.0"}
    
    monkeypatch.setattr("anki.tools.check_connection.make_anki_request", mockreturn)

    result = await check_connection()
    assert result[0].text == "Connected to AnkiConnect v5.0.0"


@pytest.mark.asyncio
async def test_check_connection_fails(monkeypatch):
    async def mockreturn(*args, **kwargs):
        return {"success": False, "error": "Could not connect to Anki"}
    
    monkeypatch.setattr("anki.tools.check_connection.make_anki_request", mockreturn)

    result = await check_connection()
    assert result[0].text == "Failed to connect to AnkiConnect: Could not connect to Anki"
