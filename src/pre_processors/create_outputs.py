"""
Last Updated May 22, 2025
Author: Max Freitas
File Purpose: Create outpost JSON for reproducible research
"""

from datetime import datetime



def create_outputs(
    image_name: str,
    model_outputs: dict,
    model_version: str,
    json_filename: str,
    output_dir: str,
    prompt_text,
    original_image_size,
    resized_image_size,
    python_metadata,
):
    """
    We are creating output JSON file for readible output.

    Params:
    - image_name (str): name of the image file
    - model_outputs (dict): dict of detections in form {'class1': #, 'class2': #, ...}

    Returns:
    - Structured JSON File
    """
    return {
        "image_name": image_name,
        "output_json_name": json_filename,
        "output_dir": output_dir,
        "image_metadata": {
            "original_image_size": original_image_size,
            "resized_and_padded_size": resized_image_size,
        },
        "detections": model_outputs,
        "model_metadata": {
            "model_version": model_version,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "input_message": prompt_text,
        },
        "python_metadata": python_metadata,
    }
