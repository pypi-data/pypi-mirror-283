#!/usr/bin/env python

from setuptools import find_packages, setup

version = "1.0.0"

# with open("README.md") as f:
#     readme = f.read()

# with open("requirements.txt") as f:
#     required = f.read().splitlines()

setup(
    name="messi_add_method",
    version=version,
    description="Helper tools for adding new method into the MESSI pipeline.",
    keywords=[
        "nextflow",
        "bioinformatics",
        "workflow",
        "pipeline"
    ],
    author="Tony Liang",
    author_email="chunqingliang@gmail.com",
    license="MIT",
    python_requires=">=3.8, <4",
    packages=find_packages(exclude=("docs")),
    include_package_data=True,
    zip_safe=False,
)