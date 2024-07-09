# search.py
# Module for searching through datasets using filters on 7 dimensions.

import json
import logging
import os
import re
from typing import Dict, List

from ..constants import (
    COORDINATE_KEYS_SUFFIX,
    COORDINATE_AXES,
    SOURCE_KEY,
    DATA_KEY,
    DATASET_KEY,
    NAME_KEY,
    T_REFERENCE_KEY,
    PROBABILISTIC_DIMENSION_KEY,
    FORECAST_KEY,
    METEO_VARIABLE_KEY,
    UUID_KEY,
    PATH_KEY,
    CONTENT_METADATA_SUFFIX,
    GENERAL_KEY,
    DATA_FILE_NAME_KEY,
    DIMENSIONS_KEY,
)


def search_datasets(catalog_path: str, source: str, filters: Dict) -> Dict:
    """Searches for datasets matching filters in a catalog.

    Loads a catalog from the provided path, source and filters.

    Args:
        catalog_path (str): The path to the catalog file.
        source (str): "hadisd", "era5" or "mf".
        filters (Dict): Filters for the search.

    Returns:
        [Dict]: The datasets from the catalog which check given filters.
    """
    matching_datasets = {}

    try:
        with open(catalog_path, "r") as file:
            catalog = json.load(file)
    except FileNotFoundError:
        logging.error(f"Catalog file not found: {catalog_path}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from the catalog file: {e}")
        raise

    logging.debug(
        f"Starting search in {catalog_path} for filters:\n{json.dumps(filters, indent=4)}"
    )

    for dataset in catalog:
        source_match = re.search(source, dataset[DATA_KEY][SOURCE_KEY].lower())
        if source_match:
            compliant_dataset_files = check_dataset(dataset, filters)
            if len(compliant_dataset_files) > 0:
                matching_datasets[dataset[DATASET_KEY][NAME_KEY]] = (
                    compliant_dataset_files
                )
                logging.info(
                    f"Found a dataset that matches the provided filters in {catalog_path}: "
                    f"{dataset[DATASET_KEY][NAME_KEY]}"
                    f" - UUID: {dataset[DATASET_KEY][UUID_KEY]} - Number of matching files: "
                    f"{len(compliant_dataset_files)}"
                )

    # Log if no corresponding dataset was found
    if len(matching_datasets) == 0:
        logging.info(
            f"No matching dataset found for provided filters in {catalog_path}"
        )
    return matching_datasets


def check_dataset(dataset: Dict, filters: Dict) -> List[str]:
    """Checks whether a dataset matches each given filter.

    Args:
        dataset (Dict): The dataset to check.
        filters (Dict): The filters to apply for the check. Filters must respect the following template:
            filters = {
                'x-coordinate': [-10, 10],
                'y-coordinate': [-10, 10],
                'z-coordinate': [-10, 10],
                't-reference': ["20240101:0000", "20240131:2359"],
                'forecast': [0, 24],
                'probabilistic-dimension': [0],
                'meteo-variable': ['Temperature']
            }


    Returns:
        List[str]: The list of the files of the dataset which match each given filter.
    """
    source_is_hadisd = dataset[DATA_KEY][SOURCE_KEY].lower() == "hadisd"

    # Retrieve the list of every content metadata file
    content_metadata_folder_path = dataset[DATASET_KEY][PATH_KEY]
    content_metadata_filenames = get_content_metadata_filenames(
        content_metadata_folder_path
    )

    # Iterate over content metadata file
    compliant_metadata_files = []
    for content_metadata_filename in content_metadata_filenames:
        content_metadata_path = os.path.join(
            content_metadata_folder_path, content_metadata_filename
        )
        try:
            with open(content_metadata_path, "r") as file:
                content_metadata = json.load(file)
        except FileNotFoundError:
            logging.error(f"Content metadata file not found: {content_metadata_path}")
            raise
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from the content metadata file: {e}")
            raise

        check_content_metadata_tuple = check_content_metadata(
            content_metadata, filters, ignore_meteo_variable=source_is_hadisd
        )
        if check_content_metadata_tuple[0]:
            compliant_metadata_files.append(
                (
                    content_metadata[GENERAL_KEY][DATA_FILE_NAME_KEY],
                    check_content_metadata_tuple[1],
                )
            )

    return compliant_metadata_files


