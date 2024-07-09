# dataset_builder.py
# Module to build FAIR datasets.
import datetime
import gzip
import json
import logging
import os
import shutil
import tarfile
import textwrap
import uuid

import numpy as np
import xarray as xr

from ..catalog import catalog_manager as catalog
from ..check_dataset import check_dataset
from ..constants import (
    HADISD_VARIABLES_LIST,
    HADISD_ARCHIVE_EXTENSION,
    HADISD_CHECKSUMS_FILE,
    HADISD_STATION_INFO_FILE,
    GENERAL_METADATA_FILE_NAME,
    AROME_MODEL,
    ARPEGE_MODEL,
    CONTENT_METADATA_SUFFIX,
    ERA5_DATASETS,
    VERIFICATION_RESULTS_KEY,
    WGS84_SYSTEM,
    DATA_KEY,
    SOURCE_KEY,
    HADISD_KEY,
    CONTENT_METADATA,
    GENERAL_KEY,
    DATA_FILE_NAME_KEY,
    SPATIAL_REFERENCE_KEY,
    TIME_REFERENCE_KEY,
    DIMENSIONS_KEY,
    X_COORDINATE_KEY,
    Y_COORDINATE_KEY,
    Z_COORDINATE_KEY,
    T_REFERENCE_KEY,
    FORECAST_KEY,
    PROBABILISTIC_DIMENSION_KEY,
    NAME_KEY,
    STANDARD_NAME_KEY,
    UNIT_KEY,
    MIN_VALUE_KEY,
    MAX_VALUE_KEY,
    MISSING_VALUE_INDICATOR_KEY,
    MISSING_VALUE_INDICATOR_DEFINED_KEY,
    TOTAL_MISSING_VALUE_KEY,
    METEO_VARIABLE_KEY,
    LONG_NAME_ATTRIBUTE,
    STANDARD_NAME_ATTRIBUTE,
    UNIT_ATTRIBUTE,
    GRIB_MISSING_VALUE_ATTRIBUTE,
    VALID_MIN_ATTRIBUTE,
    VALID_MAX_ATTRIBUTE,
    FLAGGED_VALUE_ATTRIBUTE,
    GENERAL_METADATA,
    CATALOG_FILENAME,
    RELEASE_NOTES_FILENAME,
    DATE_FORMAT,
)
from ..utils import metadata

try:
    from mcapy import file_access
except ImportError as e:
    raise ImportError(
        "mcapy is required for dataset_builder module but is not installed."
    )


