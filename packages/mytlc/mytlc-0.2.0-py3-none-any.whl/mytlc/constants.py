# constants.py
# This file contains the constants used in the mytlc module. This includes file names,
# dictionary keys, and other constant values manipulated in various parts of the module.
import os

# Key for FAIR "Accessible" result in metadata
ACCESSIBLE_KEY = "accessible"

# Metadata catalog JSON file name
CATALOG_FILENAME = "catalog.json"

# Release notes file name
RELEASE_NOTES_FILENAME = "release_notes.md"

# Key for checksums reference in metadata
CHECKSUMS_REFERENCE_KEY = "checksums-reference"

# Coordinate keys suffix used in content metadata files
COORDINATE_KEYS_SUFFIX = "-coordinate"

# Key for coherence in metadata
COHERENCE_KEY = "coherence"

# Key for consistency in metadata
CONSISTENCY_KEY = "consistency"

# Content metadata suffix used in content metadata filenames
CONTENT_METADATA_SUFFIX = "_content_metadata.json"

# Coordinates axes used in content metadata files
COORDINATE_AXES = ["x", "y", "z"]

# Key for data license in metadata
DATA_LICENSE_KEY = "data-license"

# Key for data paper reference in metadata
DATAPAPER_REFERENCE_KEY = "datapaper-reference"

# Key for dimensions field used in content metadata files
DIMENSIONS_KEY = "dimensions"

# Key for download date in metadata
DOWNLOAD_DATE_KEY = "download-date"

# Key for end in metadata
END_KEY = "end"

# Key for FAIR results in metadata
FAIR_RESULTS_KEY = "fair-results"

# Key for FAIR "Findable" result in metadata
FINDABLE_KEY = "findable"

# Key for general field used in content metadata files
GENERAL_KEY = "general"

# Key for data file name field used in content metadata files
DATA_FILE_NAME_KEY = "data-file-name"

# Key for path field used in general metadata files
PATH_KEY = "path"

# Key for time reference field used in content metadata files
TIME_REFERENCE_KEY = "time-reference"

# Key for t-reference field used in content metadata (dimensions) files
T_REFERENCE_KEY = "t-reference"

# Key for forecast field used in content metadata files
FORECAST_KEY = "forecast"

# Key for probabilistic dimension field used in content metadata files
PROBABILISTIC_DIMENSION_KEY = "probabilistic-dimension"

# Key for meteo variable JSON object used in content metadata files
METEO_VARIABLE_KEY = "meteo-variable"

# Key for variable file-number in general metadata
FILE_NUMBER_KEY = "file-number"

# Key for variable format-reference in general metadata
FORMAT_REFERENCE_KEY = "format-reference"

# Key for FAIR "Interoperable" result in metadata
INTEROPERABLE_KEY = "interoperable"

# Key for last modification date in metadata
LAST_MODIFICATION_DATE_KEY = "last-modification-date"

# Key for license DOI in metadata
LICENSE_DOI_KEY = "license-doi"

# Key for license quote in metadata
LICENSE_QUOTE_KEY = "license-quote"

# General metadata
GENERAL_METADATA = "general_metadata"

# Content metadata
CONTENT_METADATA = "content_metadata"

# JSON schema file name for metadata validation
METADATA_SCHEMA_FILENAME = "general_metadata_schema.json"

# JSON template file name for general metadata file generation
METADATA_TEMPLATE_FILENAME = "general_metadata_template.json"

# JSON schema file name for content metadata validation
CONTENT_METADATA_SCHEMA_FILENAME = "content_metadata_schema.json"

# JSON template file name for content metadata file generation
CONTENT_METADATA_TEMPLATE_FILENAME = "content_metadata_template.json"

# String to write for an unsuccessful check on metadata
METADATA_CHECK_KO = "KO"

# String to write for a successful check on metadata
METADATA_CHECK_OK = "OK"

