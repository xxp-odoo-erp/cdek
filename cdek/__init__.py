"""
CDEK Python SDK v2

Python library for working with CDEK API version 2.

Usage example:
    from cdek import CdekClient

    # Create a test client
    client = CdekClient('TEST')

    # Create a production client
    client = CdekClient('PROD', account='your_account', secure='your_password')

    # Get list of cities
    cities = client.get_cities({'size': 10})

    # Calculate tariff
    from cdek.requests.tariff import Tariff
    tariff = Tariff()
    tariff.set_type(1)
    tariff.set_tariff_code(136)
    tariff.set_city_codes(44, 137)
    tariff.set_package_weight(1000)

    result = client.calculate_tariff(tariff)
"""

from . import constants
from .client import CdekClient
from .exceptions import CdekAuthException, CdekException, CdekRequestException

__version__ = "2.1.1.0.2"
__author__ = "CDEK Python SDK"
__license__ = "MIT"

__all__ = [
    "CdekClient",
    "CdekException",
    "CdekAuthException",
    "CdekRequestException",
    "constants",
]
