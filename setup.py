import re
from setuptools import find_packages, setup
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements from file if it exists, otherwise use a default list
if os.path.exists('requirements.txt'):
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
else:
    requirements = [
        "matplotlib",
        "pandas",
        "numpy",
        "jinja2",
        "requests",
    ]

version = "0.10.6"

setup(
    name="Qtok",
    version=version,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={
        "qtok": ["data/*"],
    },
    python_requires=">=3.6",
    include_package_data=True,
    license="BSD",
    url="https://github.com/nup-csai/Qtok/",
    author="Aleksey Komissarov, Iaroslav Chelombitko, Egor Safronov",
    author_email="ad3002@gmail.com",
    description="Qtok: quality control tool for tokenization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    entry_points={
        'console_scripts': [
            'qtok = qtok.qtok:run_it',
        ],
    },
)
