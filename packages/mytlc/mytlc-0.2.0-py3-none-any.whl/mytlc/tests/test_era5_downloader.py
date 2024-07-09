import socket

import pytest

from ..download.era5_downloader import Era5Downloader


def internet_available():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False


def get_era5_file_list():
    file_list = [
        "2023_01_2m_temperature.nc",
        "checksums_generated.txt",
        "general_metadata.json",
    ]
    return file_list


@pytest.mark.timeout(600)
@pytest.mark.skipif(
    not internet_available(), reason="Internet connection not available"
)
def test_era5_downloader(tmpdir):
    # test ping google

    output_dir = tmpdir.mkdir("output")
    sub_output_dir = output_dir.mkdir("ERA5_data")

    # Download test data
    parameters = {
        "dataset": "reanalysis-era5-single-levels",
        "variable": ["2m_temperature"],
        "start_date": "202301",
        "end_date": "202301",
        "coordinate": [-10, 11, 37, 38],
        "format": "netcdf",
    }

    era5_dl = Era5Downloader()
    era5_dl.download_era5_data(parameters, sub_output_dir)

    # Assert files
    output_files = [f.basename for f in sub_output_dir.listdir()]
    era5_file_list = get_era5_file_list()
    assert output_files == era5_file_list
