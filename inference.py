"""
Last Updated: June 2, 2025
Author: Max Freitas
File Purpose: Run Inference on Images
"""
import base64
from io import BytesIO
import os
from openai import AzureOpenAI

from correct_orientation import correct_orientation
from resize_with_padding import resize_with_padding
from create_outputs import create_outputs



from PIL import Image
import sys
import json
import ast
import re
import platform



# client info (setup based on your account)
endpoint = os.getenv("ENDPOINT_URL", "YOUR_URL")
deployment = os.getenv("DEPLOYMENT_NAME", "YOUR_MODEL_VERSION")
subscription_key = os.getenv(
    "AZURE_OPENAI_API_KEY",
    "YOUR_KEY",
)
api_version = "YOUR_API_VERSION"

# setup client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version=api_version
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

def count_objects_in_images(
    image_path,
    prompt_text,
    model_version=deployment,
    output_dir=os.getcwd(),
    input_cost_per_million=2,
    output_cost_per_million=8,
):
    # load image
    image = Image.open(image_path)
    image = correct_orientation(image)
    original_image_size = image.size
    resized_image = resize_with_padding(
        image, target_size=(640, 640), padding_color=(0, 0, 0)
    )
    resized_image_size = resized_image.size
    # Convert the processed image to base64 for sending in the API request
    buffered = BytesIO()
    resized_image.save(buffered, format="JPEG")
    base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt_text,
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        },
    ]

    json_filename = f"{image_path.split('.')[0]}_output.json"

    # send request to GPT-4
    completion = client.chat.completions.create(
        model=deployment,
        messages=messages,
        max_tokens=1500,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False,
    )

    # pull detections
    response = completion.to_dict()
    detections_str = response["choices"][0]["message"]["content"]
    detections_str_fixed = re.sub(r"(\w+):", r'"\1":', detections_str)
    detections = ast.literal_eval(detections_str_fixed)  # converts string to dict

    # Create structured output for JSON file
    output = create_outputs(
        image_path,
        detections,
        model_version,
        json_filename,
        output_dir,
        prompt_text,
        original_image_size,
        resized_image_size,
        python_metadata,
    )

    # Get token usage
    token_usage = {
        "prompt_tokens": response["usage"]["prompt_tokens"],
        "completion_tokens": response["usage"]["completion_tokens"],
        "total_tokens": response["usage"]["total_tokens"],
        "prompt_tokens_cost": (
            response["usage"]["prompt_tokens"] * input_cost_per_million
        )
        / 1_000_000,
        "completion_tokens_cost": (
            response["usage"]["completion_tokens"] * output_cost_per_million
        )
        / 1_000_000,
        "total_cost": (
            response["usage"]["prompt_tokens"] * input_cost_per_million
            + response["usage"]["completion_tokens"] * output_cost_per_million
        )
        / 1_000_000,
        "total_cost_per_12000_images": round(
            (
                response["usage"]["prompt_tokens"] * input_cost_per_million
                + response["usage"]["completion_tokens"] * output_cost_per_million
            )
            / 1_000_000
            * 12_000,
            3,
        ),
    }

    # Add token usage to the output
    output["token_usage"] = token_usage

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        json_path = os.path.join(output_dir, json_filename)
    else:
        json_path = json_filename
    with open(json_path, "w") as json_file:
        json.dump(output, json_file, indent=4)
        print(f"Sucessfully saved {json_file} to {output_dir}")

    return output


count_objects_in_images("test_animals.jpg", prompt_text)