# hadisd_downloader.py
# Module to download HadISD data.

import datetime
import hashlib
import json
import logging
import os.path
import re

import urllib3
from urllib3.exceptions import LocationParseError, HTTPError

from ..utils import metadata

# Regex used to parse HadISD files
HADISD_DATA_REGEX = r"WMO_\d{6}-\d{6}\.tar.gz"

# URL to HadISD website
HADISD_URL = "https://www.metoffice.gov.uk/hadobs/hadisd/"


class HadisdDownloader:
    """
    Class allowing downloading of HadISD data
    """

    def __init__(self):
        self.url_version = None
        self.checksums_url = None
        self.metadata_url = None
        self.data_url = None
        self.checksums_path = None
        self.metadata_path = None
        self.data_path = None
        self.download_date = None
        self.http = urllib3.PoolManager()

    def download_data(self, data_version, path, metadata_file=None, sample=False):
        """
        Main method to call to download the entire HadISD dataset for a specific version.

        Args:
            data_version : Version of the HadISD dataset
            metadata_file : Text file containing metadata specified in the file to completing general metadata file
            path : Path to directory where files are downloaded and created
            sample (bool): If True, download the first archive only for testing purposes
        """
        # Init url and path used by the method
        self.init_url(data_version)
        self.init_path(data_version, path)

        # Download checksums
        self.download_checksums()

        # Download stations metadata
        self.download_metadata()

        # Download archives
        self.download_archives(path, sample)

        # Get date where data are downloaded
        self.download_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Generate the general metadata file with partial completion
        self.generate_general_metadata_file(data_version, path, metadata_file)

        # Generate md5 checksums file
        self.generate_md5_checksums_file(HADISD_DATA_REGEX, path)

        # Check archives integrity
        self.compare_checksums(
            self.checksums_path, os.path.join(path, "checksums_generated.txt")
        )

    def init_url(self, data_version):
        """
        Method to init url allowing to download data, checksums and stations info file

        Args:
            data_version : Version of the HadISD dataset
        """
        self.url_version = HADISD_URL + data_version

        # Check if HadISD URL is valid
        try:
            self.http.request("HEAD", self.url_version)
        except (LocationParseError, urllib3.exceptions.MaxRetryError):
            message = (
                f"Invalid URL {self.url_version}. Check HadISD URL or data version"
            )
            logging.error(message)
            raise ValueError(message)

        self.checksums_url = self.url_version + "/files/checksums.txt"
        metadata_file_name = "/files/hadisd_station_info_" + data_version + ".txt"
        self.metadata_url = self.url_version + metadata_file_name
        self.data_url = self.url_version + "/data/"

    def init_path(self, data_version, path):
        """
        Method to init path allowing to store data, checksums and stations info file

        Args:
            data_version : Version of the HadISD dataset
            path : Path to directory where files are downloaded and created
        """
        if path:
            self.checksums_path = os.path.join(path, "checksums.txt")
            self.metadata_path = os.path.join(
                path, "hadisd_station_info_" + data_version + ".txt"
            )
            if not os.path.exists(path):
                os.mkdir(path)
        else:
            message = "Invalid path"
            logging.error(message)
            raise ValueError(message)

    def get_hadisd_filenames(self):
        """
        Method to get file name for all files respecting a regex in the downloaded checksums file
        """
        # Get archive name from checksums file
        with open(self.checksums_path, "r") as f:
            content = f.read()
            filenames = re.findall(HADISD_DATA_REGEX, content)
            if filenames:
                return filenames
            else:
                message = "No files retrieved from archive list. Can't download HadISD archives"
                logging.error(message)
                raise ValueError(message)

    def download_archives(self, path, sample):
        """
        Method to download HadISD archives.

        Args:
            path : Path to directory where archives will be stored
            sample (bool): If True, download the first archive only for testing purposes
        """
        filenames = self.get_hadisd_filenames()
        print("Starting HadISD archives download...")
        for index, filename in enumerate(filenames):
            if not os.path.exists(os.path.join(path, filename)):
                filename_url = self.url_version + "/data/" + filename
                resp_data = self.http.request("GET", filename_url)

                # Get each archive
                if resp_data.status == 200:
                    with open(os.path.join(path, filename), "wb") as f:
                        f.write(resp_data.data)
                        logging.info(
                            f"File {filename} downloaded : {index + 1}/{len(filenames)} files"
                        )
                    if sample:
                        logging.info("Sample downloaded")
                        break
                else:
                    logging.info(f"Download failed. Code : {resp_data.status}")
            else:
                logging.info(f"File {filename} already downloaded.")

    def download_checksums(self):
        """
        Method to download HadISD checksums file
        """
        # Get checksums file which contains list of all station data files to download
        resp_checksums = self.http.request("GET", self.checksums_url)

        # Request to get checksums file
        if resp_checksums.status == 200:
            with open(self.checksums_path, "wb") as f:
                f.write(resp_checksums.data)
            logging.info("Checksums downloaded")
        else:
            message = f"Download failed. Code : {resp_checksums.status}"
            logging.error(message)
            raise HTTPError(message)

    def download_metadata(self):
        """
        Method to download stations metadata file
        """
        resp_metadata = self.http.request("GET", self.metadata_url)

        # Request to get stations metadata file
        if resp_metadata.status == 200:
            with open(self.metadata_path, "wb") as f:
                f.write(resp_metadata.data)
            logging.info("Metadata downloaded")
        else:
            message = f"Download failed. Code : {resp_metadata.status}"
            logging.error(message)
            raise HTTPError(message)

    @staticmethod
    def calculate_md5_file_checksum(file_path):
        """
        Method to calculate MD5 checksum of file

        Args:
            file_path : Path to file whose checksum must be calculated
        """
        md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
        return md5.hexdigest()

    def generate_md5_checksums_file(self, regex_pattern, path):
        """
        Method to generate a file containing the result of MD5 checksums calculation (file name + associated checksum)

        Args:
            regex_pattern : Regex pattern of files whose checksums must be calculated
            path : Path to directory containing files
        """
        with open(os.path.join(path, "checksums_generated.txt"), "w") as f:
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if re.match(regex_pattern, file):
                        checksum = self.calculate_md5_file_checksum(file_path)
                        f.write(f"{checksum} {file}\n")
        logging.info("Checksums generated")

    @staticmethod
    def compare_checksums(reference_checksums_file, checksums_file_to_check):
        """
        Method to compare two checksums files. Files must be formatted as following : file name + blank space + MD5
        checksum

        Arg:
            reference_checksums_file : Reference for checksums comparison
            checksums_file_to_check : Path to second checksums file to validate
        """
        md5_list = []

        with open(reference_checksums_file, "r") as reference_file:
            for line in reference_file:
                if not line.strip():
                    break
                # Split line in file in two parts : checksum and filename
                md5, filename = line.strip().split(" ", 1)
                md5_list.append((md5, filename))

        with open(checksums_file_to_check, "r") as to_compare_file:
            for line in to_compare_file:
                if not line.strip():
                    break
                md5, filename = line.strip().split(" ", 1)
                if (md5, filename) in md5_list:
                    logging.info(f"Checksum ok for {filename}")
                else:
                    logging.info(f"Checksum ko for {filename}")

    def generate_general_metadata_file(self, data_version, path, metadata_file=None):
        """
        Method to create and complete general metadata file

        Args:
            data_version : Version of the HadISD dataset
            path : Path to directory where general metadata file must be stored
            metadata_file : Text file completed by user to add specific metadata to general metadata file
        """

        # Initialisation of general metadata json and json schema from templates
        json_template = metadata.get_metadata_template("general_metadata")
        json_schema = metadata.get_metadata_schema("general_metadata")

        # Init and completion of data to update general metadata json
        data = {}
        data.update(
            {
                "data.protection-level": "NP",
                "data.source": "HadISD",
                "data.source-url": "https://www.metoffice.gov.uk/hadobs/hadisd/index.html",
                "data.download-date": datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "data.format-reference": "NetCDF",
                "data.data-license": "Non-Commercial Government Licence",
                "data.license-quote": "HadISD."
                                      + data_version
                                      + " data were obtained from "
                                        "http://www.metoffice.gov.uk/hadobs/hadisd on "
                                      + self.download_date
                                      + " and are British Crown Copyright, Met Office 2024, "
                                        "provided under an Open Government License, "
                                        "http://www.nationalarchives.gov.uk/doc/non"
                                        "-commercial--government-licence/non-commercial"
                                        "-government-licence.htm",
            }
        )

        if metadata_file:
            with open(metadata_file, "r") as f:
                for line in f:
                    # Split line in file in two parts : checksum and filename
                    key, value = line.strip().split(":", 1)
                    data.update({key: value})

        general_metadata_json = metadata.update_metadata_file(
            json_template, json_schema, data
        )

        # Save json object to json file
        with open(os.path.join(path, "general_metadata.json"), "w") as f:
            json.dump(general_metadata_json, f, indent=4)
