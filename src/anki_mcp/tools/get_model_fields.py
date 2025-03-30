import mcp.types as types

from .utils import make_anki_request


async def get_model_fields(model_name: str) -> list[types.TextContent]:
    # Get field names
    names_result = await make_anki_request("modelFieldNames", modelName=model_name)

    # Get field descriptions
    descriptions_result = await make_anki_request("modelFieldDescriptions", modelName=model_name)

    if names_result["success"] and descriptions_result["success"]:
        field_names = names_result["result"]
        field_descriptions = descriptions_result["result"]

        # Combine fields and descriptions
        field_info = []
        for i, (name, description) in enumerate(zip(field_names, field_descriptions)):
            desc_text = f": {description}" if description else ""
            field_info.append(f"- {name}{desc_text}")

        return [
            types.TextContent(
                type="text",
                text=f"Fields for model '{model_name}' ({len(field_names)}):\n" + "\n".join(field_info),
            )
        ]
    elif not names_result["success"]:
        return [
            types.TextContent(
                type="text",
                text=f"Failed to retrieve field names: {names_result['error']}",
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=f"Failed to retrieve field descriptions: {descriptions_result['error']}",
            )
        ]
