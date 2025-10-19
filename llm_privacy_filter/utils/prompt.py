MASKING_PROMPT_TEMPLATE = """You are a privacy filter that masks sensitive information in a given text based on the provided entity types.

Entities to mask: {entities}
Text: {text}

e.g 
Entities to mask: name.salutation, name.first, name.last, name.middle, organization.company, organization.education, organization.government
Text: John Doe lives in New York and works at OpenAI.

Output Format (as JSON with these keys):
```json
{{
  "masked_text": "string",
  "text_to_entities": {{
    "string": ["string"]
  }}
}}
```

e.g 
```json
{{
  "masked_text": "[name.first] [name.last] lives in New York and works at [organization.company].",
  "text_to_entities": {{
    "John": ["name.first"],
    "Doe": ["name.last"],
    "OpenAI": ["organization.company"]
  }}
}}
```
"""

SEMANTIC_MASKING_PROMPT_TEMPLATE = """

"""