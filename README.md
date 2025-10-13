# 🧩 llm-privacy-filter

> A lightweight, modular, LLM-powered privacy filtering library for masking sensitive information in text.

[![PyPI Version](https://img.shields.io/pypi/v/llm-privacy-filter.svg)](https://pypi.org/project/llm-privacy-filter/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-%3E%3D3.9-blue)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/powered%20by-LangChain-green)](https://www.langchain.com/)

---

## 🧠 Overview

`llm-privacy-filter` is a **modular text anonymization toolkit** built on top of the LangChain ecosystem.
It uses large language models (LLMs) to **detect and mask sensitive entities** (like names, emails, phone numbers, and IDs) from natural language text, based on configurable **privacy sensitivity thresholds**.

It’s ideal for:

* Pre-processing user data before training or inference.
* Privacy-preserving text analytics and LLM evaluation pipelines.
* Redacting personally identifiable information (PII) in compliance with GDPR/CCPA.

---

## 📦 Features

✅ Mask sensitive entities using LLM reasoning
✅ Adjustable sensitivity levels (0.0–1.0) for granular privacy control
✅ Simple unified API with multiple model providers (Ollama, OpenAI, Anthropic, Gemini, etc.)
✅ Pydantic-based structured outputs
✅ Zero external database or service dependency

---

## 🏗️ Installation

### Basic installation

```bash
pip install llm-privacy-filter
```

### With provider integrations

```bash
# For Ollama (default)
pip install llm-privacy-filter[ollama]

# For OpenAI models
pip install llm-privacy-filter[openai]

# For Anthropic models
pip install llm-privacy-filter[anthropic]

# For Google Gemini models
pip install llm-privacy-filter[gemini]

# Install all providers
pip install llm-privacy-filter[all]
```

> **Python ≥3.9** is required.

---

## ⚙️ Quick Start

```python
from llm_privacy_filter import Masker

masker = Masker(
    model="gpt-oss:120b-cloud",   # or any supported model
    model_provider="ollama"       # ollama | openai | anthropic | google-genai
)

text = """
Dr. Jane A. Smith, a senior researcher at MIT, was born on March 12, 1985.
She can be reached at jane.smith@example.com or +1-202-555-0198.
She lives at 45 Cherry Street, Boston, MA, and holds a US passport number X1234567.
"""

masked_text, mapping = masker.mask_text(text, sensitivity=1.0)

print(masked_text)
print(mapping)
```

**Example Output:**

```json
{
  "masked_text": "[name.salutation] [name.first] [name.last], a senior researcher at [organization.education], was born on [date.date_of_birth]. She can be reached at [email_address] or [phonenumber.mobile]. She lives at [address], and holds a [passport_number].",
  "text_to_entities": {
    "Jane": ["name.first"],
    "Smith": ["name.last"],
    "MIT": ["organization.education"],
    "March 12, 1985": ["date.date_of_birth"],
    "jane.smith@example.com": ["email_address"],
    "+1-202-555-0198": ["phonenumber.mobile"],
    "45 Cherry Street, Boston, MA": ["address"],
    "X1234567": ["passport_number"]
  }
}
```

---

## 🧩 Architecture

### Project Structure

```
data4i-llm_privacy_filter/
│
├── pyproject.toml         # Build metadata and dependencies
├── requirements.txt       # Full dependency list (for development)
├── LICENSE                # MIT license
├── README.md              # This documentation
│
└── llm_privacy_filter/
    ├── __init__.py        # Public interface
    ├── __main__.py        # CLI entrypoint
    ├── core.py            # Main Masker class
    ├── pdet.py            # Privacy Data Entity Taxonomy (PDET)
    ├── privacy_states.py  # Pydantic models for outputs
    ├── prompt_template.py # Prompt template for structured LLM masking
    ├── providers.py       # Dynamic LLM provider initialization
    └── utils.py           # Utility helpers for entity flattening & sorting
```

---

## 🔍 Core Components

### 1️⃣ `Masker` (in `core.py`)

Handles the full pipeline: entity sorting → prompt generation → LLM inference → structured output.

**Usage:**

```python
masker = Masker(model="gpt-4o-mini", model_provider="openai")
masked_text, entity_map = masker.mask_text("My name is John Doe", sensitivity=0.8)
```

**Methods:**

| Method                               | Description                                          |
| ------------------------------------ | ---------------------------------------------------- |
| `mask_text(text, sensitivity)`       | Masks sensitive text according to threshold          |
| `generalize_text(text, sensitivity)` | Placeholder for semantic generalization (future use) |

---

### 2️⃣ `PDET` (in `pdet.py`)

Defines the **Privacy Data Entity Taxonomy**:
a sensitivity-based mapping (0.0–1.0) of entity categories such as `name`, `email`, `passport_number`, etc.

Example:

```python
{
  0.8: [
    {"name": ["first", "last", "middle"]},
    "email_address",
    "phonenumber",
    "ip_address"
  ]
}
```

---

### 3️⃣ `MaskState` (in `privacy_states.py`)

A structured Pydantic model for consistent LLM outputs.

```python
from pydantic import BaseModel

class MaskState(BaseModel):
    masked_text: str
    text_to_entities: dict[str, list[str]]
```

---

### 4️⃣ `MASKING_PROMPT_TEMPLATE` (in `prompt_template.py`)

Prompt design guiding the LLM’s structured response format.

```python
"You are a privacy filter that masks sensitive information..."
```

Ensures consistent JSON output with `masked_text` and `text_to_entities` keys.

---

### 5️⃣ `get_llm()` (in `providers.py`)

Dynamic loader for multiple LLM backends via LangChain.

**Supported Providers:**

| Provider       | Package                  |
| -------------- | ------------------------ |
| `ollama`       | `langchain-ollama`       |
| `openai`       | `langchain-openai`       |
| `anthropic`    | `langchain-anthropic`    |
| `google-genai` | `langchain-google-genai` |
| `mistral`      | `langchain-mistralai`    |

Example:

```python
from llm_privacy_filter.providers import get_llm
llm = get_llm("gpt-4o-mini", "openai")
```

---

### 6️⃣ `utils.py`

Helper functions:

* `flatten_entity_list()` → Handles nested dicts in `PDET`
* `list_to_str()` → Converts lists to readable comma-joined strings
* `sort_entities()` → Filters and formats entity categories by sensitivity threshold

Example:

```python
from llm_privacy_filter.utils import sort_entities
entities = sort_entities(PDET, sensitivity=0.8)
print(entities)
# -> name.first, name.last, email_address, ip_address
```

---

## 🧪 Running from Command Line

You can run the library directly as a CLI test:

```bash
python -m llm_privacy_filter
```

**Output Example:**

```
[name.salutation] [name.first] [name.last], a senior researcher at [organization.education]...
```

---

## 🧰 Development Setup

```bash
git clone https://github.com/Data4i/llm_privacy_filter.git
cd llm_privacy_filter
python -m venv venv
source venv/bin/activate
pip install -e .
```

Run example:

```bash
python -m llm_privacy_filter
```

---

## 🧪 Testing (Coming Soon)

Tests will be added under `tests/` using `pytest`.

```bash
pytest -v
```

---

## 🌐 Supported LLM Providers

| Provider  | Model Example        | Notes                   |
| --------- | -------------------- | ----------------------- |
| Ollama    | `gpt-oss:120b-cloud` | Local & private         |
| OpenAI    | `gpt-4o-mini`        | Cloud-based             |
| Anthropic | `claude-3.5-sonnet`  | High-context reasoning  |
| Google    | `gemini-1.5-pro`     | Multimodal capabilities |

---

## 🪪 License

This project is licensed under the [MIT License](./LICENSE) — free for personal and commercial use.

---

## 👤 Author

**Okechukwu Obiahu**
📧 [paulobiahu@gmail.com](mailto:paulobiahu@gmail.com)
🌐 [GitHub: Data4i](https://github.com/Data4i)

---

## ⭐ Support

If you find this project helpful:

* Give it a ⭐ on GitHub — [Data4i/llm_privacy_filter](https://github.com/Data4i/llm_privacy_filter)
* Share your feedback or issues in the [Issue Tracker](https://github.com/Data4i/llm_privacy_filter/issues)

---
