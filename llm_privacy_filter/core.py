from .pdet_utils import sort_entities
from .pdet import PDET
from .prompt_template import MASKING_PROMPT_TEMPLATE
from .privacy_states import MaskState
from .providers import get_llm
from typing import Optional
import pathlib

from langchain_core.prompts import PromptTemplate

class Masker:
    def __init__(
        self, 
        model: str = "gpt-oss:120b-cloud", 
        model_provider: str = "ollama",
        path: str | pathlib.Path | None = None
    ):    
        self.model = model
        self.model_provider = model_provider
        self.llm = get_llm(
            model=self.model, 
            provider=self.model_provider, 
            temperature=0.0
        )
        self.path = path

    def mask_text(self, text: str | None, sensitivity: float = 1.0) -> dict:
        """Masks sensitive information in the text.

        Args:
            text (str): The input text to be masked.
            sensitivity (float, optional): The sensitivity threshold for masking. Defaults to 1.0.

        Returns:
            dict: A dictionary containing the masked text and the mapping of text segments to their associated entities.
        """
        if self.path == None and text is None:
            raise ValueError("Either 'path' or 'text' must be provided.")
        
        prompt = PromptTemplate.from_template(MASKING_PROMPT_TEMPLATE)
        entities = sort_entities(PDET, sensitivity)
        masked_llm = self.llm.with_structured_output(MaskState)
        chain = prompt | masked_llm
        result: MaskState = chain.invoke({"text": text, "entities": entities})
        return result.masked_text, result.text_to_entities
    
    def generalize_text(self, text: str, sensitivity: float = 1.0) -> str:
        # masked_text, _ = self.mask_text(text, sensitivity)
        # return masked_text
        pass           