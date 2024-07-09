# check_dataset.py
# Script to check datasets and update verification results in metadata.

import json
import logging
import mimetypes
import os
import uuid
from typing import Dict, Any, Tuple, List

from ..constants import (
    CONTENT_METADATA_SUFFIX,
    DATASET_KEY,
    PATH_KEY,
    GENERAL_METADATA_FILENAME,
    FILE_NUMBER_KEY,
    DATA_KEY,
    FORMAT_REFERENCE_KEY,
    METADATA_CHECK_KO,
    METADATA_CHECK_OK,
    NETCDF_FORMAT,
    NETCDF_FILE_SUFFIX,
    VERIFICATION_RESULTS_KEY,
    UUID_KEY,
    NETCDF_MIME_TYPE,
    FAIR_RESULTS_KEY,
    METADATA_VALUES_KEY,
    FINDABLE_KEY,
    COHERENCE_KEY,
    CONSISTENCY_KEY,
    PLAUSIBILITY_KEY,
    OTHER_RESULTS_KEY,
    REUSABLE_KEY,
    INTEROPERABLE_KEY,
    ACCESSIBLE_KEY,
    UUID_VALUE_KEY,
    CHECKSUMS_REFERENCE_KEY,
    DATAPAPER_REFERENCE_KEY,
    RELEASENOTES_REFERENCE_KEY,
    RGPD_KEY,
    RESTRICTIONS_KEY,
    SIZE_KEY,
    LAST_MODIFICATION_DATE_KEY,
    PROTECTION_LEVEL_KEY,
    SOURCE_KEY,
    SOURCE_URL_KEY,
    DOWNLOAD_DATE_KEY,
    LICENSE_DOI_KEY,
    DATA_LICENSE_KEY,
    LICENSE_QUOTE_KEY,
    TIME_RANGE_KEY,
    START_KEY,
    END_KEY,
    NAME_KEY,
    UNIT_KEY,
    MIN_VALUE_KEY,
    MAX_VALUE_KEY,
    TOTAL_MISSING_VALUE_KEY,
    MISSING_VALUE_INDICATOR_KEY,
    MISSING_VALUE_INDICATOR_DEFINED_KEY,
    DIMENSIONS_KEY,
    METEO_VARIABLE_KEY,
    GENERAL_KEY,
    DATA_FILE_NAME_KEY,
    TIME_REFERENCE_KEY,
    X_COORDINATE_KEY,
    Y_COORDINATE_KEY,
    Z_COORDINATE_KEY,
    SPATIAL_REFERENCE_KEY,
    FORECAST_KEY,
    PROBABILISTIC_DIMENSION_KEY,
    T_REFERENCE_KEY,
    STANDARD_NAME_KEY
)


