import mcp.types as types

from .utils import make_anki_request

async def get_collection_overview() -> list[types.TextContent]:
    """
    Get comprehensive information about the Anki collection:
    - Available decks
    - Available note models
    - Fields for each model
    
    Returns a list of TextContent objects with formatted information.
    """
    results = []
    
    # Get decks
    decks_result = await make_anki_request("deckNames")
    if not decks_result["success"]:
        return [types.TextContent(
            type="text", 
            text=f"\nFailed to retrieve decks: {decks_result['error']}"
        )]
        
    decks = decks_result["result"]
    results.append(
        types.TextContent(
            type="text",
            text=f"\nAvailable decks in Anki ({len(decks)}):\n" + 
                 "\n".join(f"- {deck}" for deck in decks)
        )
    )
    
    # Get models
    models_result = await make_anki_request("modelNames")
    if not models_result["success"]:
        return [types.TextContent(
            type="text",
            text=f"\nFailed to retrieve models: {models_result['error']}"
        )]
        
    models = models_result["result"]
    results.append(
        types.TextContent(
            type="text",
            text=f"\nAvailable note models in Anki ({len(models)}):\n" + 
                 "\n".join(f"- {model}" for model in models)
        )
    )
    
    # Get fields for each model
    for model_name in models:
        # Get field names
        names_result = await make_anki_request("modelFieldNames", modelName=model_name)
        
        # Get field descriptions
        descriptions_result = await make_anki_request("modelFieldDescriptions", modelName=model_name)
        
        if names_result["success"] and descriptions_result["success"]:
            field_names = names_result["result"]
            field_descriptions = descriptions_result["result"]
            
            # Combine fields and descriptions
            field_info = []
            for name, description in zip(field_names, field_descriptions):
                desc_text = f": {description}" if description else ""
                field_info.append(f"  - {name}{desc_text}")
            
            results.append(
                types.TextContent(
                    type="text",
                    text=f"\nFields for model '{model_name}' ({len(field_names)}):\n" + 
                         "\n".join(field_info)
                )
            )
        elif not names_result["success"]:
            results.append(
                types.TextContent(
                    type="text",
                    text=f"\nFailed to retrieve field names for '{model_name}': {names_result['error']}"
                )
            )
        else:
            results.append(
                types.TextContent(
                    type="text",
                    text=f"\nFailed to retrieve field descriptions for '{model_name}': {descriptions_result['error']}"
                )
            )
    
    return results 