class DatasetBuilder:

    def __init__(self):
        self.dataset_path = None
        self.min_date = None
        self.max_date = None
        self.source = None
        self.file_format = None
        self.dataset_name = None
        self.dataset_creation_date = None
        self.content_metadata_array = None

    def build_dataset(self, data_path, name, final_path=None):
        """
        Main method to build a dataset from downloaded data.

        Args:
            data_path (str): Path to directory containing data to build dataset.
            name (str): Name of the dataset. Version is appended to dataset name : NAME_01.00.00
            final_path (str): Optional arg. Parent directory where the dataset will be built. If not provided, the
            dataset is built in the data directory.
        """

        # Check the content of the data directory
        self.check_dataset_content(data_path)
        # Create the dataset directory and the dataset path
        self.set_dataset_dir(data_path, name, final_path)

        # Copy file if needed and extract data from archives if a source is HadISD
        if final_path:
            self.move_data(data_path, self.dataset_path)
        if self.source.lower() == HADISD_KEY:
            self.extract_hadisd_archives(self.dataset_path)
            self.extract_hadisd_gz(self.dataset_path)

        # Generate content metadata json for each meteorological data file
        self.generate_content_metadata_file(
            self.dataset_path, data_source=self.source, data_format=self.file_format
        )

        # Update general metadata
        self.update_general_metadata(self.dataset_path)

        # Generate release notes
        self.generate_release_notes()

        # Process dataset validation
        self.process_dataset_validation()

    def set_dataset_dir(self, data_path, name, final_path=None):
        """
        Method to create new dataset directory.
        If a final path is not provided, the dataset is built in data directory.

        Args:
            data_path: Path to downloaded and created files using to build a dataset
            name: Name of the dataset
            final_path: Optional parameter to allow user to choose the directory where dataset will be built
        """
        # Dataset name
        self.dataset_name = name + "_01.00.00"
        # Define a dataset path and create or rename the dataset directory
        if final_path:
            self.dataset_path = os.path.join(final_path, self.dataset_name)
            if not os.path.exists(self.dataset_path):
                os.mkdir(self.dataset_path)
            else:
                message = f"Dataset path {self.dataset_path} already exists"
                logging.error(message)
                raise ValueError(message)
        else:
            self.dataset_path = os.path.join(
                os.path.dirname(data_path), self.dataset_name
            )
            os.rename(data_path, self.dataset_path)

    def check_dataset_content(self, data_path):
        """
        Method to check the content of data directory used to build dataset

        Args:
            data_path: Path to download and create files using to build a dataset
        """
        general_metadata_json_path = os.path.join(data_path, GENERAL_METADATA_FILE_NAME)
        if os.path.isfile(general_metadata_json_path):
            with open(general_metadata_json_path, "r") as f:
                general_metadata_json = json.load(f)
            self.source = general_metadata_json[DATA_KEY][SOURCE_KEY]
            self.check_data_file_format(data_path)
            if self.source.lower() == HADISD_KEY:
                self.check_hadisd_files(data_path)
        else:
            message = f"General metadata file not found in {data_path} directory"
            logging.error(message)
            raise FileNotFoundError(message)

    @staticmethod
    def move_data(data_path, dataset_path):
        files = os.listdir(data_path)
        for file in files:
            source_file_path = os.path.join(data_path, file)
            destination_file_path = os.path.join(dataset_path, file)
            shutil.copy(source_file_path, destination_file_path)

    def check_data_file_format(self, dir_path):
        """
        Method to check if meteorological data are .grib or .nc

        Args:
            dir_path: Path to download and create files using to build a dataset
        """
        file_found = False
        for filename in os.listdir(dir_path):
            if filename.endswith(HADISD_ARCHIVE_EXTENSION):
                tar_path = os.path.join(dir_path, filename)
                with tarfile.open(tar_path, "r:gz") as tar:
                    for tarinfo in tar:
                        if tarinfo.isfile() and tarinfo.name.endswith(".nc.gz"):
                            self.file_format = "nc"
                            file_found = True
                            break
            if filename.endswith(".nc"):
                self.file_format = "nc"
                file_found = True
                break
            elif filename.endswith(".grib"):
                self.file_format = "grib"
                file_found = True
                break
            elif filename.endswith(".grib2"):
                self.file_format = "grib2"
                file_found = True
                break
        if not file_found:
            message = f"No meteorological data found in {dir_path} directory"
            logging.error(message)
            raise FileNotFoundError(message)

    @staticmethod
    def check_hadisd_files(dir_path):
        """
        Method to check if dir contains stations list and stations metadata file

        Args:
            dir_path: Path to download and create files using to build a dataset
        """
        found_files = []

        for filename in os.listdir(dir_path):
            if (
                HADISD_STATION_INFO_FILE in filename
                or HADISD_CHECKSUMS_FILE in filename
            ):
                found_files.append(filename)

        if len(found_files) != 2:
            message = "Missing hadisd_station_info file or checksums file"
            logging.error(message)
            raise FileNotFoundError(message)

    @staticmethod
    def extract_hadisd_archives(dir_path):
        """
        Method to extract content of .tar.gz archives

        Args:
            dir_path: Path where archives are stored
        """
        total_archives = 0
        archives_extracted = 0

        for filename in os.listdir(dir_path):
            if filename.endswith(HADISD_ARCHIVE_EXTENSION):
                total_archives += 1
                tar_path = os.path.join(dir_path, filename)
                with tarfile.open(tar_path, "r:gz") as tar:
                    try:
                        tar.extractall(path=dir_path)
                    except tarfile.TarError as e:
                        logging.error(
                            f"Error during extraction of {tar_path} archive: {e}"
                        )
                    else:
                        archives_extracted += 1

        if archives_extracted == total_archives:
            for filename in os.listdir(dir_path):
                if filename.endswith(HADISD_ARCHIVE_EXTENSION):
                    os.remove(os.path.join(dir_path, filename))

    @staticmethod
    def extract_hadisd_gz(dir_path):
        """
        Function to extract the content of .gz archives.

        Args:
            dir_path (str): Path to the directory where archives are stored.
        """
        total_archives = 0
        archives_extracted = 0
        for gz_filename in os.listdir(dir_path):
            if gz_filename.endswith(".gz"):
                total_archives += 1
                gz_path = os.path.join(dir_path, gz_filename)
                with gzip.open(gz_path, "rb") as f_in:
                    try:
                        with open(
                            os.path.join(
                                dir_path, os.path.splitext(os.path.basename(gz_path))[0]
                            ),
                            "wb",
                        ) as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    except tarfile.TarError as e:
                        logging.error(
                            f"Error during extraction of {gz_path} archive: {e}"
                        )
                    else:
                        archives_extracted += 1

        if archives_extracted == total_archives:
            for filename in os.listdir(dir_path):
                if filename.endswith(".gz"):
                    os.remove(os.path.join(dir_path, filename))

    def generate_content_metadata_file(self, path, data_source, data_format):
        """
        Main method to generate content metadata file. Detects if the dataset contains .grib or .nc files and start
        generation for each meteorological file in the directory.

        Args:
             path (str): Path to the directory where data are stored.
             data_source (str): Source where meteorological data come from.
             data_format (str): Format of meteorological data files (grib or nc).
        """
        if data_format == "nc":
            format_extension = ".nc"
        elif data_format == "grib":
            format_extension = ".grib"
        elif data_format == "grib2":
            format_extension = ".grib2"
        else:
            message = f"Invalid data format : {data_format}"
            logging.error(message)
            raise ValueError(message)

        for file_name in os.listdir(path):
            if file_name.endswith(format_extension):
                self.complete_content_metadata(
                    os.path.join(path, file_name), data_source, data_format
                )

    def complete_content_metadata(self, file_path, data_source, data_format):
        """
        Method used to call the correct function to get metadata from meteorological files depending on the source.

        Args:
            file_path (str): Path to the meteorological data file for which metadata is generated.
            data_source (str): Source where meteorological data come from.
            data_format (str): Format of meteorological data files (grib or nc).
        """
        if data_source.lower() == HADISD_KEY:
            self.generate_content_metadata_hadisd(file_path)
        elif data_source in ERA5_DATASETS:
            self.generate_content_metadata_era5(file_path, data_format)
        elif data_source.lower() == AROME_MODEL or data_source.lower() == ARPEGE_MODEL:
            self.generate_content_metadata_mf(file_path)
        else:
            message = f"Invalid data source : {data_source}"
            logging.error(message)
            raise ValueError(message)

    def generate_content_metadata_era5(self, file_path, data_format):
        """
        Method used to complete the content metadata file for an ERA5 data file.

        Args:
            file_path (str): Path to the meteorological data file for which metadata is generated.
            data_format (str): Format of meteorological data files (grib or nc).
        """
        # Init content metadata json from template
        content_metadata_json = metadata.get_metadata_template(CONTENT_METADATA)

        # Read file content with MCAPY.
        ds = file_access.read(file_path)

        if data_format == "nc":
            content_metadata_json[GENERAL_KEY][DATA_FILE_NAME_KEY] = os.path.basename(
                file_path
            )
            content_metadata_json[GENERAL_KEY][SPATIAL_REFERENCE_KEY] = WGS84_SYSTEM
            content_metadata_json[GENERAL_KEY][TIME_REFERENCE_KEY] = "UTC"
            content_metadata_json[DIMENSIONS_KEY][X_COORDINATE_KEY] = [
                float(min(ds[0].longitude.data)),
                float(max(ds[0].longitude.data)),
            ]
            content_metadata_json[DIMENSIONS_KEY][Y_COORDINATE_KEY] = [
                float(min(ds[0].latitude.data)),
                float(max(ds[0].latitude.data)),
            ]
            if "level" in ds[0].coords:
                data = ds[0].level.data
            else:
                data = [0]
            content_metadata_json[DIMENSIONS_KEY][Z_COORDINATE_KEY] = [
                float(min(data)),
                float(max(data)),
            ]
            content_metadata_json[DIMENSIONS_KEY][T_REFERENCE_KEY] = [
                self.format_date(str(ds[0].time.data[0])),
                self.format_date(str(ds[0].time.data[-1])),
            ]
            content_metadata_json[DIMENSIONS_KEY][FORECAST_KEY] = [0]
            content_metadata_json[DIMENSIONS_KEY][PROBABILISTIC_DIMENSION_KEY] = [0]

            self.update_data_time_interval(
                self.format_date(str(ds[0].time.data[0])),
                self.format_date(str(ds[0].time.data[-1])),
            )

            for index, variable in enumerate(file_access.info(ds[0], info="getVars")):
                variable_attribute_list = file_access.info(
                    ds[0], variable=variable, info="getVariableAttrs"
                )

                new_variable = {
                    NAME_KEY: variable_attribute_list[LONG_NAME_ATTRIBUTE],
                    STANDARD_NAME_KEY: "unspecified",
                    UNIT_KEY: variable_attribute_list[UNIT_ATTRIBUTE],
                    MIN_VALUE_KEY: float(np.min(getattr(ds[0], variable).data)),
                    MAX_VALUE_KEY: float(np.max(getattr(ds[0], variable).data)),
                    MISSING_VALUE_INDICATOR_KEY: "unspecified",
                    MISSING_VALUE_INDICATOR_DEFINED_KEY: False,
                    TOTAL_MISSING_VALUE_KEY: -1,
                }

                if STANDARD_NAME_ATTRIBUTE in ds[0].variables[variable].attrs:
                    new_variable.update(
                        {
                            STANDARD_NAME_KEY: ds[0]
                            .variables[variable]
                            .attrs[STANDARD_NAME_ATTRIBUTE]
                        }
                    )

                content_metadata_json[DIMENSIONS_KEY][METEO_VARIABLE_KEY].append(
                    new_variable
                )

        elif data_format == "grib":
            content_metadata_json[GENERAL_KEY][DATA_FILE_NAME_KEY] = os.path.basename(
                file_path
            )
            content_metadata_json[GENERAL_KEY][SPATIAL_REFERENCE_KEY] = WGS84_SYSTEM
            content_metadata_json[GENERAL_KEY][TIME_REFERENCE_KEY] = "UTC"
            content_metadata_json[DIMENSIONS_KEY][X_COORDINATE_KEY] = [
                float(min(ds[0].longitude.data)),
                float(max(ds[0].longitude.data)),
            ]
            content_metadata_json[DIMENSIONS_KEY][Y_COORDINATE_KEY] = [
                float(min(ds[0].latitude.data)),
                float(max(ds[0].latitude.data)),
            ]
            content_metadata_json[DIMENSIONS_KEY][Z_COORDINATE_KEY] = [
                float(min(ds[0].isobaricInhPa.data)),
                float(max(ds[0].isobaricInhPa.data)),
            ]
            content_metadata_json[DIMENSIONS_KEY][T_REFERENCE_KEY] = [
                self.format_date(str(ds[0].time.data[0])),
                self.format_date(str(ds[0].time.data[-1])),
            ]
            content_metadata_json[DIMENSIONS_KEY][FORECAST_KEY] = [0]
            content_metadata_json[DIMENSIONS_KEY][PROBABILISTIC_DIMENSION_KEY] = [0]

            self.update_data_time_interval(
                self.format_date(str(ds[0].time.data[0])),
                self.format_date(str(ds[0].time.data[-1])),
            )

            for index, variable in enumerate(file_access.info(ds[0], info="getVars")):
                variable_attribute_list = file_access.info(
                    ds[0], variable=variable, info="getVariableAttrs"
                )

                new_variable = {
                    NAME_KEY: variable_attribute_list[LONG_NAME_ATTRIBUTE],
                    STANDARD_NAME_KEY: variable_attribute_list[STANDARD_NAME_ATTRIBUTE],
                    UNIT_KEY: variable_attribute_list[UNIT_ATTRIBUTE],
                    MIN_VALUE_KEY: float(np.min(getattr(ds[0], variable).data)),
                    MAX_VALUE_KEY: float(np.max(getattr(ds[0], variable).data)),
                    MISSING_VALUE_INDICATOR_KEY: variable_attribute_list[
                        GRIB_MISSING_VALUE_ATTRIBUTE
                    ],
                    MISSING_VALUE_INDICATOR_DEFINED_KEY: True,
                    TOTAL_MISSING_VALUE_KEY: np.count_nonzero(
                        getattr(ds[0], variable).data
                        == variable_attribute_list[GRIB_MISSING_VALUE_ATTRIBUTE]
                    ),
                }

                content_metadata_json[DIMENSIONS_KEY][METEO_VARIABLE_KEY].append(
                    new_variable
                )

        # Save json object to json file
        with open(
            os.path.join(
                os.path.dirname(file_path),
                os.path.splitext(os.path.basename(file_path))[0]
                + CONTENT_METADATA_SUFFIX,
            ),
            "w",
        ) as f:
            json.dump(content_metadata_json, f, indent=4)

    def generate_content_metadata_hadisd(self, file_path):
        """
        Method used to complete the content metadata file for an HadISD data file.

        Args:
            file_path (str): Path to the meteorological data file for which metadata is generated.
        """
        # Init content metadata json from template
        content_metadata_json = metadata.get_metadata_template(CONTENT_METADATA)

        # Read file content with MCAPY
        ds = xr.open_dataset(file_path)

        content_metadata_json[GENERAL_KEY][DATA_FILE_NAME_KEY] = os.path.basename(
            file_path
        )
        content_metadata_json[GENERAL_KEY][SPATIAL_REFERENCE_KEY] = WGS84_SYSTEM
        content_metadata_json[GENERAL_KEY][TIME_REFERENCE_KEY] = "UTC"
        content_metadata_json[DIMENSIONS_KEY][X_COORDINATE_KEY] = [
            float(min(ds.longitude.data))
        ]
        content_metadata_json[DIMENSIONS_KEY][Y_COORDINATE_KEY] = [
            float(min(ds.latitude.data))
        ]
        content_metadata_json[DIMENSIONS_KEY][Z_COORDINATE_KEY] = [
            float(min(ds.elevation.data))
        ]
        content_metadata_json[DIMENSIONS_KEY][T_REFERENCE_KEY] = [
            self.format_date(str(ds.time.data[0])),
            self.format_date(str(ds.time.data[-1])),
        ]
        content_metadata_json[DIMENSIONS_KEY][FORECAST_KEY] = [0]
        content_metadata_json[DIMENSIONS_KEY][PROBABILISTIC_DIMENSION_KEY] = [-1]

        self.update_data_time_interval(
            self.format_date(str(ds.time.data[0])),
            self.format_date(str(ds.time.data[-1])),
        )

        for index, variable in enumerate(HADISD_VARIABLES_LIST):
            new_variable = {
                NAME_KEY: ds.variables[variable].attrs[LONG_NAME_ATTRIBUTE],
                STANDARD_NAME_KEY: "unspecified",
                UNIT_KEY: ds.variables[variable].attrs[UNIT_ATTRIBUTE],
                MIN_VALUE_KEY: float(ds.variables[variable].attrs[VALID_MIN_ATTRIBUTE]),
                MAX_VALUE_KEY: float(ds.variables[variable].attrs[VALID_MAX_ATTRIBUTE]),
                TOTAL_MISSING_VALUE_KEY: -1,
            }

            if STANDARD_NAME_ATTRIBUTE in ds.variables[variable].attrs:
                new_variable.update(
                    {
                        STANDARD_NAME_KEY: ds.variables[variable].attrs[
                            STANDARD_NAME_ATTRIBUTE
                        ]
                    }
                )

            if FLAGGED_VALUE_ATTRIBUTE in ds.variables[variable].attrs:
                new_variable.update(
                    {
                        MISSING_VALUE_INDICATOR_KEY: float(
                            ds.variables[variable].attrs[FLAGGED_VALUE_ATTRIBUTE]
                        ),
                        MISSING_VALUE_INDICATOR_DEFINED_KEY: True,
                        TOTAL_MISSING_VALUE_KEY: np.count_nonzero(
                            ds.variables[variable].data
                            == ds.variables[variable].attrs[FLAGGED_VALUE_ATTRIBUTE]
                        ),
                    }
                )
            else:
                new_variable.update(
                    {
                        MISSING_VALUE_INDICATOR_KEY: "unspecified",
                        MISSING_VALUE_INDICATOR_DEFINED_KEY: False,
                    }
                )

            content_metadata_json[DIMENSIONS_KEY][METEO_VARIABLE_KEY].append(
                new_variable
            )

        # Save json object to json file

        with open(
            os.path.join(
                os.path.dirname(file_path),
                os.path.splitext(os.path.basename(file_path))[0]
                + "_content_metadata.json",
            ),
            "w",
        ) as f:
            json.dump(content_metadata_json, f, indent=4)

    def generate_content_metadata_mf(self, file_path):
        """
        Method used to complete the content metadata file for Meteo France data file.

        Args:
            file_path (str): Path to the meteorological data file for which metadata is generated.
        """
        # Init content metadata json from template
        content_metadata_json = metadata.get_metadata_template(CONTENT_METADATA)

        # Read file content with MCAPY
        ds = file_access.read(file_path)

        content_metadata_json[GENERAL_KEY][DATA_FILE_NAME_KEY] = os.path.basename(
            file_path
        )
        content_metadata_json[GENERAL_KEY][SPATIAL_REFERENCE_KEY] = WGS84_SYSTEM
        content_metadata_json[GENERAL_KEY][TIME_REFERENCE_KEY] = "UTC"
        content_metadata_json[DIMENSIONS_KEY][X_COORDINATE_KEY] = [
            float(min(ds[0].longitude.data)),
            float(max(ds[0].longitude.data)),
        ]
        content_metadata_json[DIMENSIONS_KEY][Y_COORDINATE_KEY] = [
            float(min(ds[0].latitude.data)),
            float(max(ds[0].latitude.data)),
        ]
        if "heightAboveGround" in ds[0].coords:
            data = ds[0].heightAboveGround.data
        else:
            data = np.array(0)

        if data.ndim == 1:
            content_metadata_json[DIMENSIONS_KEY][Z_COORDINATE_KEY] = [
                float(min(data)),
                float(max(data)),
            ]
        else:
            content_metadata_json[DIMENSIONS_KEY][Z_COORDINATE_KEY] = [float(data)]
        if ds[0].time.data.ndim == 1:
            content_metadata_json[DIMENSIONS_KEY][T_REFERENCE_KEY] = [
                self.format_date(str(ds[0].time.data[0])),
                self.format_date(str(ds[0].time.data[-1])),
            ]
            self.update_data_time_interval(
                self.format_date(str(ds[0].time.data[0])),
                self.format_date(str(ds[0].time.data[-1])),
            )
        elif ds[0].time.data.ndim == 0:
            content_metadata_json[DIMENSIONS_KEY][T_REFERENCE_KEY] = [
                self.format_date(str(ds[0].time.data)),
                self.format_date(
                    str(
                        self.add_timedelta_to_date(
                            str(ds[0].time.data), ds[0].step.data[-1]
                        )
                    )
                ),
            ]
            self.update_data_time_interval(
                self.format_date(str(ds[0].time.data)),
                self.format_date(
                    str(
                        self.add_timedelta_to_date(
                            str(ds[0].time.data), ds[0].step.data[-1]
                        )
                    )
                ),
            )
        content_metadata_json[DIMENSIONS_KEY][FORECAST_KEY] = (
            (ds[0].step.data / np.timedelta64(1, "h")).astype(int).tolist()
        )
        content_metadata_json[DIMENSIONS_KEY][PROBABILISTIC_DIMENSION_KEY] = [0]

        for index, variable in enumerate(file_access.info(ds[0], info="getVars")):
            variable_attribute_list = file_access.info(
                ds[0], variable=variable, info="getVariableAttrs"
            )

            new_variable = {
                NAME_KEY: variable_attribute_list[LONG_NAME_ATTRIBUTE],
                STANDARD_NAME_KEY: variable_attribute_list[STANDARD_NAME_ATTRIBUTE],
                UNIT_KEY: variable_attribute_list[UNIT_ATTRIBUTE],
                MIN_VALUE_KEY: float(np.nanmin(getattr(ds[0], variable).data)),
                MAX_VALUE_KEY: float(np.nanmax(getattr(ds[0], variable).data)),
                MISSING_VALUE_INDICATOR_KEY: variable_attribute_list[
                    GRIB_MISSING_VALUE_ATTRIBUTE
                ],
                MISSING_VALUE_INDICATOR_DEFINED_KEY: True,
                TOTAL_MISSING_VALUE_KEY: int(
                    np.sum(
                        getattr(ds[0], variable).data
                        == variable_attribute_list[GRIB_MISSING_VALUE_ATTRIBUTE]
                    )
                    + np.sum(np.isnan(getattr(ds[0], variable).data))
                ),
            }

            content_metadata_json[DIMENSIONS_KEY][METEO_VARIABLE_KEY].append(
                new_variable
            )

        # Save json object to json file
        with open(
            os.path.join(
                os.path.dirname(file_path),
                os.path.splitext(os.path.basename(file_path))[0]
                + CONTENT_METADATA_SUFFIX,
            ),
            "w",
        ) as f:
            json.dump(content_metadata_json, f, indent=4)

    @staticmethod
    def format_date(date):
        """
        Function to format date from %Y-%m-%dT%H:%M:%S.%f to %Y%m%d:%H%M format

        Args:
            date (str): Date to format
        """
        date_obj = datetime.datetime.strptime(date[:-3], "%Y-%m-%dT%H:%M:%S.%f")
        date = date_obj.strftime("%Y%m%d:%H%M%S")
        return date

    @staticmethod
    def add_timedelta_to_date(date, timedelta):
        """
        Function to add timedelta to date

        Args:
            date (str): Reference date
            timedelta (float): Time delta to add to date
        """
        date_obj = datetime.datetime.strptime(date[:-3], "%Y-%m-%dT%H:%M:%S.%f")
        delta = datetime.timedelta(hours=(timedelta / np.timedelta64(1, "h")))
        date = date_obj + delta
        return date.strftime("%Y-%m-%dT%H:%M:%S.%f")

    def update_general_metadata(self, dataset_path):
        """
        Method to update general metadata file after dataset building

        Args:
            dataset_path (str): Path to dataset directory
        """
        general_metadata_path = os.path.join(dataset_path, GENERAL_METADATA_FILE_NAME)
        json_schema = metadata.get_metadata_schema(GENERAL_METADATA)

        with open(general_metadata_path, "r") as f:
            general_metadata_json = json.load(f)

        data = {}

        self.dataset_creation_date = datetime.datetime.now().strftime(DATE_FORMAT)

        data.update(
            {
                "dataset.path": self.dataset_path,
                "dataset.name": self.dataset_name,
                "dataset.uuid": str(uuid.uuid5(uuid.NAMESPACE_DNS, self.dataset_name)),
                "dataset.size-go": self.get_dataset_size(dataset_path),
                "dataset.file-number": self.get_file_number(self.dataset_path),
                "dataset.last-modification-date": self.dataset_creation_date,
                "data.time-range.start": self.min_date,
                "data.time-range.end": self.max_date,
                "checksums-reference": "checksums_generated.txt",
                "releasenotes-reference": "releases_notes.md",
            }
        )

        general_metadata_json = metadata.update_metadata_file(
            general_metadata_json, json_schema, data
        )

        # Save json object to json file
        with open(os.path.join(dataset_path, GENERAL_METADATA_FILE_NAME), "w") as f:
            json.dump(general_metadata_json, f, indent=4)

    @staticmethod
    def get_dataset_size(dataset_path):
        """
        Function to get the total size of dataset in Go.

        Args:
            dataset_path (str): Path to dataset directory.
        """
        total_size = 0

        for directory, sub_directory, files in os.walk(dataset_path):
            for file in files:
                file_path = os.path.join(directory, file)
                total_size += os.path.getsize(file_path)

        return round(total_size / (1024**3), 4)

    @staticmethod
    def get_file_number(dataset_path):
        """
        Function to get numbers of files in dataset.

        Args:
            dataset_path (str): Path to dataset directory.
        """
        file_number = 0

        for directory, sub_directory, files in os.walk(dataset_path):
            file_number += len(files)

        return str(file_number)

    def update_data_time_interval(self, min_date, max_date):
        """
        Method to update the date time interval in general metadata file. Based on the min date and the max date find
        from each data file.

        Args:
            min_date (str): Min date.
            max_date (str): Max date.
        """
        min_date_obj = datetime.datetime.strptime(min_date, "%Y%m%d:%H%M%S")
        max_date_obj = datetime.datetime.strptime(max_date, "%Y%m%d:%H%M%S")

        if self.min_date is not None:
            current_min_date_obj = datetime.datetime.strptime(
                self.min_date, DATE_FORMAT
            )
            if current_min_date_obj - min_date_obj > datetime.timedelta(minutes=1):
                self.min_date = min_date_obj.strftime(DATE_FORMAT)
        else:
            self.min_date = min_date_obj.strftime(DATE_FORMAT)

        if self.max_date is not None:
            current_max_date_obj = datetime.datetime.strptime(
                self.max_date, DATE_FORMAT
            )
            if min_date_obj - current_max_date_obj > datetime.timedelta(minutes=1):
                self.max_date = max_date_obj.strftime(DATE_FORMAT)
        else:
            self.max_date = max_date_obj.strftime(DATE_FORMAT)

    def generate_release_notes(self):
        """
        Method used to generate the release notes file.
        """

        content = f"""
        # Release Notes
        ## Dataset {self.dataset_name}
        * Source : {self.source}
        * Data format : {self.file_format}
        ### Version 01.00.00
        * Dataset created : {self.dataset_creation_date}
        """

        with open(
            os.path.join(self.dataset_path, RELEASE_NOTES_FILENAME),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(textwrap.dedent(content))

    def process_dataset_validation(self):
        """
        Method to process multiples validation test.
        """

        # Get general metadata content from JSON file
        general_metadata_path = os.path.join(
            self.dataset_path, GENERAL_METADATA_FILE_NAME
        )
        with open(general_metadata_path, "r") as f:
            general_metadata = json.load(f)

        # Get verification results
        verification_results = check_dataset.validate_dataset(general_metadata)
        # Update general metadata with results
        general_metadata[VERIFICATION_RESULTS_KEY] = verification_results
        with open(general_metadata_path, "w") as file:
            json.dump(general_metadata, file, indent=4)
            logging.info("General metadata updated with verification results.")

        # Update catalog
        catalog.update_catalog(
            os.path.join(os.path.dirname(self.dataset_path), str(CATALOG_FILENAME)),
            general_metadata,
        )
