from pydantic import BaseModel

class MaskState(BaseModel):
    """Represents the state of a text masking operation.

    Attributes:
        masked_text (str): The masked text.
        text_to_entities (dict[str, list[str]]): A mapping from text segments to their associated entities.
    """
    masked_text: str
    text_to_entities: dict[str, list[str]]