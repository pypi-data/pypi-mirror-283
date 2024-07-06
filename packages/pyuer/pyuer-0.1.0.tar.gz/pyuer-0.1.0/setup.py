from setuptools import setup, find_packages

setup(
    name="pyuer",
    version="0.1.0",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "requests",
        "bs4",
        "selenium"
    ],
)

