import mcp.types as types

from .utils import make_anki_request

async def list_models() -> list[types.TextContent]:
    result = await make_anki_request("modelNames")

    if result["success"]:
        models = result["result"]
        return [
            types.TextContent(
                type="text",
                text=f"Available note models in Anki ({len(models)}):\n" + "\n".join(f"- {model}" for model in models),
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=f"Failed to retrieve models: {result['error']}",
            )
        ]
