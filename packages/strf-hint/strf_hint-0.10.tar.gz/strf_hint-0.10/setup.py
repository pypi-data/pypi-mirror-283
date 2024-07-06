from setuptools import find_packages, setup

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name='strf_hint',
    version='0.10',
    description="Encrypt your own datetime format using strf codes",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marataj/strf_hint",
    author="marataj",
    license="MIT"
)
