#!/usr/bin/env python
# -*- coding: utf8 -*-

import setuptools


setuptools.setup(
    name="zeeguu",
    version="0.1",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    author="Zeeguu Team",
    author_email="me@mir.lu",
    description="API for Zeeguu",
    keywords="second language acquisition api",
    dependency_links=[
        "git+https://github.com/mircealungu/python-wordstats.git#egg=wordstats"
    ],
    install_requires=("flask>=0.10.1",
                      "Flask-SQLAlchemy",
                      "readability",
                      "cssmin",
                      "jsmin",
                      "flask-wtf",
                      "goslate",
                      "Markupsafe",
                      "MySQL-python",
                      "regex",
                      "beautifulsoup4",
                      "feedparser",
                      "wordstats",
                      "requests",
                      "readability")
)