def check_content_metadata(
        content_metadata: Dict, filters: Dict, ignore_meteo_variable: bool = False
) -> tuple[bool, str]:
    """Checks whether content metadata matches each given filter.

    Args:
        content_metadata (Dict): The content metadata to check.
        filters (Dict): The filters to apply for the check. Filters must respect the following template:
            filters = {
                'x-coordinate': [-10, 10] OR 8.83938,
                'y-coordinate': [-10, 10] OR 8.83938,
                'z-coordinate': [-10, 10] OR 8.83938,
                'time_reference': ["20240101:0000", "20240131:2359"],
                'forecast': [0, 24],
                'probabilistic_dimension': [0],
                'meteo_variable': ['temperature']
            }
        ignore_meteo_variable (bool, optional): If set to True, the meteo_variable metadata will not be checked ;
            otherwise it will be checked.

    Returns:
        tuple[bool, str]: Dimension 1: True if the content metadata matches each given filter, False otherwise.
            Dimension 2: The details about range overlap (partial or total overlaps).
    """
    error_msg_suffix = f" check failed for content metadata on file {content_metadata[GENERAL_KEY][DATA_FILE_NAME_KEY]}"

    dimensions_metadata = content_metadata[DIMENSIONS_KEY]
    overlap_details = ""

    # Check coordinate intervals
    check_coordinate_intervals_tuple = check_coordinate_intervals(
        filters, dimensions_metadata, error_msg_suffix
    )
    if not check_coordinate_intervals_tuple[0]:
        return False, ""
    elif check_coordinate_intervals_tuple[1]:
        overlap_details += " - " + check_coordinate_intervals_tuple[1]

    # Check time reference
    if T_REFERENCE_KEY in filters:
        check_time_reference_tuple = check_time_reference(
            filters[T_REFERENCE_KEY], dimensions_metadata
        )
        if not check_time_reference_tuple[0]:
            logging.debug("Time reference" + error_msg_suffix)
            return False, ""
        elif check_time_reference_tuple[1]:
            overlap_details += " - " + check_time_reference_tuple[1]

    # Check forecast
    if FORECAST_KEY in filters and not check_forecast(
            filters[FORECAST_KEY], dimensions_metadata[FORECAST_KEY]
    ):
        logging.debug("Forecast" + error_msg_suffix)
        return False, ""

    # Check probabilistic dimension
    if PROBABILISTIC_DIMENSION_KEY in filters and not check_probabilistic_dimension(
            filters[PROBABILISTIC_DIMENSION_KEY], dimensions_metadata
    ):
        logging.debug("Probabilistic" + error_msg_suffix)
        return False, ""

    # Check other variables presence
    # This step is ignored if the dataset source is HadISD since it always contains every weather variable
    if (
            not ignore_meteo_variable
            and METEO_VARIABLE_KEY in filters
            and not check_meteo_variables(filters[METEO_VARIABLE_KEY], dimensions_metadata)
    ):
        logging.debug("Other weather variable" + error_msg_suffix)
        return False, ""
    return True, overlap_details


def get_content_metadata_filenames(content_metadata_folder_path: str) -> List[str]:
    """Returns a list containing the names of all the content metadata files in a given folder.

    Args:
        content_metadata_folder_path (str): The path to the folder containing the content metadata files.

    Returns:
        List[str]: The list of the names of the content metadata files.

    """
    # List every content metadata file name for this dataset
    content_metadata_filenames = []
    for file in os.listdir(content_metadata_folder_path):
        if file.endswith(CONTENT_METADATA_SUFFIX):
            content_metadata_filenames.append(file)
    logging.debug(
        f"Found {len(content_metadata_filenames)} content metadata files:\n{content_metadata_filenames}"
    )

    return content_metadata_filenames


