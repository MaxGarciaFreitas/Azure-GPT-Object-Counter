"""
Last Updated: June 2, 2025
Author: Max Freitas
File Purpose: Create runner for making API calls
    - `count_objects_in_images`: used to make API calls by combining:
        1. image pre-processing
        2. Azure API call
        3. Output human readible JSON output file for reproducible research
"""

from src.pre_processors.correct_orientation import correct_orientation
from src.pre_processors.create_outputs import create_outputs
from src.pre_processors.resize_with_padding import resize_with_padding

import ast
import base64
import json
import os
import re
from io import BytesIO
from PIL import Image


def count_objects_in_images(
    image_path,
    prompt_text,
    model_version,
    output_dir,
    client,
    deployment,
    python_metadata=None,
    input_cost_per_million=2,
    output_cost_per_million=8,
):
    """Processes image through GPT-model, to count objects and save results.

    Operations:
        1. Load and preprocess image (orientation correction, resizing)
        2. Sends the image to GPT-model API with provided prompt_text
        3. Process the API response to extract object detection
        4. Calculate token usage and associated costs
        5. Saves results to a JSON file and returns the output

    Args:
        image_path: Path to the input image file
        prompt_text: Text prompt to send the GPT-model API
        model_version: Version identifier of the model being used
        output_dir: Directory to save output JSON files
        client: Initialized Azure API client object
        deployment: name of the model deployment to use
        python_metadata: Dictionary containing metadata about the Python environment (default: None)
        input_cost_per_million: Cost per million input tokens (default: 2)
        output_cost_per_million: Cost per million output tokens (default: 8)

    Returns:
        JSON-file in the format (shown in example_output.json)
    """
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

    # json path-name
    parent_folder = os.path.basename(os.path.dirname(image_path))
    grandparent_folder = os.path.basename(os.path.dirname(os.path.dirname(image_path)))
    image_file = os.path.basename(image_path)
    image_file_no_ext = os.path.splitext(image_file)[0]
    json_filename = (
        f"{grandparent_folder}_{parent_folder}_{image_file_no_ext}_output.json"
    )

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
        "total_cost_per_10000_images": round(
            (
                response["usage"]["prompt_tokens"] * input_cost_per_million
                + response["usage"]["completion_tokens"] * output_cost_per_million
            )
            / 1_000_000
            * 10_000,
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
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(output, json_file, indent=4)
        print(f"Sucessfully saved {json_file} to {output_dir}")

    return output