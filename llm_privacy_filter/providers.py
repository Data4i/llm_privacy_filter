from langchain.chat_models import init_chat_model

def get_llm(model: str, provider: str, temperature: float = 0.0):
    """Dynamically initializes an LLM from the given provider.

    Args:
        model (str): The name of the model to use.
        provider (str): The name of the provider to use.
        temperature (float, optional): The temperature to use for the model. Defaults to 0.0.

    Raises:
        ImportError: If the required provider-specific package is not installed.
        RuntimeError: If initialization fails for any other reason.

    Returns:
        Any: An initialized LLM/chat model instance ready for use.
    """
    try:
        return init_chat_model(model=model, model_provider=provider, temperature=temperature)
    except ImportError as e:
        missing_pkg = _detect_missing_package(provider)
        raise ImportError(
            f"\n[llm-privacy-filter] The provider '{provider}' requires the package '{missing_pkg}', "
            f"which is not installed.\n"
            f"Install it using:\n\n    pip install -U {missing_pkg}\n"
        ) from e
    except Exception as e:
        raise RuntimeError(f"Failed to initialize provider '{provider}' for model '{model}': {e}")

def _detect_missing_package(provider: str) -> str:
    """Detects the missing package for a given provider.

    Args:
        provider (str): The name of the provider.

    Returns:
        str: The name of the missing package.
    """
    mapping = {
        "openai": "langchain-openai",
        "google-genai": "langchain-google-genai",
        "anthropic": "langchain-anthropic",
        "ollama": "langchain-ollama",
        "mistral": "langchain-mistralai",
    }
    return mapping.get(provider, f"langchain-{provider}")
