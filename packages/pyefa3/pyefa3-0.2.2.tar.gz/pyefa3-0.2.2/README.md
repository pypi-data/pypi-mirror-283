# pyefa3

Python-Library for accessing online train connection APIs (Elektronische Fahrplanauskunft).

A list of supported regions can be found [here](https://github.com/NoMoKeTo/pyefa/wiki/Supported-Regions).

## Installation

Just install it from the [Python Package Index](https://pypi.python.org/pypi/pyefa3):

```sh
pip install pyefa3
```

## Usage

```python
from pyefa.classes import Station
from pyefa.networks import DING

origin_station = Station()
origin_station.name = "Theater"
origin_station.place = "Ulm"

destination_station = Station()
destination_station.name = "Universität Süd"
destination_station.place = "Ulm"

efa_api = DING()
result = efa_api.tripRequest(origin_station, destination_station, apitype="xml")
print(result)

machine_readable = result.asdict()
```

### Install from source

The Python-Modules **beautifulsoup4** and **colorama** are required.

Just clone the repository and run:

```sh
python setup.py install
```

## Documentation

Documentation is available via docstrings.

```sh
pydoc clifa
pydoc clifa.classes
# and so on
```
