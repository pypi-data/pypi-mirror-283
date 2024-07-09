import importlib.resources as pkg_resources
import json
import os

from ..search import search


def get_root_data_dir():
    root_data = pkg_resources.files("mytlc.tests.data") / "test_search_data"
    return str(root_data)


def test_search():
    # Get data in mytlc package
    root_data = get_root_data_dir()
    catalog_path = os.path.join(root_data, "catalog.json")
    # Edit catalog dataset path
    with open(catalog_path, "r") as file:
        data = json.load(file)

    data[0]["dataset"]["path"] = os.path.join(root_data, "ERA5_test_01.00.00")

    with open(catalog_path, "w") as file:
        json.dump(data, file, indent=4)

    # Search test
    source = "era5"

    filters_positive = {
        "x-coordinate": [-10, 10],
        "y-coordinate": [37.5, 54.75],
        "z-coordinate": [0],
        "t-reference": ["20230101:0000", "20230131:230000"],
        "probabilistic-dimension": [0],
        "meteo-variable": ["2 metre temperature"],
    }

    positive_results = search.search_datasets(catalog_path, source, filters_positive)
    assert positive_results == {
        "ERA5_test_01.00.00": [
            (
                "2023_01_2m_temperature.nc",
                " - Total overlap on x axis - Total overlap on y axis - Total overlap on z axis -  - Partial time overlap",
            )
        ]
    }

    filters_negative = {
        "x-coordinate": [75],
        "y-coordinate": [75],
        "z-coordinate": [10],
        "t-reference": ["20230101:0000", "20230131:230000"],
        "probabilistic-dimension": [0],
    }

    negative_results = search.search_datasets(catalog_path, source, filters_negative)
    assert negative_results == {}
