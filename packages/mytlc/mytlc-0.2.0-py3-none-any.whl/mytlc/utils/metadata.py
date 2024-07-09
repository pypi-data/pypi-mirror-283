import copy
import json
import logging
import os.path

import pandas as pd
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from ..constants import (
    EDITABLE_GENERAL_METADATA_KEYS,
    METADATA_SCHEMA_FILENAME,
    CONTENT_METADATA_SCHEMA_FILENAME,
    METADATA_TEMPLATE_FILENAME,
    CONTENT_METADATA_TEMPLATE_FILENAME,
    GENERAL_METADATA,
    CONTENT_METADATA,
    MODULE_ROOT_PATH,
    SCHEMAS_DIR,
    CONTENT_METADATA_SUFFIX,
)


def get_metadata_template(template):
    """
    Function that returns a template of json metadata file

    Args:
        template : JSON template name
    """
    if template == GENERAL_METADATA:
        template_name = METADATA_TEMPLATE_FILENAME
    elif template == CONTENT_METADATA:
        template_name = CONTENT_METADATA_TEMPLATE_FILENAME
    else:
        message = "Invalid template name"
        logging.error(message)
        raise ValueError(message)

    metadata_template_path = os.path.join(MODULE_ROOT_PATH, SCHEMAS_DIR, template_name)

    with open(metadata_template_path, "r") as f:
        json_template = json.load(f)
    return json_template


def get_metadata_schema(schema):
    """
    Function that returns the json schema of metadata json file

    Args:
        schema : JSON schema name
    """
    if schema == GENERAL_METADATA:
        schema_name = METADATA_SCHEMA_FILENAME
    elif schema == CONTENT_METADATA:
        schema_name = CONTENT_METADATA_SCHEMA_FILENAME
    else:
        message = "Invalid schema name"
        logging.error(message)
        raise ValueError(message)

    metadata_schema_path = os.path.join(MODULE_ROOT_PATH, SCHEMAS_DIR, schema_name)

    with open(metadata_schema_path, "r") as f:
        json_schema = json.load(f)
    return json_schema


def update_metadata_file(json_data, schema, update_data):
    """
    Function which update a json metadata object

    Args:
        json_data : JSON object to update
        schema : JSON schema used to check if final updated json is correctly completed
        update_data : Data used to update json_data
    """
    # Check if provided keys are defined in the json schema
    validate_key(update_data, json_data)

    # Store json_data input before update
    original_json_data = copy.deepcopy(json_data)
    updated_data = copy.deepcopy(json_data)

    try:
        for key_path, new_value in update_data.items():
            keys = key_path.split(".")
            current = updated_data
            for key in keys[:-1]:
                current = current[key]
            current[keys[-1]] = new_value
        validate(instance=updated_data, schema=schema)
        return updated_data
    # if the updated json doesn't respect json schema : original json returned
    except ValidationError as e:
        logging.error(f"Key update failed : {e}")
        return original_json_data


def validate_key(json_data, template):
    """
    Function to check if provided keys are defined in template

    Args:
        json_data : Dict containing key/values to check
        template : File used to check json_data keys
    """
    for key, value in json_data.items():
        nested_keys = key.split(".")
        current_dict = template
        for nested_key in nested_keys[:-1]:
            if nested_key in current_dict:
                current_dict = current_dict[nested_key]
            else:
                message = f"Impossible to update key '{key}' : invalid nested key : {nested_key}"
                logging.error(message)
                raise KeyError(message)

        last_key = nested_keys[-1]
        if last_key in current_dict:
            current_dict[last_key] = value
        else:
            message = f"Invalid key : {key}"
            logging.error(message)
            raise KeyError(message)


def check_metadata_text_file(metadata_file_path):
    """
    Function to check if metadata in metadata file provided by user before downloading are valid

    Args:
        metadata_file_path (str): Path to metadata file provided by user
    """
    with open(metadata_file_path, "r") as f:
        for line in f:
            # Split line in file in two parts: checksum and filename
            key, _ = line.strip().split(":", 1)
            if key not in EDITABLE_GENERAL_METADATA_KEYS:
                message = f"Invalid editable metadata : {key}"
                logging.error(message)
                raise ValueError(message)


def get_content_metadata(dataset_directory_path):
    """
    Method returning a dataframe with the content of all metadata content files.
    """
    df = []

    data = {
        "file-name": [],
        "x-coordinate": [],
        "y-coordinate": [],
        "z-coordinate": [],
        "t-reference": [],
        "forecast": [],
        "probabilistic-dimension": [],
        "meteo-variable": [],
    }

    files = os.listdir(dataset_directory_path)
    for file in files:
        if file.endswith(CONTENT_METADATA_SUFFIX):
            with open(os.path.join(dataset_directory_path, file), "r") as f:
                json_data = json.load(f)
                data["file-name"] = [json_data["general"]["data-file-name"]]
                data["x-coordinate"] = [json_data["dimensions"]["x-coordinate"]]
                data["y-coordinate"] = [json_data["dimensions"]["y-coordinate"]]
                data["z-coordinate"] = [json_data["dimensions"]["z-coordinate"]]
                data["t-reference"] = [json_data["dimensions"]["t-reference"]]
                data["forecast"] = [json_data["dimensions"]["forecast"]]
                data["probabilistic-dimension"] = [
                    json_data["dimensions"]["probabilistic-dimension"]
                ]
                data["meteo-variable"] = [json_data["dimensions"]["meteo-variable"]]
                df_temp = pd.DataFrame(data)
                df.append(df_temp)
    df_final = pd.concat(df, ignore_index=True)
    return df_final
