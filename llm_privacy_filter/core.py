from utils import sort_entities
from pdet import PDET
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from prompt_template import MASKING_PROMPT_TEMPLATE
from privacy_states import MaskState

class Masker:
    def __init__(
        self, 
        model: str = "gpt-oss:120b-cloud", 
        model_provider: str = "ollama", 
    ):    
        self.model = model
        self.model_provider = model_provider
        self.llm = init_chat_model(
            model=self.model, 
            model_provider=self.model_provider, 
            temperature=0.0
        )

    def mask_text(self, text: str, sensitivity: float = 1.0) -> dict:
        prompt = PromptTemplate.from_template(MASKING_PROMPT_TEMPLATE)
        entities = sort_entities(PDET, sensitivity)
        masked_llm = self.llm.with_structured_output(MaskState)
        chain = prompt | masked_llm
        result: MaskState = chain.invoke({"text": text, "entities": entities})
        return result.masked_text, result.text_to_entities
    
    def generalize_text(self, text: str, sensitivity: float = 1.0) -> str:
        masked_text, _ = self.mask_text(text, sensitivity)
        return masked_text
           
           