def check_coordinate_interval(
        filters: Dict, metadata: Dict, axis: str
) -> tuple[bool, bool | None]:
    """Verifies that the coordinate interval is respected for this axis on metadata.

    Args:
        filters (Dict): The filters to apply for the check.
        metadata (Dict): A dictionary of metadata associated with a dataset,
            which includes the coordinate interval information on the axis.
        axis (str): The coordinate axis on which the check is done ("x", "y" or "z").

    Returns:
        tuple[bool, bool]: Dimension 1: True if the metadata respects the interval, False otherwise.
            Dimension 2: True if the overlap between ranges is total, False if the overlap is partial.
    """
    filter_key = f"{axis}{COORDINATE_KEYS_SUFFIX}"

    # Return True if filter or metadata do not have the required axis info
    if filter_key not in filters or filter_key not in metadata:
        return True, None

    filter_values = filters[filter_key]
    axis_values = metadata[filter_key]

    # Handling cases where the coordinate is a single value or a range
    if isinstance(axis_values, list):
        if len(axis_values) == 2:
            return check_range(axis_values, filter_values)
        elif len(axis_values) == 1:
            if all(
                    isinstance(elt, float) or isinstance(elt, int) for elt in filter_values
            ):
                return check_single_value(axis_values[0], filter_values), True
            else:
                return check_single_value(axis_values[0], filter_values), False
        else:
            return False, False
    return check_single_value(axis_values, filter_values), True


def check_range(
        axis_values: List[float], filter_values: List[float | str]
) -> tuple[bool, bool]:
    """Helper function to check if range-based metadata respects the filter interval.

    Args:
        axis_values (List[float]): The axis (metadata) values.
        filter_values (List[float | str]): The filter values.

    Returns:
        tuple[bool, bool]: Dimension 1: True if axis values are compliant with the filter values, False otherwise.
            Dimension 2: True if the overlap between ranges is total, False if the overlap is partial.
    """
    if len(axis_values) != 2:
        return False, False
    range_min, range_max = axis_values
    if len(filter_values) == 2:
        # Data is a range, filter is a range: return True if there is an overlap between the ranges
        filter_min, filter_max = filter_values
        if (filter_max < range_min) or (filter_min > range_max):
            # Filter not fitting data
            return False, False
        elif range_min <= filter_max and filter_min <= range_max:
            # Overlap
            if range_min <= filter_min and filter_max <= range_max:
                # Total overlap: data is wider than filter
                return True, True
            else:
                # Partial overlap: filter is wider than data
                return True, False
    # Data is a range, filter is a single point: return True if data (range) contains filter (point)
    return range_min <= filter_values[0] <= range_max, True


def check_single_value(
        axis_value: float, filter_values: List[float] | int | float
) -> bool:
    """Helper function to check if single value metadata respects the filter value.

    Args:
        axis_value (float): The axis (metadata) value.
        filter_values (List[float] | int | float): The filter values (either a range or a number).

    Returns:
        bool: True if axis value is compliant with the filter values, False otherwise.
    """
    if isinstance(filter_values, list):
        if len(filter_values) == 2:
            # Data is a single point, filter is a range: return True if filter (range) contains data (point)
            filter_min, filter_max = filter_values
            return filter_min <= axis_value <= filter_max
        # Data is a single point, filter is a single point: return True if the points equal
        return axis_value == filter_values[0]
    return axis_value == filter_values


