"""
Last Updated: June 2, 2025
Author: Max Freitas
File Purpose: Test counting objects on test image
"""

import os
from openai import AzureOpenAI
import sys
import platform
from src.pre_processors.count_images_with_chatgpt import count_objects_in_images



# setup client
client = AzureOpenAI(
    azure_endpoint=endpoint, api_key=subscription_key, api_version=api_version
)
python_metadata = {
    "python_version": platform.python_version(),
    "python_implementation": platform.python_implementation(),
    "os": platform.system(),
    "os_version": platform.version(),
    "machine": platform.machine(),
    "architecture": platform.architecture()[0],
    "executable_path": sys.executable,
}

prompt_text = "Count the number of snakes, and turtles in the image. Return the result in this exact format: {Snakes: <number>, Turtles: <number>}. If none are present, return 0 for each."

image_path = "src/demo/test_animal.jpeg"
count_objects_in_images(
    image_path,
    prompt_text,
    model_version=deployment,
    output_dir="src/demo",
    client=client,
    deployment=deployment,
    python_metadata=python_metadata,
)