# Key for metadata field
METADATA_KEY = "metadata"

# Key for metadata values in metadata
METADATA_VALUES_KEY = "metadata-values"

# Key for minimal value in metadata
MIN_VALUE_KEY = "min-value"

# Key for maximal value in metadata
MAX_VALUE_KEY = "max-value"

# Name of the NetCDF MIME type
NETCDF_MIME_TYPE = "application/x-netcdf"

# Key for other results in metadata
OTHER_RESULTS_KEY = "other-results"

# Key for size in metadata
SIZE_KEY = "size-go"

# Key for spatial reference in metadata
SPATIAL_REFERENCE_KEY = "spatial-reference"

# Key for missing value indicator in metadata
MISSING_VALUE_INDICATOR_KEY = "missing-value-indicator"

# Key for missing value indicator definition key in metadata
MISSING_VALUE_INDICATOR_DEFINED_KEY = "missing-value-indicator-defined"

# Key for protection level key in metadata
PROTECTION_LEVEL_KEY = "protection-level"

# Key for plausibility in metadata
PLAUSIBILITY_KEY = "plausibility"

# Key for start in metadata
START_KEY = "start"

# Key for total missing value in metadata
TOTAL_MISSING_VALUE_KEY = "total-missing-value"

# Key for time range in metadata
TIME_RANGE_KEY = "time-range"

# Key for unit value in metadata
UNIT_KEY = "unit"

# Key for UUID value in metadata
UUID_VALUE_KEY = "uuid-value"

# Key for standard name in metadata
STANDARD_NAME_KEY = "standard-name"

# NetCDF format written in general metadata format reference field
NETCDF_FORMAT = "NetCDF"

# NetCDF file suffix
NETCDF_FILE_SUFFIX = ".nc"

# General metadata file name for a dataset
GENERAL_METADATA_FILENAME = "general_metadata.json"

# Key for release notes reference in metadata
RELEASENOTES_REFERENCE_KEY = "releasenotes-reference"

# Key for restrictions in metadata
RESTRICTIONS_KEY = "restrictions"

# Key for FAIR "Reusable" value in metadata
REUSABLE_KEY = "reusable"

# Key for RGPD in metadata
RGPD_KEY = "rgpd"

# Name of folder containing schematics and other configuration files
SCHEMAS_DIR = "templates"

# Key for source url in metadata
SOURCE_URL_KEY = "source-url"

# Primary key for JSON dataset object in metadata
DATASET_KEY = "dataset"

# Primary key for JSON data object in metadata
DATA_KEY = "data"

# Key for verification results field in metadata
VERIFICATION_RESULTS_KEY = "verification-results"

# Primary key for source field in metadata
SOURCE_KEY = "source"

# Unique key to identify each dataset in the metadata
UUID_KEY = "uuid"

# Key for the name of a dataset
NAME_KEY = "name"

# Name of the log file generated by the module
LOG_FILENAME = "mytlc_logs.log"

# Path to the module
MODULE_ROOT_PATH = os.path.dirname(__file__)

# Value for geographic coordinates with WGS84 system
WGS84_SYSTEM = "Geographic degrees (WGS84)"

# Long name attribute
LONG_NAME_ATTRIBUTE = "long_name"

# Standard name attribute
STANDARD_NAME_ATTRIBUTE = "standard_name"

# Unit attribute
UNIT_ATTRIBUTE = "units"

# Grib missing value attribute
GRIB_MISSING_VALUE_ATTRIBUTE = "GRIB_missingValue"

# Flagged value attribute
FLAGGED_VALUE_ATTRIBUTE = "flagged_value"

# Valid min attribute
VALID_MIN_ATTRIBUTE = "valid_min"

# Valid max attribute
VALID_MAX_ATTRIBUTE = "valid_max"