def check_coordinate_intervals(
        filters: Dict, metadata: Dict, fail_msg: str = ""
) -> tuple[bool, str]:
    """Verifies that all the coordinate intervals are respected for this metadata.

    Iterates through every coordinate filter if existing, and stops if one of the filters does not match with metadata.

    Args:
        filters (Dict): The filters to apply for the check.
        metadata (Dict): A dictionary of metadata associated with a dataset,
            which includes the coordinate intervals information.
        fail_msg (str): The log message to display/write whenever a check is not met.

    Returns:
         tuple[bool, str]: Dimension 1: True if the metadata respects the interval for every axis, False otherwise.
            Dimension 2: The detail for the filter/data interval overlap (either total overlap or partial overlap).
    """
    in_interval = False
    overlap_message = ""
    for axis in COORDINATE_AXES:
        check_coordinate = check_coordinate_interval(filters, metadata, axis)
        if not check_coordinate[0]:
            logging.debug(f"Coordinate interval ({axis})" + fail_msg)
            return False, ""
        else:
            if check_coordinate is None:
                in_interval = True
            elif check_coordinate[1]:
                in_interval = True
                overlap_message += f"Total overlap on {axis} axis - "
            else:
                in_interval = True
                overlap_message += f"Partial overlap on {axis} axis - "
    return in_interval, overlap_message


def check_time_reference(
        time_reference_filter: List[str], metadata: Dict
) -> tuple[bool, str]:
    """Checks if the dataset's time reference falls within the given time interval filter.

    Args:
        time_reference_filter (List[str]): A list containing two strings,
            the start and end of the filter interval in "YYYYMMDD:HHmm" format.
        metadata (Dict): A dictionary of metadata associated with a dataset,
            which includes the time reference information.

    Returns:
        tuple[bool, str]: Dimension 1: True if the dataset's time reference is within the interval
            defined by the time_reference_filter, False otherwise.
            Dimension 2: The detail for the filter/data interval overlap (either total overlap or partial overlap).
    """
    time_values = metadata[T_REFERENCE_KEY]
    check_time_range_tuple = check_range(time_values, time_reference_filter)
    if check_time_range_tuple[0]:
        if check_time_range_tuple[1]:
            return True, "Total time overlap"
        else:
            return True, "Partial time overlap"
    return False, ""


def check_probabilistic_dimension(
        probabilistic_dimension_filter: int, metadata: Dict
) -> bool:
    """
    Compares the probabilistic dimension value in the metadata with the given filter value.

    Args:
        probabilistic_dimension_filter (int): The specific probabilistic dimension
            value to filter datasets by.
        metadata (Dict): A dictionary of metadata associated with a dataset,
            which includes the probabilistic dimension information.

    Returns:
        bool: True if the dataset's probabilistic dimension matches the filter value,
            False otherwise.
    """
    return metadata[PROBABILISTIC_DIMENSION_KEY] == probabilistic_dimension_filter


def check_forecast(forecast_filter: List[float], metadata: List[float]) -> bool:
    """Verifies that the forecast intervals are respected.

    Args:
        forecast_filter (Dict): The filters to apply for the check on forecast.
        metadata (Dict): The metadata to verify.

    Returns:
        bool: True if the metadata respects the forecast intervals, False otherwise.
    """
    # Handling case where forecast_filter is a single value
    if len(forecast_filter) == 1:
        # Return True if metadata contains the forecast value specified in the filter
        return metadata.count(forecast_filter[0]) > 0
    else:
        # Return True if metadata contains at least one value contained in the specified range of the filter
        for forecast in metadata:
            if forecast_filter[0] <= forecast <= forecast_filter[1]:
                return True
        return False


def check_meteo_variables(meteo_variable_filter: Dict, metadata: Dict) -> bool:
    """Verifies that the meteo variables are present.

    Args:
        meteo_variable_filter (Dict): The filters containing variable ranges to apply for the check.
        metadata (Dict): The metadata containing meteo variables to verify.

    Returns:
        bool: True if all variables in the filter are present in the metadata.
    """
    meteo_variables_metadata: List = metadata[METEO_VARIABLE_KEY]
    meteo_variables_names = []
    for var in meteo_variables_metadata:
        meteo_variables_names.append(var[NAME_KEY])

    for filter_variable in meteo_variable_filter:
        # Check if the variable is in the dataset's metadata
        if meteo_variables_names.count(filter_variable) < 1:
            return False
    return True