def load_catalog(catalog_path: str) -> Dict[str, Any]:
    """
    Load the dataset catalog from a JSON file safely and efficiently.

    Checks the file's existence and validates the JSON content for safety and correctness.

    Args:
        catalog_path (str): The file path to the JSON catalog file.

    Returns:
        dict: The catalog as a dictionary loaded from the JSON file.

    Raises:
        FileNotFoundError: If the JSON file does not exist.
        ValueError: If the JSON file cannot be decoded or contains invalid data.
    """
    if not os.path.isfile(catalog_path):
        error_message = f"The specified file does not exist: {catalog_path}"
        logging.error(error_message)
        raise FileNotFoundError(error_message)

    try:
        with open(catalog_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            # Simple check for expected top-level type
            if not isinstance(data, dict):
                error_message = "JSON content is not in expected dictionary format."
                logging.error(error_message)
                raise ValueError(error_message)

            return data

    except json.JSONDecodeError as e:
        error_message = f"Failed to decode JSON from the provided file: {str(e)}"
        logging.error(error_message)
        raise ValueError(error_message)


def save_catalog(catalog: Dict[str, Any], catalog_path: str) -> None:
    """
    Save the updated catalog back to the JSON file.

    This function writes a dictionary representation of a dataset catalog to a JSON file.

    Args:
        catalog (Dict[str, Any]): The catalog data to be saved.
        catalog_path (str): The file path where the JSON catalog file will be saved.

    Raises:
        IOError: If there's an issue writing to the file.
        ValueError: If the data cannot be encoded to JSON.
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(catalog_path), exist_ok=True)

    try:
        with open(catalog_path, "w", encoding="utf-8") as file:
            json.dump(catalog, file, indent=4)
    except TypeError as e:
        error_message = f"Data type error during JSON serialization: {str(e)}"
        logging.error(error_message)
        raise ValueError(error_message)
    except ValueError as e:
        error_message = f"JSON serialization error: {str(e)}"
        logging.error(error_message)
        raise ValueError(error_message)
    except OSError as e:
        error_message = f"Error opening or writing to file at {catalog_path}: {str(e)}"
        logging.error(error_message)
        raise IOError(error_message)


def check_metadata_values(metadata: Dict) -> Tuple[str, str, str, str]:
    """
    Ensure all metadata fields are non-empty and perform various integrity checks.

    Args:
        metadata (Dict): Metadata dictionary of a dataset.

    Returns:
        Tuple[str, str, str, str]: A tuple indicating the result of metadata checks, plausibility checks,
    consistency checks, and coherence checks.
    """
    # Default value: "OK"
    plausibility_check = METADATA_CHECK_OK
    consistency_check = METADATA_CHECK_OK
    coherence_check = METADATA_CHECK_OK

    # Define required fields for general metadata and content-specific metadata
    required_fields_general = get_required_general_fields()
    required_fields_content = get_required_content_fields()

    # Check general metadata fields (from catalog)
    metadata_check = check_fields(metadata, required_fields_general)

    dataset_path = metadata.get(DATASET_KEY, {}).get(PATH_KEY, "")
    if dataset_path and os.path.isdir(dataset_path):
        # Check content metadata files
        metadata_check, plausibility_check, consistency_check, coherence_check = (
            check_content_metadata_files(
                dataset_path,
                required_fields_content,
                metadata_check,
            )
        )

    return metadata_check, plausibility_check, consistency_check, coherence_check


def get_required_general_fields() -> List[str]:
    """
    Returns:
        List [str]: A list containing the names of every required general metadata field.
    """
    separator = "."
    return [
        f"{DATASET_KEY}{separator}{PATH_KEY}",
        f"{DATASET_KEY}{separator}{UUID_KEY}",
        f"{DATASET_KEY}{separator}{SIZE_KEY}",
        f"{DATASET_KEY}{separator}{FILE_NUMBER_KEY}",
        f"{DATASET_KEY}{separator}{LAST_MODIFICATION_DATE_KEY}",
        f"{DATA_KEY}{separator}{PROTECTION_LEVEL_KEY}",
        f"{DATA_KEY}{separator}{SOURCE_KEY}",
        f"{DATA_KEY}{separator}{SOURCE_URL_KEY}",
        f"{DATA_KEY}{separator}{DOWNLOAD_DATE_KEY}",
        f"{DATA_KEY}{separator}{FORMAT_REFERENCE_KEY}",
        f"{DATA_KEY}{separator}{DATA_LICENSE_KEY}",
        f"{DATA_KEY}{separator}{LICENSE_DOI_KEY}",
        f"{DATA_KEY}{separator}{LICENSE_QUOTE_KEY}",
        f"{DATA_KEY}{separator}{TIME_RANGE_KEY}{separator}{START_KEY}",
        f"{DATA_KEY}{separator}{TIME_RANGE_KEY}{separator}{END_KEY}",
        f"{CHECKSUMS_REFERENCE_KEY}",
        f"{DATAPAPER_REFERENCE_KEY}",
        f"{RELEASENOTES_REFERENCE_KEY}",
        f"{RGPD_KEY}",
        f"{RESTRICTIONS_KEY}",
    ]


def get_required_content_fields() -> List[str]:
    """
    Returns:
        List [str]: A list containing the names of every required content metadata field.
    """
    separator = "."
    return [
        f"{GENERAL_KEY}{separator}{DATA_FILE_NAME_KEY}",
        f"{GENERAL_KEY}{separator}{SPATIAL_REFERENCE_KEY}",
        f"{GENERAL_KEY}{separator}{TIME_REFERENCE_KEY}",
        f"{DIMENSIONS_KEY}{separator}{X_COORDINATE_KEY}",
        f"{DIMENSIONS_KEY}{separator}{Y_COORDINATE_KEY}",
        f"{DIMENSIONS_KEY}{separator}{Z_COORDINATE_KEY}",
        f"{DIMENSIONS_KEY}{separator}{T_REFERENCE_KEY}",
        f"{DIMENSIONS_KEY}{separator}{FORECAST_KEY}",
        f"{DIMENSIONS_KEY}{separator}{PROBABILISTIC_DIMENSION_KEY}",
    ]


def get_meteo_variable_fields() -> List[str]:
    """
    Returns:
        List [str]: A list containing the names of every required meteo variable metadata field.
    """
    return [
        NAME_KEY,
        STANDARD_NAME_KEY,
        UNIT_KEY,
        MIN_VALUE_KEY,
        MAX_VALUE_KEY,
        TOTAL_MISSING_VALUE_KEY,
        MISSING_VALUE_INDICATOR_KEY,
        MISSING_VALUE_INDICATOR_DEFINED_KEY,
    ]


def check_fields(metadata: Dict, fields: List[str]) -> str:
    """
    Check each required metadata field to ensure that it is not empty.

    Args:
        metadata (Dict): Metadata dictionary of a dataset.
        fields (List[str]): List of required field paths.

    Returns:
        str: "OK" if all required fields are non-empty; "KO" if any are empty.
    """
    result = METADATA_CHECK_OK
    for field in fields:
        keys = field.split(".")
        value = metadata
        try:
            for key in keys:
                value = value[key]
            if (
                    value is None
                    or value == ""
                    or (isinstance(value, (list, dict)) and not value)
            ):
                logging.info(f"Empty field: {field}")
                return METADATA_CHECK_KO
        except KeyError:
            logging.info(f"Missing field: {field}")
            return METADATA_CHECK_KO
    return result


def check_content_metadata_files(
        path: str, fields: List[str], metadata_check: str
) -> Tuple[str, str, str, str]:
    """
    Check metadata fields within content-specific metadata files in a directory.

    Args:
        path (str): Directory path containing metadata files.
        fields (List[str]): List of required field paths for content-specific metadata.
        metadata_check (str): Current result of metadata checks.

    Returns:
        Tuple[str, str, str, str]: Updated metadata, plausibility, consistency and coherence results after
    checking content metadata files.
    """
    for filename in os.listdir(path):
        if filename.endswith(CONTENT_METADATA_SUFFIX):
            with open(os.path.join(path, filename), "r") as file:
                content_metadata = json.load(file)

                if metadata_check == METADATA_CHECK_OK:
                    content_metadata_check = check_fields(content_metadata, fields)

                # Verifications on meteo-variables
                variables = content_metadata.get(DIMENSIONS_KEY, {}).get(
                    METEO_VARIABLE_KEY, []
                )
                (
                    meteo_metadata_check,
                    plausibility_check,
                    consistency_check,
                    coherence_check,
                ) = check_meteo_variables(variables)

                if (
                        metadata_check == METADATA_CHECK_OK
                        and content_metadata_check == METADATA_CHECK_OK
                        and meteo_metadata_check == METADATA_CHECK_OK
                ):
                    metadata_check = METADATA_CHECK_OK
                else:
                    metadata_check = METADATA_CHECK_KO

    return metadata_check, plausibility_check, consistency_check, coherence_check


def check_meteo_variables(meteo_variables: List[Any]) -> Tuple[str, str, str, str]:
    """
    Check metadata fields within content-specific meteo variables field in metadata content files.

    Args:
        meteo_variables (List[Any]): A list containing the meteo variables to check.

    Returns:
        Tuple[str, str, str, str]: Updated metadata, plausibility, consistency and coherence results after
    checking meteo variables content.
    """
    meteo_variable_fields = get_meteo_variable_fields()

    # Default value : "OK"
    metadata_check = METADATA_CHECK_OK
    plausibility_check = METADATA_CHECK_OK
    consistency_check = METADATA_CHECK_OK
    coherence_check = METADATA_CHECK_OK

    for variable in meteo_variables:
        for field in meteo_variable_fields:
            try:
                # Check if the field exists and is non-empty
                if (
                        field not in variable
                        or not variable[field]
                        and variable[field] != 0
                ):
                    metadata_check, plausibility_check = check_plausibility(
                        field, plausibility_check
                    )

                # Consistency check
                if field == TOTAL_MISSING_VALUE_KEY and variable[field] > 0:
                    consistency_check = METADATA_CHECK_KO

                # FOR FUTURE: coherence check (add variables to a dictionary)
                # if field == "name" and variable[field] is not in ALLOWED_FIELDS:
                # coherence_check = METADATA_CHECK_KO

            except KeyError:
                metadata_check, plausibility_check = check_plausibility(
                    field, plausibility_check
                )
    return metadata_check, plausibility_check, consistency_check, coherence_check


def check_plausibility(field: str, plausibility_check: str) -> Tuple[str, str]:
    """
    Checks whether min-value or max-value fields are missing, in which case the plausibility check does not pass.

    Args:
        field (str): The field to check.
        plausibility_check (str): Current value for plausibility_check.

    Returns:
        Tuple[str, str]: The updated metadata and plausibility checks.
    """
    if field == MIN_VALUE_KEY or field == MAX_VALUE_KEY:
        logging.info(f"Empty field (plausibility check failed): {field}")
        plausibility_check = METADATA_CHECK_KO
    logging.info(f"Missing field: {field}")
    metadata_check = METADATA_CHECK_KO

    return metadata_check, plausibility_check


def check_uuid(metadata: Dict) -> str:
    """Check if the UUID field contains a valid UUID version 5.

    Verifies the format and version of the UUID in the dataset's metadata to ensure it's a valid version 5 UUID. Part
    of the 'findable' FAIR component to check.

    Args:
        metadata (Dict): Metadata dictionary containing the UUID field.

    Returns:
        str: "OK" if the UUID is valid and version 5; "KO" if not.
    """
    try:
        uuid_obj = uuid.UUID(metadata.get(DATASET_KEY).get(UUID_KEY))
        if uuid_obj.version == 5:
            return METADATA_CHECK_OK
        else:
            logging.info(f"Invalid UUID version: {uuid_obj}")
            return METADATA_CHECK_KO
    except ValueError:
        logging.info(f"Invalid UUID value: {metadata.get(DATASET_KEY).get(UUID_KEY)}")
        return METADATA_CHECK_KO


def check_files_exist(metadata: Dict) -> str:
    """Check if all required files are present in the dataset directory.

    Verifies the existence of crucial metadata files necessary for the dataset to be 'accessible'.
    This includes general and content metadata files.

    Args:
        metadata (Dict): Metadata dictionary that might contain paths to required files.

    Returns:
        str: "OK" if all files exist; "KO" if any are missing.
    """
    dataset_path = metadata.get(DATASET_KEY).get(PATH_KEY)
    general_metadata_path = os.path.join(dataset_path, GENERAL_METADATA_FILENAME)

    # Verify general metadata file presence
    if not os.path.exists(general_metadata_path):
        logging.info(f"General metadata file not found: {general_metadata_path}")
        return METADATA_CHECK_KO
    else:
        with open(general_metadata_path, "r") as file:
            general_metadata = json.load(file)
            if general_metadata != metadata:
                logging.error(
                    f"Catalog general metadata does not match file general metadata at {general_metadata_path}"
                )
                return METADATA_CHECK_KO

    # Verify content metadata file presence for every metadata file
    content_metadata_count = 0
    for file in os.listdir(dataset_path):
        if file.endswith(CONTENT_METADATA_SUFFIX):
            content_metadata_count += 1
    file_number = int(metadata.get(DATASET_KEY).get(FILE_NUMBER_KEY))
    if content_metadata_count != file_number:
        logging.info(
            f"Only {content_metadata_count} content metadata files out of {file_number} data files were "
            f"found in {dataset_path}"
        )
        return METADATA_CHECK_KO
    return METADATA_CHECK_OK


def check_mime_type(metadata: Dict) -> str:
    """Verify that the dataset file formats are valid MIME types.

    Checks the format reference in the dataset metadata to ensure it corresponds to a recognized MIME type,
    supporting 'interoperability' of the dataset.

    Args:
        metadata (Dict): Metadata dictionary containing the format reference.

    Returns:
        str: "OK" if the format is a valid MIME type; "KO" if it is not.
    """
    dataset_path = metadata.get(DATASET_KEY).get(PATH_KEY)
    data_format = metadata.get(DATA_KEY).get(FORMAT_REFERENCE_KEY)
    if data_format == NETCDF_FORMAT:
        for metadata_file in os.listdir(dataset_path):
            if metadata_file.endswith(CONTENT_METADATA_SUFFIX):
                data_file = (
                        metadata_file.removesuffix(CONTENT_METADATA_SUFFIX)
                        + NETCDF_FILE_SUFFIX
                )
                mime_type = mimetypes.guess_type(data_file)[0]
                if mime_type is None or mime_type != NETCDF_MIME_TYPE:
                    return METADATA_CHECK_KO
    return METADATA_CHECK_OK


def validate_dataset(metadata: Dict) -> Dict:
    """Perform validation checks on the dataset metadata.

    Executes several checks on the dataset's metadata to ensure compliance with FAIR principles and additional
    integrity checks. This includes validations for 'findability', 'accessibility', 'interoperability',
    and 'reusability' criteria.

    Args:
        metadata (Dict): The metadata dictionary of the dataset to be validated.

    Returns:
        Dict: A dictionary with detailed results of each FAIR criterion and other integrity checks.
    """

    (metadata_check, plausibility_check, consistency_check, coherence_check) = (
        check_metadata_values(metadata)
    )

    results = {
        FAIR_RESULTS_KEY: {
            FINDABLE_KEY: {
                METADATA_VALUES_KEY: metadata_check,
                UUID_VALUE_KEY: check_uuid(metadata),
            },
            ACCESSIBLE_KEY: check_files_exist(metadata),
            INTEROPERABLE_KEY: check_mime_type(metadata),
            REUSABLE_KEY: metadata_check,
        },
        OTHER_RESULTS_KEY: {
            PLAUSIBILITY_KEY: plausibility_check,
            CONSISTENCY_KEY: consistency_check,
            COHERENCE_KEY: coherence_check,
        },
    }
    return results


def check_datasets(catalog_path: str):
    """Checks and verifies datasets within the specified catalog.

    Opens and reads the dataset catalog from the given path, applying a series of verification rules to each dataset.
    This function is designed to ensure that all datasets comply with predefined validation criteria.

    Args:
        catalog_path (str): The file path to the catalog JSON file that contains the datasets to be verified.

    Returns:
        None: This function does not return a value but updates the catalog with verification results.

    Raises:
        FileNotFoundError: If the catalog file does not exist at the specified path.
        json.JSONDecodeError: If the catalog file is not a valid JSON.
    """
    try:
        with open(catalog_path, "r") as file:
            catalog = json.load(file)
    except FileNotFoundError:
        logging.error(f"Catalog file not found: {catalog_path}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from the catalog file: {e}")
        raise

    for dataset in catalog:
        verification_results = validate_dataset(dataset)
        dataset[VERIFICATION_RESULTS_KEY] = verification_results

        general_metadata_path = os.path.join(
            dataset[DATASET_KEY][PATH_KEY], GENERAL_METADATA_FILENAME
        )
        with open(general_metadata_path, "r") as file:
            general_metadata = json.load(file)
            general_metadata[VERIFICATION_RESULTS_KEY] = verification_results
        with open(general_metadata_path, "w") as file:
            json.dump(general_metadata, file, indent=4)
            logging.info("General metadata updated with verification results.")

    # Save the updated catalog back to the file
    with open(catalog_path, "w") as file:
        json.dump(catalog, file, indent=4)
        logging.info("Catalog updated with verification results.")