# Date format
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# HadISD variables list
HADISD_VARIABLES_LIST = [
    "temperatures",
    "dewpoints",
    "slp",
    "stnlp",
    "windspeeds",
    "winddirs",
    "total_cloud_cover",
    "low_cloud_cover",
    "mid_cloud_cover",
    "high_cloud_cover",
    "precip1_depth",
    "precip2_depth",
    "precip3_depth",
    "precip6_depth",
    "precip9_depth",
    "precip12_depth",
    "precip15_depth",
    "precip18_depth",
    "precip24_depth",
    "cloud_base",
    "wind_gust",
    "past_sigwx1",
]

# HadISD key
HADISD_KEY = "hadisd"

# ERA5 datasets allowed
ERA5_DATASETS = ["reanalysis-era5-pressure-levels", "reanalysis-era5-single-levels"]

# ERA5 data file format
ERA5_FORMAT = ["netcdf", "grib"]

# Key for x coordinate
X_COORDINATE_KEY = "x-coordinate"

# Key for y coordinate
Y_COORDINATE_KEY = "y-coordinate"

# Key for z coordinate
Z_COORDINATE_KEY = "z-coordinate"

# Allowed parameters to request ERA5 API with hourly pressure levels dataset
ERA5_PRESSURE_LEVELS_LIST = [
    "dataset",
    "variable",
    "pressure_level",
    "start_date",
    "end_date",
    "coordinate",
    "format",
]

# Allowed parameters to request ERA5 API with hourly single level dataset
ERA5_SINGLE_LEVEL_LIST = [
    "dataset",
    "variable",
    "start_date",
    "end_date",
    "coordinate",
    "format",
]

# Allowed variables for hourly pressure levels dataset
PRESSURE_LEVELS_VARIABLES = [
    "divergence",
    "fraction_of_cloud_cover",
    "geopotential",
    "ozone_mass_mixing_ratio",
    "potential_vorticity",
    "relative_humidity",
    "specific_cloud_ice_water_content",
    "specific_cloud_liquid_water_content",
    "specific_humidity",
    "specific_rain_water_content",
    "specific_snow_water_content",
    "temperature",
    "u_component_of_wind",
    "v_component_of_wind",
    "vertical_velocity",
    "vorticity",
]

# Allowed pressure levels
PRESSURE_LEVELS = [
    "1",
    "2",
    "3",
    "5",
    "7",
    "10",
    "20",
    "30",
    "50",
    "70",
    "100",
    "125",
    "150",
    "175",
    "200",
    "225",
    "250",
    "300",
    "350",
    "400",
    "450",
    "500",
    "550",
    "600",
    "650",
    "700",
    "750",
    "775",
    "800",
    "825",
    "850",
    "875",
    "900",
    "925",
    "950",
    "975",
    "1000",
]

