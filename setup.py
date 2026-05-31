"""Setup script for camKapture."""
from setuptools import setup, find_packages
import os

# Read long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="camKapture",
    version="2.0.0",
    author="camKapture Contributors",
    description="Professional webcam application with effects and capture features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manojuppala/camKapture",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics :: Capture :: Digital Camera",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "opencv-python>=4.5.0",
        "numpy>=1.19.0",
        "PySide6>=6.0.0",
    ],
    entry_points={
        "console_scripts": [
            "camkapture=main:main",
        ],
    },
    include_package_data=True,
)
