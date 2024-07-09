# catalog_manager.py
# Module for updating the dataset catalog.

import json
import logging
import os
from typing import Dict, List

from jsonschema import validate, ValidationError

from ..constants import (
    METADATA_SCHEMA_FILENAME,
    SCHEMAS_DIR,
    DATASET_KEY,
    UUID_KEY,
    MODULE_ROOT_PATH,
    DATA_KEY,
    SOURCE_KEY,
)


def load_schema(schema_path: str) -> Dict:
    """Loads and returns the JSON schema for validation.

    Loads a JSON schema from the provided path and returns it as a dictionary.
    Used to validate dataset metadata with this schema.

    Args:
        schema_path (str): The full path to the JSON schema file.

    Returns:
        Dict: The schema loaded as a dictionary.

    Raises:
        RuntimeError: If the schema file cannot be loaded or is invalid.
    """
    try:
        with open(schema_path, "r") as schema_file:
            return json.load(schema_file)
    except json.JSONDecodeError as e:
        message = f"Failed to load schema: {e}"
        logging.error(message)
        raise RuntimeError(message)


def validate_metadata(metadata: Dict, schema: Dict) -> None:
    """Validates the metadata of a dataset with the given schema.

    Validates the provided metadata data by comparing it to a JSON schema.
    Throws an exception if the metadata does not match the schema.

    Args:
        metadata (Dict): The metadata to validate.
        schema (Dict): The JSON schema to use for validation.

    Raises:
        ValueError: If the metadata does not conform to the schema.
    """
    try:
        validate(instance=metadata, schema=schema)
    except ValidationError as e:
        message = f"Metadata data is invalid: {e}"
        logging.error(message)
        raise ValueError(message)


def update_catalog(catalog_path: str, metadata: Dict) -> None:
    """Updates the dataset catalog with new metadata or a new dataset.

    Adds a new dataset to the existing catalog or updates an existing dataset if the UUID matches.
    The catalog is saved as a JSON file. Metadata is validated before updating.

    Args:
        catalog_path (str): The path to the catalog file.
        metadata (Dict): The metadata of the dataset to add or update in the catalog.

    Raises:
        ValueError: If the metadata is invalid according to the schema.
        RuntimeError: If the catalog or schema cannot be loaded or saved correctly.
    """
    try:
        # Loading existing catalog if possible
        if os.path.isfile(catalog_path):
            with open(catalog_path, "r") as file:
                catalog = json.load(file)
        else:
            logging.info(
                f"Couldn't open catalog file: {catalog_path}. A new catalog will be created."
            )
            catalog = []

        # Metadata validation
        schema_path = os.path.join(
            MODULE_ROOT_PATH, SCHEMAS_DIR, METADATA_SCHEMA_FILENAME
        )
        schema = load_schema(str(schema_path))
        validate_metadata(metadata, schema)

        # Search for the index of the existing dataset in the catalog
        dataset_index = next(
            (
                i
                for i, item in enumerate(catalog)
                if item[DATASET_KEY][UUID_KEY] == metadata[DATASET_KEY][UUID_KEY]
            ),
            None,
        )
        if dataset_index is not None:
            # Complete replacement of existing metadata with new ones
            catalog[dataset_index] = metadata
            logging.info(
                f"Complete metadata update for dataset {metadata[DATASET_KEY][UUID_KEY]}"
            )
        else:
            # Adding the metadata of the new dataset to the catalog
            catalog.append(metadata)
            logging.info(
                f"Adding a new dataset to the catalog with UUID {metadata[DATASET_KEY][UUID_KEY]}"
            )

        # Save updated catalog
        with open(catalog_path, "w") as file:
            json.dump(catalog, file, indent=4)

    except Exception as e:
        message = f"Error updating catalog: {e}"
        logging.error(message)
        raise RuntimeError(message)


def list_sources(catalog_path: str) -> List[str]:
    """Lists every unique source appearing in this catalog's datasets.

    Args:
        catalog_path (str): The path to the catalog file.

    Returns:
        List[str]: The list of every unique source contained in the catalog.
    """
    try:
        # Load the catalog
        if os.path.isfile(catalog_path):
            with open(catalog_path, "r") as file:
                catalog = json.load(file)
        else:
            logging.error(f"Couldn't open catalog file: {catalog_path}.")

        # Iterate through every dataset
        sources = set()
        for dataset in catalog:
            sources.add(dataset[DATA_KEY][SOURCE_KEY])

        logging.debug(f"Found following sources in catalog {catalog_path}: {sources}")
        return list(sources)

    except Exception as e:
        message = f"Error when listing sources in catalog: {e}"
        logging.error(message)
        raise RuntimeError(message)
