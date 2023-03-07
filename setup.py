#!/usr/bin/env python
# encoding: UTF-8

import os

from setuptools import setup


long_description = ""
if os.path.isfile("README.rst"):
    long_description = open("README.rst", "r", encoding="UTF-8").read()


setup(
    name="pelican-gemini-capsule",
    version="0.3.0",
    description="Pelican plugin to generate Gemini capsules",
    url="https://github.com/flozz/pelican-gemini-capsule",
    project_urls={
        "Source Code": "https://github.com/flozz/pelican-gemini-capsule",
        "Issues": "https://github.com/flozz/pelican-gemini-capsule/issues",
        "Chat": "https://discord.gg/P77sWhuSs4",
        "Donate": "https://github.com/flozz/pelican-gemini-capsule#support-this-project",
    },
    license="GPLv3",
    long_description=long_description,
    keywords="pelican gemini capsule gemtext gmi",
    author="Fabien LOISON",
    py_modules=["pelican_gemini_capsule"],
    install_requires=[
        "rst2gemtext",
    ],
    extras_require={
        "dev": [
            "nox",
            "flake8",
            "black",
        ]
    },
)
