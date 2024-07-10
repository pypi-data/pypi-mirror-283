from jinja2 import Template
from promptflow import tool
from promptflow.connections import CustomStrongTypeConnection
from promptflow.contracts.types import PromptTemplate, Secret
from promptflow.tools.common import render_jinja_template, parse_chat

import requests

class PerplexityConnection(CustomStrongTypeConnection):
    """Custom strong type connection for Perplexity API.

    :param api_key: The API key for Perplexity.
    :type api_key: Secret
    :param api_base: The API base URL.
    :type api_base: str
    """
    api_key: Secret
    api_base: str = "https://api.perplexity.ai"

@tool
def generate(
    connection: PerplexityConnection,
    prompt: PromptTemplate,
    model: str = "llama-3-sonar-large-32k-online",
    temperature: float = 1.0,
    top_p: float = None,
    max_tokens: int = 4096,
    **kwargs
) -> str:
    prompt = render_jinja_template(prompt, trim_blocks=True, keep_trailing_newline=True, **kwargs)
    messages = parse_chat(prompt)
    
    headers = {
        'Authorization': f'Bearer {connection.api_key}',
        'Content-Type': 'application/json'
    }

    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": messages
    }

    if top_p is not None:
        payload['top_p'] = top_p
    
    print(f"Payload: {payload}")

    response = requests.post(f"{connection.api_base}/chat/completions", headers=headers, json=payload)
    
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.text}")
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        response.raise_for_status()
