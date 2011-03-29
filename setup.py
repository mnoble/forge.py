from setuptools import setup, find_packages
import sys, os

setup(
    name                 = 'forge',
    version              = '0.0.1',
    description          = "Simple object forger for unit testing.",
    long_description     = "Simple object forger for unit testing.",
    author               = 'Matte Noble',
    author_email         = 'me@mattenoble.com',
    url                  = 'http://mattenoble.com',
    packages             = find_packages(exclude=['ez_setup', 'examples', 'tests', '.build']),
    include_package_data = True,
    zip_safe             = False,
    setup_requires       = [
        "nose       >= 1.0.0",
        "unittest2  >= 0.5.1",
        "sqlalchemy >= 0.6.6",
    ]
)
