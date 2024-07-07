from setuptools import setup, find_packages
from pkg_resources import parse_requirements


def read_requirements():
    with open("requirements.txt", "r") as f:
        return [str(req) for req in parse_requirements(f)]


def read_long_description():
    with open("README.md", "r") as file:
        return file.read()


setup(
    name="plynk",
    version="0.1.2",
    packages=find_packages(),
    install_requires=read_requirements(),
    author="Benjamin Albrechts",
    author_email="benjamin.albrechts@gmail.com",
    description="Easy command over the PLINK software directly from Python",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/achwalt/plynk",
    keywords="plink genomics genetics",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
