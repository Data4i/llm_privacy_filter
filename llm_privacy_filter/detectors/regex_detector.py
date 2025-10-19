from .base import BaseDetector

class RegexDetector(BaseDetector):
    def detect(self, text: str) -> dict:
        # Implementation for detecting sensitive information using regex
        pass
    
    def mask(self, text: str) -> str:
        # Implementation for masking sensitive information using regex
        pass
