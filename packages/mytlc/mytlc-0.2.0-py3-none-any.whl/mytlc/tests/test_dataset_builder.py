import importlib.resources as pkg_resources
import os

from ..build_dataset.dataset_builder import DatasetBuilder


def get_root_data_dir():
    root_data = pkg_resources.files("mytlc.tests.data") / "test_dataset_builder_data"
    return str(root_data)


def get_era5_file_list():
    file_list = [
        "2023_01_2m_temperature.nc",
        "2023_01_2m_temperature_content_metadata.json",
        "checksums_generated.txt",
        "general_metadata.json",
        "release_notes.md",
    ]
    return file_list


def get_hadisd_file_list():
    file_list = [
        "checksums.txt",
        "checksums_generated.txt",
        "general_metadata.json",
        "hadisd.3.4.1.202405p_19310101-20240601_010010-99999.nc",
        "hadisd.3.4.1.202405p_19310101-20240601_010010-99999_content_metadata.json",
        "hadisd_station_info_v341_202405p.txt",
        "release_notes.md",
    ]
    return file_list


def test_build_dataset_era5(tmpdir):
    # Get data in mytlc package
    root_data = get_root_data_dir()
    data_path = os.path.join(root_data, "ERA5_data")
    # Create temp dir to build dataset
    output_dir = tmpdir.mkdir("output")
    # Build test dataset
    dataset_name = "ERA5_test"
    builder = DatasetBuilder()
    builder.build_dataset(data_path, dataset_name, final_path=output_dir)
    # Assert presence of files
    output_sub_dir = output_dir.join("ERA5_test_01.00.00")
    output_files = [f.basename for f in output_sub_dir.listdir()]
    era5_file_list = get_era5_file_list()
    assert output_files == era5_file_list


def test_build_dataset_hadisd(tmpdir):
    # Get data in mytlc package
    root_data = get_root_data_dir()
    data_path = os.path.join(root_data, "HadISD_data")
    # Create temp dir to build dataset
    output_dir = tmpdir.mkdir("output")
    # Build test dataset
    dataset_name = "HadISD_test"
    builder = DatasetBuilder()
    builder.build_dataset(data_path, dataset_name, final_path=output_dir)
    # Assert presence of files
    output_sub_dir = output_dir.join("HadISD_test_01.00.00")
    output_files = [f.basename for f in output_sub_dir.listdir()]
    hadisd_file_list = get_hadisd_file_list()
    assert output_files == hadisd_file_list
