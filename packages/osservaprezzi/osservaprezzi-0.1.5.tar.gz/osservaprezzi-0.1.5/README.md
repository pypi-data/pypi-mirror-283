# Client Library for Osservaprezzi

[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=lnx85_osservaprezzi-py&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=lnx85_osservaprezzi-py) [![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=lnx85_osservaprezzi-py&metric=security_rating)](https://sonarcloud.io/dashboard?id=lnx85_osservaprezzi-py) [![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=lnx85_osservaprezzi-py&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=lnx85_osservaprezzi-py) [![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=lnx85_osservaprezzi-py&metric=ncloc)](https://sonarcloud.io/dashboard?id=lnx85_osservaprezzi-py) [![Coverage](https://sonarcloud.io/api/project_badges/measure?project=lnx85_osservaprezzi-py&metric=coverage)](https://sonarcloud.io/dashboard?id=lnx85_osservaprezzi-py)

Please report any [issues](https://github.com/lnx85/osservaprezzi.py/issues) and feel free to raise [pull requests](https://github.com/lnx85/osservaprezzi.py/pulls).

[![BuyMeCoffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/lnx85)

## Installation

If you have a recent version of Python 3, you should be able to
do `pip install osservaprezzi` to get the most recently released version of
this.

## Usage

You are welcome to try using this as a python library for other efforts.
A simple usage might go something like this:

```python
import aiohttp
import asyncio
import logging

from osservaprezzi.client import Osservaprezzi
from osservaprezzi.models import GPSCoordinates


async def main():
  async with aiohttp.ClientSession() as session:
    logging.basicConfig(level=logging.DEBUG)
    client = Osservaprezzi(session)

    # brands list
    brands = await client.get_brands()
    for brand in brands:
        print(brand.name)

    # fuels list
    fuels = await client.get_fuels()
    for fuel in fuels:
        print(fuel)

    # stations list 5 km near 45.541553,10.211802
    location = GPSCoordinates(latitude=45.541553, longitude=10.211802)
    stations = await client.get_stations(location, radius=5)
    for station in stations:
       print(station.name)

    # station details
    station = await client.get_station(47997)
    print(station.name)


if __name__ == '__main__':
    asyncio.run(main())
```

## Thanks

My heartfelt thanks to:

- All the users who have given useful feedback and contributed code!
