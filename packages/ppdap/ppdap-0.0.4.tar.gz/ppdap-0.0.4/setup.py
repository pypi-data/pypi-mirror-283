#!/usr/bin/env python3
from setuptools import setup

NAME = "ppdap"
DESCRIPTION = "Digo Accessory Protocol implementation in python"
URL = "https://gitlab.com/digo_public/ppdap"
AUTHOR = "DIGO"


PROJECT_URLS = {
    "Bug Reports": "{}/-/issues".format(URL),
    "Documentation": "{}/-/blob/main/README.md".format(URL),
    "Source": "{}/-/tree/master".format(URL),
}

with open("README.md", "r", encoding="utf-8") as f:
    README = f.read()


REQUIRES = [
    "requests>=2.25.0",
    "paho-mqtt>=1.6.0",
]


setup(
    name=NAME,
    version="0.0.4",
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type="text/markdown",
    author=AUTHOR,
#    url=URL,
    packages=["ppdap"],
    include_package_data=True,
#    project_urls=PROJECT_URLS,
    python_requires=">=3.11",
    install_requires=REQUIRES,
    license="Apache License 2.0",
    license_file="LICENSE",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.11",
        "Topic :: Home Automation",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
