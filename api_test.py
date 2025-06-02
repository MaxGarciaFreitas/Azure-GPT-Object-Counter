"""
Last Updated: June 2, 2025
Author: Max Freitas
File Purpose: Test that Azure API is working in secure computing environment
    - Specify your known endpoint, subscription key.
    - Run using python3 api_test in terminal
    - If you see output, proceed to advanced api calls
"""

import os
from openai import AzureOpenAI

endpoint = os.getenv("ENDPOINT_URL", "YOUR_URL")
deployment = os.getenv("DEPLOYMENT_NAME", "YOUR_MODEL_VERSION")
subscription_key = os.getenv(
    "AZURE_OPENAI_API_KEY",
    "YOUR_KEY",
)
api_version = "YOUR_API_VERSION"


# Initialize Azure OpenAI client with key-based authentication
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version=api_version,
)


# Prepare the chat prompt
chat_prompt = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are an AI assistant that helps people find information.",
            }
        ],
    },
    {"role": "user", "content": "How big is duke university?"},
]

messages = chat_prompt


# Generate the completion

completion = client.chat.completions.create(
    model=deployment,
    messages=messages,
    max_tokens=800,
    temperature=0.7,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False,
)


print(completion.to_json())