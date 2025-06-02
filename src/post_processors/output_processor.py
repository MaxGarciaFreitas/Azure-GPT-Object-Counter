"""
Last Updated: June 2, 2025
Author: Max Freitas
File Purpose: Process detections after applying ChatGPT
    - 'merge_to_json_files': converts individual json files to a single .json file
    - 'json_to_excel': converts single .json file into excel
    - 'has_nonzero_detection': filter pd.Dataframe based on 'detections'
    - 'sort_by_detection_class': sort pd.Dataframe based on counts for speciic classes
    - 'convert_detections_to_cols": change detections from single column of format {class1: count, ..} to col1: count_class1, col2: count_class2
"""

import ast
import json
import os

import pandas as pd


def merge_json_files(input_dir, output_filename, output_dir) -> None:
    """Merges Multiple JSON files from a directory into a single JSON fie.

    Args:
        input_dir(str): Path to directory containing JSON files to merge
        output_filename (str): Name for the output merged JSON file
        output_dir (str): Directory path where merged JSON will be saved

    Returns:
        None: Outputs merged JSON file to specifcied location

    Note:
        Skips files that fail JSON decoding and prints error message
    """
    merged_data = []

    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(input_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        merged_data.extend(data)
                    else:
                        merged_data.append(data)
                except json.JSONDecodeError as e:
                    print(f"Skipping {filename}: {e}")

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, indent=2)

    print(f"Sucessfully saved  merged JSON to: {output_path} as {output_filename}")


def json_to_excel(json_path, excel_filename, output_dir):
    """Converts a JSON file to Excel format

    Args:
        json_path (str): Path to input JSON file
        excel_filename (str): Name for the output Excel file
        output_dir (str): Directory path where Excel file will be saved
    """

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    os.makedirs(output_dir, exist_ok=True)
    excel_path = os.path.join(output_dir, excel_filename)

    df.to_excel(excel_path, index=False)

    print(f"Successfully saved Excel file to: {excel_path} as {excel_filename}")


def has_nonzero_detection(df, col_name="detections"):
    """Filters pd.DataFrame to only include rows with non-zero-detections.

    Args:
        df (pd.DataFrame): Input pd.DataFrame containing detection data
        col_name (str, optional): Name of column containing detection strings,

    Returns:
        pd.DataFrame: Filtered pd.DataFrame containing only rows with at least one non-zero detection count
    """

    def check_detection(detection_str):
        try:
            detection_dict = ast.literal_eval(detection_str)
            return any(value > 0 for value in detection_dict.values())
        except Exception:
            return False

    return df[df[col_name].apply(check_detection)]


def sort_by_detection_class(df, class_name="cigarettes", col_name="detections"):
    """Sorts pd.DataFrame based on detection counts for a specific class.

    Args:
        df(pd.Dataframe): Input DataFrame containing detection data
        class_name (str, optional): Detection class to sort by.
        col_name (str, optional): Name of column containing detection strings.

    Returns:
        pd.DataFrame: pd.DataFrame sorted in descending order by counts of specified note

    Note:
        Assumes: `col_name` in format {class1: count, class2: count, ...}

    """

    def extract_class_count(detection_str):
        try:
            detection_dict = ast.literal_eval(detection_str)
            return detection_dict.get(class_name, 0)
        except Exception:
            return 0

    # Create temporary column with the count
    df["__sort_key__"] = df[col_name].apply(extract_class_count)

    # Sort by it in descending order
    sorted_df = df.sort_values(by="__sort_key__", ascending=False).drop(
        columns="__sort_key__"
    )

    return sorted_df


def convert_detections_to_cols(df, col_name="detections"):
    """Expands detection string column into multiple columns (one per detection class).

    Args:
        df (pd.DataFrame): Input pd.DataFrame containing detection data
        col_name (str, optional): Name of column containing detection strings.

    Returns:
        pd.DataFrame: Original pd.DataFrame with added columns for each detection class
                     (columns named as 'detections_classname')
    """

    def parse_detection(detection_str):
        try:
            return ast.literal_eval(detection_str)
        except Exception:
            return {}

    # Apply parser to extract dicts
    parsed = df[col_name].apply(parse_detection)

    # Normalize into separate columns
    detection_df = pd.json_normalize(parsed)

    # Optionally rename the columns for clarity
    detection_df.columns = [f"{col_name}_{c}" for c in detection_df.columns]

    # Concatenate with original DataFrame (drop original detections column if desired)
    return pd.concat([df, detection_df], axis=1)
