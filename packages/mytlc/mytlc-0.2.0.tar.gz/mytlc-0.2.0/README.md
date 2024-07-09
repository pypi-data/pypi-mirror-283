# MYTLC
## Package Description
The MYTLC python package is a prototype for downloading meteorological data from multiple sources and building dataset that respect FAIR principles ([FAIR Reference][]).
The package depends on the MCAPY package (which is not distributed) to read the content of meteorological files.
## Features
### Download meteorological data
The following meteorological data can be downloaded with MYTLC :
* ERA5 reanalysis (.nc or .grib) :
    * ERA5 hourly data on single levels from 1940 to present ;
    * ERA5 hourly data on pressure levels from 1940 to present.
* HadISD station observations (complete dataset)
### Build dataset
From the downloaded data, MYTLC can build dataset containing :
* All downloaded meteorological data files ;
* A general metadata file ;
* A checksums file (MD5 hash for each meteorological data file) ;
* A content metadata file for each meteorological data file ;
* A release notes file ;
* Additionnal source-dependent files.

MYTLC cannot download data from AROME and ARPEGE models (Météo France) but it can build a dataset if the initial data directory is created manually.
The data directory must contain the following elements :
* Meteorological data (.grib or .grib2) ;
* A general metadata file completed manually ;
* A checksums file (MD5 hash for each meteorological data file).
### Search dataset
MYTLC allows users to search for files of interest filtered according to following the dimensions :
* Data source ;
* Coordinates (x,y,z) ;
* Time ;
* Weather forecast time ;
* Probabilistic dimension ;
* Meteorological parameters.

## License

MYTLC is distributed under the 3-Clause BSD License. See LICENSE.txt file.


 [FAIR Reference]: https://doi.org/10.1038/sdata.2016.18