# Allowed variables for hourly single level dataset
SINGLE_LEVELS_VARIABLES = [
    "100m_u_component_of_wind",
    "100m_v_component_of_wind",
    "10m_u_component_of_neutral_wind",
    "10m_u_component_of_wind",
    "10m_v_component_of_neutral_wind",
    "10m_v_component_of_wind",
    "10m_wind_gust_since_previous_post_processing",
    "2m_dewpoint_temperature",
    "2m_temperature",
    "air_density_over_the_oceans",
    "angle_of_sub_gridscale_orography",
    "anisotropy_of_sub_gridscale_orography",
    "benjamin_feir_index",
    "boundary_layer_dissipation",
    "boundary_layer_height",
    "charnock",
    "clear_sky_direct_solar_radiation_at_surface",
    "cloud_base_height",
    "coefficient_of_drag_with_waves",
    "convective_available_potential_energy",
    "convective_inhibition",
    "convective_precipitation",
    "convective_rain_rate",
    "convective_snowfall",
    "convective_snowfall_rate_water_equivalent",
    "downward_uv_radiation_at_the_surface",
    "duct_base_height",
    "eastward_gravity_wave_surface_stress",
    "eastward_turbulent_surface_stress",
    "evaporation",
    "forecast_albedo",
    "forecast_logarithm_of_surface_roughness_for_heat",
    "forecast_surface_roughness",
    "free_convective_velocity_over_the_oceans",
    "friction_velocity",
    "geopotential",
    "gravity_wave_dissipation",
    "high_cloud_cover",
    "high_vegetation_cover",
    "ice_temperature_layer_1",
    "ice_temperature_layer_2",
    "ice_temperature_layer_3",
    "ice_temperature_layer_4",
    "instantaneous_10m_wind_gust",
    "instantaneous_eastward_turbulent_surface_stress",
    "instantaneous_large_scale_surface_precipitation_fraction",
    "instantaneous_moisture_flux",
    "instantaneous_northward_turbulent_surface_stress",
    "instantaneous_surface_sensible_heat_flux",
    "k_index",
    "lake_bottom_temperature",
    "lake_cover",
    "lake_depth",
    "lake_ice_depth",
    "lake_ice_temperature",
    "lake_mix_layer_depth",
    "lake_mix_layer_temperature",
    "lake_shape_factor",
    "lake_total_layer_temperature",
    "land_sea_mask",
    "large_scale_precipitation",
    "large_scale_precipitation_fraction",
    "large_scale_rain_rate",
    "large_scale_snowfall",
    "large_scale_snowfall_rate_water_equivalent",
    "leaf_area_index_high_vegetation",
    "leaf_area_index_low_vegetation",
    "low_cloud_cover",
    "low_vegetation_cover",
    "maximum_2m_temperature_since_previous_post_processing",
    "maximum_individual_wave_height",
    "maximum_total_precipitation_rate_since_previous_post_processing",
    "mean_boundary_layer_dissipation",
    "mean_convective_precipitation_rate",
    "mean_convective_snowfall_rate",
    "mean_direction_of_total_swell",
    "mean_direction_of_wind_waves",
    "mean_eastward_gravity_wave_surface_stress",
    "mean_eastward_turbulent_surface_stress",
    "mean_evaporation_rate",
    "mean_gravity_wave_dissipation",
    "mean_large_scale_precipitation_fraction",
    "mean_large_scale_precipitation_rate",
    "mean_large_scale_snowfall_rate",
    "mean_northward_gravity_wave_surface_stress",
    "mean_northward_turbulent_surface_stress",
    "mean_period_of_total_swell",
    "mean_period_of_wind_waves",
    "mean_potential_evaporation_rate",
    "mean_runoff_rate",
    "mean_sea_level_pressure",
    "mean_snow_evaporation_rate",
    "mean_snowfall_rate",
    "mean_snowmelt_rate",
    "mean_square_slope_of_waves",
    "mean_sub_surface_runoff_rate",
    "mean_surface_direct_short_wave_radiation_flux",
    "mean_surface_direct_short_wave_radiation_flux_clear_sky",
    "mean_surface_downward_long_wave_radiation_flux",
    "mean_surface_downward_long_wave_radiation_flux_clear_sky",
    "mean_surface_downward_short_wave_radiation_flux",
    "mean_surface_downward_short_wave_radiation_flux_clear_sky",
    "mean_surface_downward_uv_radiation_flux",
    "mean_surface_latent_heat_flux",
    "mean_surface_net_long_wave_radiation_flux",
    "mean_surface_net_long_wave_radiation_flux_clear_sky",
    "mean_surface_net_short_wave_radiation_flux",
    "mean_surface_net_short_wave_radiation_flux_clear_sky",
    "mean_surface_runoff_rate",
    "mean_surface_sensible_heat_flux",
    "mean_top_downward_short_wave_radiation_flux",
    "mean_top_net_long_wave_radiation_flux",
    "mean_top_net_long_wave_radiation_flux_clear_sky",
    "mean_top_net_short_wave_radiation_flux",
    "mean_top_net_short_wave_radiation_flux_clear_sky",
    "mean_total_precipitation_rate",
    "mean_vertical_gradient_of_refractivity_inside_trapping_layer",
    "mean_vertically_integrated_moisture_divergence",
    "mean_wave_direction",
    "mean_wave_direction_of_first_swell_partition",
    "mean_wave_direction_of_second_swell_partition",
    "mean_wave_direction_of_third_swell_partition",
    "mean_wave_period",
    "mean_wave_period_based_on_first_moment",
    "mean_wave_period_based_on_first_moment_for_swell",
    "mean_wave_period_based_on_first_moment_for_wind_waves",
    "mean_wave_period_based_on_second_moment_for_swell",
    "mean_wave_period_based_on_second_moment_for_wind_waves",
    "mean_wave_period_of_first_swell_partition",
    "mean_wave_period_of_second_swell_partition",
    "mean_wave_period_of_third_swell_partition",
    "mean_zero_crossing_wave_period",
    "medium_cloud_cover",
    "minimum_2m_temperature_since_previous_post_processing",
    "minimum_total_precipitation_rate_since_previous_post_processing",
    "minimum_vertical_gradient_of_refractivity_inside_trapping_layer",
    "model_bathymetry",
    "near_ir_albedo_for_diffuse_radiation",
    "near_ir_albedo_for_direct_radiation",
    "normalized_energy_flux_into_ocean",
    "normalized_energy_flux_into_waves",
    "normalized_stress_into_ocean",
    "northward_gravity_wave_surface_stress",
    "northward_turbulent_surface_stress",
    "ocean_surface_stress_equivalent_10m_neutral_wind_direction",
    "ocean_surface_stress_equivalent_10m_neutral_wind_speed",
    "peak_wave_period",
    "period_corresponding_to_maximum_individual_wave_height",
    "potential_evaporation",
    "precipitation_type",
    "runoff",
    "sea_ice_cover",
    "sea_surface_temperature",
    "significant_height_of_combined_wind_waves_and_swell",
    "significant_height_of_total_swell",
    "significant_height_of_wind_waves",
    "significant_wave_height_of_first_swell_partition",
    "significant_wave_height_of_second_swell_partition",
    "significant_wave_height_of_third_swell_partition",
    "skin_reservoir_content",
    "skin_temperature",
    "slope_of_sub_gridscale_orography",
    "snow_albedo",
    "snow_density",
    "snow_depth",
    "snow_evaporation",
    "snowfall",
    "snowmelt",
    "soil_temperature_level_1",
    "soil_temperature_level_2",
    "soil_temperature_level_3",
    "soil_temperature_level_4",
    "soil_type",
    "standard_deviation_of_filtered_subgrid_orography",
    "standard_deviation_of_orography",
    "sub_surface_runoff",
    "surface_latent_heat_flux",
    "surface_net_solar_radiation",
    "surface_net_solar_radiation_clear_sky",
    "surface_net_thermal_radiation",
    "surface_net_thermal_radiation_clear_sky",
    "surface_pressure",
    "surface_runoff",
    "surface_sensible_heat_flux",
    "surface_solar_radiation_downward_clear_sky",
    "surface_solar_radiation_downwards",
    "surface_thermal_radiation_downward_clear_sky",
    "surface_thermal_radiation_downwards",
    "temperature_of_snow_layer",
    "toa_incident_solar_radiation",
    "top_net_solar_radiation",
    "top_net_solar_radiation_clear_sky",
    "top_net_thermal_radiation",
    "top_net_thermal_radiation_clear_sky",
    "total_cloud_cover",
    "total_column_cloud_ice_water",
    "total_column_cloud_liquid_water",
    "total_column_ozone",
    "total_column_rain_water",
    "total_column_snow_water",
    "total_column_supercooled_liquid_water",
    "total_column_water",
    "total_column_water_vapour",
    "total_precipitation",
    "total_sky_direct_solar_radiation_at_surface",
    "total_totals_index",
    "trapping_layer_base_height",
    "trapping_layer_top_height",
    "type_of_high_vegetation",
    "type_of_low_vegetation",
    "u_component_stokes_drift",
    "uv_visible_albedo_for_diffuse_radiation",
    "uv_visible_albedo_for_direct_radiation",
    "v_component_stokes_drift",
    "vertical_integral_of_divergence_of_cloud_frozen_water_flux",
    "vertical_integral_of_divergence_of_cloud_liquid_water_flux",
    "vertical_integral_of_divergence_of_geopotential_flux",
    "vertical_integral_of_divergence_of_kinetic_energy_flux",
    "vertical_integral_of_divergence_of_mass_flux",
    "vertical_integral_of_divergence_of_moisture_flux",
    "vertical_integral_of_divergence_of_ozone_flux",
    "vertical_integral_of_divergence_of_thermal_energy_flux",
    "vertical_integral_of_divergence_of_total_energy_flux",
    "vertical_integral_of_eastward_cloud_frozen_water_flux",
    "vertical_integral_of_eastward_cloud_liquid_water_flux",
    "vertical_integral_of_eastward_geopotential_flux",
    "vertical_integral_of_eastward_heat_flux",
    "vertical_integral_of_eastward_kinetic_energy_flux",
    "vertical_integral_of_eastward_mass_flux",
    "vertical_integral_of_eastward_ozone_flux",
    "vertical_integral_of_eastward_total_energy_flux",
    "vertical_integral_of_eastward_water_vapour_flux",
    "vertical_integral_of_energy_conversion",
    "vertical_integral_of_kinetic_energy",
    "vertical_integral_of_mass_of_atmosphere",
    "vertical_integral_of_mass_tendency",
    "vertical_integral_of_northward_cloud_frozen_water_flux",
    "vertical_integral_of_northward_cloud_liquid_water_flux",
    "vertical_integral_of_northward_geopotential_flux",
    "vertical_integral_of_northward_heat_flux",
    "vertical_integral_of_northward_kinetic_energy_flux",
    "vertical_integral_of_northward_mass_flux",
    "vertical_integral_of_northward_ozone_flux",
    "vertical_integral_of_northward_total_energy_flux",
    "vertical_integral_of_northward_water_vapour_flux",
    "vertical_integral_of_potential_and_internal_energy",
    "vertical_integral_of_potential_internal_and_latent_energy",
    "vertical_integral_of_temperature",
    "vertical_integral_of_thermal_energy",
    "vertical_integral_of_total_energy",
    "vertically_integrated_moisture_divergence",
    "volumetric_soil_water_layer_1",
    "volumetric_soil_water_layer_2",
    "volumetric_soil_water_layer_3",
    "volumetric_soil_water_layer_4",
    "wave_spectral_directional_width",
    "wave_spectral_directional_width_for_swell",
    "wave_spectral_directional_width_for_wind_waves",
    "wave_spectral_kurtosis",
    "wave_spectral_peakedness",
    "wave_spectral_skewness",
    "zero_degree_level",
]

# User editable keys in general metadata file
EDITABLE_GENERAL_METADATA_KEYS = [
    "data.protection-level",
    "datapaper-reference",
    "rgpd",
    "restrictions",
]

# HadISD archive extension
HADISD_ARCHIVE_EXTENSION = ".tar.gz"

# HadISD station info file
HADISD_STATION_INFO_FILE = "hadisd_station_info"

# HadISD checksums file
HADISD_CHECKSUMS_FILE = "checksums.txt"

# General metadata JSON file
GENERAL_METADATA_FILE_NAME = "general_metadata.json"

# Meteo France AROME model
AROME_MODEL = "arome"

# Meteo France ARPEGE model
ARPEGE_MODEL = "arpege"
