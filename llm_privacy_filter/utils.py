def flatten_entity_list(entities: list) -> list:
    return [
        f"{key}.{val}" if isinstance(item, dict) else item
        for item in entities
        for key, vals in (item.items() if isinstance(item, dict) else [(None, None)])
        for val in (vals if isinstance(item, dict) else [item])
    ]

def list_to_str(lst: list) -> str:
    return ", ".join(lst)

def sort_entities(ENTITY_CATEGORY, sensitivity: float) -> str:
    values = []
    for key, value in ENTITY_CATEGORY.items():
        if float(key) >= sensitivity:
            values.extend(value)
            
    entity_list = flatten_entity_list(values)
    entity_string = list_to_str(entity_list)
    return entity_string

