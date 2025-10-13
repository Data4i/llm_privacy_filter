from pydantic import BaseModel

class MaskState(BaseModel):
    masked_text: str
    text_to_entities: dict[str, list[str]]