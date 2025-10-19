def flatten_entity_list(entities: list) -> list:
    """Flattens a list of entities, which may be nested dictionaries or lists.

    Args:
        entities (list): The list of entities to flatten.

    Returns:
        list: A flattened list of entities.
    """
    return [
        f"{key}.{val}" if isinstance(item, dict) else item
        for item in entities
        for key, vals in (item.items() if isinstance(item, dict) else [(None, None)])
        for val in (vals if isinstance(item, dict) else [item])
    ]

def list_to_str(lst: list) -> str:
    """Converts a list of strings to a single string.

    Args:
        lst (list): The list of strings to convert.

    Returns:
        str: A single string with list elements joined by commas.
    """
    return ", ".join(lst)

def sort_entities(ENTITY_CATEGORY, sensitivity: float) -> str:
    """Sorts entities based on their sensitivity.

    Args:
        ENTITY_CATEGORY (dict): The entity category mapping.
        sensitivity (float): The sensitivity threshold.

    Returns:
        str: A string representation of the sorted entities.
    """
    values = []
    for key, value in ENTITY_CATEGORY.items():
        if float(key) >= sensitivity:
            values.extend(value)
            
    entity_list = flatten_entity_list(values)
    entity_string = list_to_str(entity_list)
    return entity_string

