import pytest
from pyicu_slugify import pyicu_slugify

def test_basic_slugify():
    assert pyicu_slugify("Hello World!") == "hello-world"

def test_german_slugify():
    assert pyicu_slugify("Über den Wölken", "de") == "ueber-den-woelken"

# Add more tests as needed