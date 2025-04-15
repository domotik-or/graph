#!/usr/bin/env python3

from setuptools import setup


setup(
    name="graph",
    version="0.1.0",
    description="Draw domotic graphs",
    author="Franck Barbenoire",
    author_email="fbarbenoire@gmail.com",
    url="https://github.com/domotik-or/graph",
    packages=["graph"],
    package_dir={"graph": "src"},
    include_package_data=True,
    install_requires=[
        "aiohttp", "python-dateutil", "matplotlib"
    ],
    entry_points={
        "console_scripts": ["graph=graph.main:run", ]
    },
    python_requires='>=3.11',
    zip_safe=False,
    license="MIT"
)

# http://python-packaging.readthedocs.io/en/latest/command-line-scripts.html
