from abc import ABC, abstractmethod

class BaseDetector(ABC):
    @abstractmethod
    def detect(self, text: str) -> dict:
        """Detect sensitive information in the given text.

        Args:
            text (str): The input text to analyze.

        Returns:
            dict: A dictionary containing the name and entity of detected sensitive information.
        """
        pass
    
    @abstractmethod
    def mask(self, text: str) -> str:
        """Mask sensitive information in the given text.

        Args:
            text (str): The input text to mask.

        Returns:
            str: The masked text.
        """
        pass