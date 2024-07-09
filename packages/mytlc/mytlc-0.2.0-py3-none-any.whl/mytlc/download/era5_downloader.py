# era5_downloader.py
# Module to download ERA5 data with CDS API.

import datetime
import hashlib
import json
import logging
import os
import time

import cdsapi

from ..constants import (
    ERA5_DATASETS,
    ERA5_FORMAT,
    ERA5_PRESSURE_LEVELS_LIST,
    ERA5_SINGLE_LEVEL_LIST,
    PRESSURE_LEVELS_VARIABLES,
    PRESSURE_LEVELS,
    SINGLE_LEVELS_VARIABLES,
)
from ..utils import metadata as metadata


class Era5Downloader:

    def __init__(self):
        self.data_url = None
        self.data_path = None
        self.download_date = None
        self.download_url = None
        self.file_format = None
        self.dataset = None

    def download_era5_data(self, parameters, path, metadata_file=None):
        """
        Download ERA5 data with CDS API.
        Provided parameters dictionary contains the following elements:
            - dataset (str): reanalysis-era5-pressure-levels or reanalysis-era5-single-levels.
            - variable (list): List of meteorological variables depending on the selected dataset .
            - pressure_level (list): Optional parameter. List of pressure levels if pressure levels dataset.
            - start_date (str): Date from which the data must be downloaded following the format : YYYYMM
            (YYYY: Year, MM: Month). Date must be selected after 1940 and 1 month before the current date.
            - end_date (str): Date until which the data must be downloaded following the format : YYYYMM
            (YYYY: Year, MM: Month). Date must be selected after 1940 and 1 month before the current date.
            - coordinate (list): Min and max longitude (in the range [-180;180] referenced to Greenwich Prime Meridian)
             and latitude (in the range [-90;90] referenced to the equator) in decimal degrees.
            - format (str): Data file format : grib or netcdf.

        Example :
        parameters = {
            'dataset': 'reanalysis-era5-pressure-levels',
            'variable': ['divergence', 'temperature'],
            'pressure_level': ['100', '200'],
            'start_date': '202302',
            'end_date': '202401',
            'coordinate': [0.25, 10, -10, 15.5],
            'format': 'netcdf'
        }

        Args:
            parameters (dict): API request parameters
            metadata_file (str): Text file containing metadata specified in the file to completing general metadata file
            path (str): Path to directory where files are downloaded and created
        """
        # Check parameters
        self.check_request_parameters(parameters)

        # Check metadata text file
        if metadata_file:
            metadata.check_metadata_text_file(metadata_file)

        # Assign attribute to complete metadata file
        self.file_format = parameters["format"]
        self.dataset = parameters["dataset"]

        # From parameters, call formatting_parameters to generate multiple sub requests instead of single request
        formatted_parameters = self.formatting_parameters(parameters)

        # Init CDS API Client
        cds = cdsapi.Client(sleep_max=10)

        # Request the API
        self.handle_api_request(cds, parameters, formatted_parameters, path)

        # Generate the general metadata file with partial completion
        self.generate_general_metadata_file(path, metadata_file)

        # Generate md5 checksums file
        self.generate_md5_checksums_file(path)

    def check_request_parameters(self, parameters):
        """
        Method to check parameters furnished by the user according to CDS API

        Args:
            parameters (dict): Dict of parameters to check
        Returns:
            check_bool (bool): Boolean equal to True if parameters are valid
        """
        # Parameters dict must contain specific keys
        if parameters["dataset"] == ERA5_DATASETS[0]:
            for element in ERA5_PRESSURE_LEVELS_LIST:
                if element not in parameters:
                    message = f"Parameter '{element}' is missing"
                    logging.error(message)
                    raise ValueError(message)
            self.check_parameters_content(parameters, PRESSURE_LEVELS_VARIABLES)
        elif parameters["dataset"] == ERA5_DATASETS[1]:
            for element in ERA5_SINGLE_LEVEL_LIST:
                if element not in parameters:
                    message = f"Parameter '{element}' is missing"
                    logging.error(message)
                    raise ValueError(message)
            self.check_parameters_content(parameters, SINGLE_LEVELS_VARIABLES)
        else:
            message = "Parameter 'dataset' is invalid or missing"
            logging.error(message)
            raise ValueError(message)

    def check_parameters_content(self, parameters, variable_list):
        """
        Method used to check if request parameters are valid

        Args:
            parameters (dict): Dict of parameters
            variable_list (list): List containing all allowed parameters
        """
        # Check if variables are valid value accepted by CDS API
        for element in parameters["variable"]:
            if element not in variable_list:
                message = f"Invalid variable : '{element}'"
                logging.error(message)
                raise ValueError(message)
        # Check if pressure levels are valid value accepted by CDS API
        if "pressure_level" in parameters:
            for element in parameters["pressure_level"]:
                if element not in PRESSURE_LEVELS:
                    message = f"Invalid pressure level : '{element}'"
                    logging.error(message)
                    raise ValueError(message)
        # Check if format is valid value accepted by CDS API
        if parameters["format"] not in ERA5_FORMAT:
            message = "Invalid format"
            logging.error(message)
            raise ValueError(message)

        self.check_date_parameter(parameters)

        self.check_coordinate_parameter(parameters)

    @staticmethod
    def check_date_parameter(parameters):
        """
        Function to check if start_date and end_date are valid

        Args:
            parameters (dict): Dict of parameters
        """
        # Check if start date begin from 1940
        min_date = datetime.datetime.strptime(parameters["start_date"], "%Y%m")
        if min_date.year < 1940:
            message = "Start date must be greater than or equal to 1940"
            logging.error(message)
            raise ValueError(message)
        max_date = datetime.datetime.strptime(parameters["end_date"], "%Y%m")
        # Check if end_date is greater than start_date
        if max_date - min_date < datetime.timedelta(hours=0):
            message = "end_date must be greater than start_date"
            logging.error(message)
            raise ValueError(message)
        # Check if end date stop 6 days before current date
        if datetime.datetime.today().date() - max_date.date() < datetime.timedelta(
                days=6
        ):
            message = "End date must be inferior than 6 days compare to current date"
            logging.error(message)
            raise ValueError(message)

    @staticmethod
    def check_coordinate_parameter(parameters):
        """
        Function to check if coordinates are valid

        Args:
            parameters (dict): Dict of parameters
        """
        # Check if coordinates are defined and within valid intervals
        if len(parameters["coordinate"]) != 4:
            message = "'coordinate' parameter must contain 4 coordinates"
            logging.error(message)
            raise ValueError(message)
        if not (-180 <= parameters["coordinate"][0] <= 180) and (
                -180 <= parameters["coordinate"][1] <= 180
        ):
            message = "Longitude coordinates must be between -180 and 180 degrees"
            logging.error(message)
            raise ValueError(message)
        if not (-90 <= parameters["coordinate"][2] <= 90) and (
                -90 <= parameters["coordinate"][3] <= 90
        ):
            message = "Longitude coordinates must be between -90 and 90 degrees"
            logging.error(message)
            raise ValueError(message)

    def formatting_parameters(self, parameters):
        """
        Method used to split parameters furnished by user to set up multiple requests respecting same organisation rules.
        Request are organised by meteorological parameter and by month.

        Args:
            parameters (dict): All parameters furnished by user
        Return:
            formatted_parameters (list): List of dict of parameters (one dict of parameters for each request)
        """
        formatted_parameters = []

        min_date = datetime.datetime.strptime(parameters["start_date"], "%Y%m")
        max_date = datetime.datetime.strptime(parameters["end_date"], "%Y%m")

        date_ranges = []

        current_month_start = min_date.replace(day=1)
        while current_month_start <= max_date:
            next_month_start = current_month_start.replace(day=1) + datetime.timedelta(
                days=32
            )
            next_month_start = next_month_start.replace(day=1)
            current_month_end = next_month_start - datetime.timedelta(days=1)

            date_ranges.append(current_month_end)

            current_month_start = next_month_start

        # Filling a list with each hour from 0h to 23h
        # And formatting each hour as 'hh:00'
        time_list = list(range(0, 24, 1))
        for element in time_list:
            time_list[time_list.index(element)] = str("{:02d}".format(element)) + ":00"

        # Formatting area according to CDS API
        area = [
            parameters["coordinate"][3],
            parameters["coordinate"][0],
            parameters["coordinate"][2],
            parameters["coordinate"][1],
        ]

        if "pressure_level" in parameters:
            pressure_level = parameters["pressure_level"]
        else:
            pressure_level = None

        # For each meteorological parameter we're creating a new request for each date in date list
        for element in parameters["variable"]:
            for date in date_ranges:
                days_list = []
                for i in range(1, date.day + 1):
                    days_list.append(str("{:02d}".format(i)))
                formatted_parameters.append(
                    self.generate_request(
                        format=parameters["format"],
                        variable=element,
                        year=str(date.year),
                        month=str("{:02d}".format(date.month)),
                        day=days_list,
                        time=time_list,
                        area=area,
                        pressure_level=pressure_level,
                    )
                )

        return formatted_parameters

    def handle_api_request(self, cds, parameters, formatted_parameters, path):
        """
        Method to request the CDS API with selected parameters

        Args:
            cds (Client): Instanced CDS client to request API
            parameters (dict): Dict of parameters provided by user
            formatted_parameters (list): List of dict of parameters formatted to request data by month and by variable.
            path (str): Parent directory path where data are downloaded
        """
        # Request CDS database with each element of formatted_parameters
        for request_parameters in formatted_parameters:
            filepath = os.path.join(path, self.file_name(request_parameters))
            r = cds.retrieve(parameters["dataset"], request_parameters)
            self.process_request(r, filepath, path)

    @staticmethod
    def process_request(r, file_path, path):
        """
        Request processing

        Args:
            r (result): Result of the request
            file_path (str): Path of the data file
            path (str): Parent directory path where data are downloaded
        """
        while True:
            r.update()
            reply = r.reply
            r.info("Request ID: %s, state: %s" % (reply["request_id"], reply["state"]))
            # If the request is completed (download ready), download start
            if reply["state"] == "completed":
                if not os.path.exists(path):
                    os.mkdir(path)
                r.download(f"{file_path}")
                break
            # If the request has state queued or running, waiting processing from API
            elif reply["state"] in ("queued", "running"):
                r.info("Request ID: %s, sleep: %s", reply["request_id"], 15)
                time.sleep(15)
            # If the request fails, error is sent
            elif reply["state"] in ("failed",):
                r.error("Message: %s", reply["error"].get("message"))
                r.error("Reason:  %s", reply["error"].get("reason"))
                for n in (
                        reply.get("error", {})
                                .get("context", {})
                                .get("traceback", "")
                                .split("\n")
                ):
                    if n.strip() == "":
                        break
                    r.error("  %s", n)
                logging.info(
                    "%s. %s."
                    % (reply["error"].get("message"), reply["error"].get("reason"))
                )

    @staticmethod
    def generate_request(
            format, variable, year, month, day, time, area, pressure_level=None
    ):
        """
        Method to filling a dict used as parameter to retrieve ERA5 data.

        Args:
            format: File of format resulting from request
            variable: Meteorological parameter
            year: Year
            month: Month
            day: Day
            time: Time
            area: Geographical area
            pressure_level: Height for ERA5 hourly data on pressure levels
        """
        request_dict = {
            "product_type": "reanalysis",
            "format": format,
            "variable": variable,
            "year": year,
            "month": month,
            "day": day,
            "time": time,
            "area": area,
        }
        if pressure_level:
            request_dict.update({"pressure_level": pressure_level})
        return request_dict

    @staticmethod
    def file_name(request_parameters):
        """
        Method to generate à file name for each data requested (YEAR_MONTH_VARIABLE)

        Args:
            request_parameters (dict): Dict containing parameters of the request used to generate a name

        Return:
            file_name (str): Return the generated file_name
        """
        file_name = (
                request_parameters["year"]
                + "_"
                + request_parameters["month"]
                + "_"
                + request_parameters["variable"]
        )
        if request_parameters["format"] == "netcdf":
            file_name = file_name + ".nc"
        if request_parameters["format"] == "grib":
            file_name = file_name + ".grib"
        return file_name

    def generate_general_metadata_file(self, path, metadata_file=None):
        """
        Method to create and complete general metadata file

        Args:
            path (str): Path to directory where general metadata file must be stored
            metadata_file (str): Text file completed by user to add specific metadata to general metadata file
        """

        # Initialisation of general metadata json and json schema from templates
        json_template = metadata.get_metadata_template("general_metadata")
        json_schema = metadata.get_metadata_schema("general_metadata")

        # Init and completion of data to update general metadata json
        data = {}
        doi = "unspecified"
        quote = ""
        if self.dataset == ERA5_DATASETS[0]:
            doi = "10.24381/cds.bd0915c6"
            quote = "pressure levels"
        elif self.dataset == ERA5_DATASETS[1]:
            doi = "10.24381/cds.adbb2d47"
            quote = "single levels"

        data.update(
            {
                "data.protection-level": "NP",
                "data.source": self.dataset,
                "data.source-url": "https://cds.climate.copernicus.eu/api/v2/",
                "data.download-date": datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "data.format-reference": self.file_format,
                "data.data-license": "https://cds.climate.copernicus.eu/api/v2/terms/static/licence-to-use-copernicus"
                                     "-products.pdf",
                "data.license-quote": "Generated using Copernicus Climate Change Service information "
                                      + datetime.datetime.now().strftime("%Y")
                                      + " and/or generated using Copernicus Atmosphere Monitoring Service Information "
                                      + datetime.datetime.now().strftime("%Y")
                                      + "Hersbach, H., Bell, B., Berrisford, P., Biavati, G., Horányi, A., "
                                        "Muñoz Sabater, J., Nicolas, J., Peubey, C., Radu, R., Rozum, I., Schepers, D., "
                                        "Simmons, A., Soci, C., Dee, D., Thépaut, J-N. (2023): ERA5 hourly data on "
                                      + quote
                                      + " from 1940 to present. Copernicus Climate Change Service (C3S) "
                                        "Climate Data Store (CDS), DOI: "
                                      + doi
                                      + " (Accessed on "
                                      + datetime.datetime.now().strftime("%d-%m-%Y")
                                      + "). Neither the European Commission nor ECMWF is responsible for any use that "
                                        "may be made of the Copernicus information or data it contains.",
                "data.license-doi": doi,
            }
        )

        if metadata_file:
            with open(metadata_file, "r") as f:
                for line in f:
                    # Split line in file in two parts: checksum and filename
                    key, value = line.strip().split(":", 1)
                    data.update({key: value})

        general_metadata_json = metadata.update_metadata_file(
            json_template, json_schema, data
        )

        # Save json object to json file
        with open(
                os.path.join(path, "general_metadata.json"), "w", encoding="utf-8"
        ) as f:
            json.dump(general_metadata_json, f, indent=4, ensure_ascii=False)
            logging.info("General metadata generated")

    def generate_md5_checksums_file(self, path):
        """
        Method to generate a MD5 checksums file with .nc downloaded files.

        Args:
            path (str): Working directory
        """
        with open(os.path.join(path, "checksums_generated.txt"), "w") as f:
            for root, dirs, files in os.walk(path):
                for file in files:
                    # Check if the file is a netCDF
                    if file.endswith(".nc"):
                        file_path = os.path.join(root, file)
                        # Calculate MD5 checksum for the find file
                        md5_hexdigest = self.calculate_checksums(file_path)
                        f.write(f"{md5_hexdigest} {file}\n")
        logging.info("Checksums generated")

    @staticmethod
    def calculate_checksums(file_path):
        """
        Method to calculate MD5 checksum of file

        Args:
            file_path (str): Path to file whose checksum must be calculated
        """
        md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
        return md5.hexdigest()
