# Propertia SDK

![PyPI version](https://badge.fury.io/py/propertia.svg) [![Python support](https://img.shields.io/badge/python-3.8+-blue.svg)](https://img.shields.io/badge/python-3.8+-blue)  [![Unit Tests](https://github.com/SearchSmartly/propertia-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/SearchSmartly/propertia-sdk/actions/workflows/ci.yml)

The Propertia SDK helps users integrate easily with the SmartScore services

## Installation

Install Propertia SDK using `pip`

```
pip install propertia
```

### SDK set up

In order to authenticate with Propertia, you will have to supply the API Key.

```python
from propertia.client import PropertiaClient

with PropertiaClient(api_key="your_api_key") as client:
    ...
```

## Client Usage

### Get Scores

Given coordinates and needs, return the scores

#### Takes:

* properties
* needs

#### Returns:

* List of properties sorted by descending scores

#### Example:

```python
from propertia.client import PropertiaClient

properties = [
    {
        "id": "Property A",
        "latitude": "43.70558",
        "longitude": "-79.530985"
    },
    {
        "id": "Property B",
        "latitude": "43.640971",
        "longitude": "-79.579119"
    },
    {
        "id": "Property C",
        "latitude": "43.704711",
        "longitude": "-79.287965"
    }
]

needs = {
    "food-and-drink": {
        "importance": 5,
        "categories": [
            "fast-food"
        ]
    }
}

with PropertiaClient(api_key="your_api_key") as client:
    scores = client.get_scores(properties, needs, region)
    # Do something with your scores
```

### Get Isochrones

Given a list of one or two destinations and a boolean, return the isochrones (polygon)

#### Takes:

* destinations
* aggregated

#### Returns:

* A polygon in GeoJSON format

#### Example:

```python
from propertia.client import PropertiaClient

destinations = [
    {
        "id": "destination",
        "latitude": 25.197197,
        "longitude": 55.27437639999999,
        "time": 10,
        "methods": [
            "walking"
        ]
    }
]

aggregated = True

with PropertiaClient(api_key="your_api_key") as client:
    polygon = client.get_isochrones(destinations, aggregated)
    # Do something with your isochrones
```

### Get Commute Times

Given a list of one or two destinations and a list of properties, returns the time it takes to commute to each property

#### Takes:

* destinations
* properties

#### Returns:

* A dictionary of properties with the time it takes to commute to each property

#### Example:

```python
from propertia.client import PropertiaClient

destinations = [
    {
        "id": "destination",
        "latitude": 25.197197,
        "longitude": 55.27437639999999,
        "time": 10,
        "methods": [
            "walking"
        ]
    }
]

properties = [
    {
        "id": "Property A",
        "latitude": "43.70558",
        "longitude": "-79.530985"
    },
    {
        "id": "Property B",
        "latitude": "43.640971",
        "longitude": "-79.579119"
    },
    {
        "id": "Property C",
        "latitude": "43.704711",
        "longitude": "-79.287965"
    }
]

with PropertiaClient(api_key="your_api_key") as client:
    results = client.get_commute_time(destinations, properties)
    # Do something with your results
```

## Use category tree

```
from propertia.categories import CATEGORY_TREE
```

## Get user categories

```
from propertia.client import PropertiaClient

with PropertiaClient(api_key="your_api_key") as client:
    categories = client.get_user_categories()
    # Do something with your results
```