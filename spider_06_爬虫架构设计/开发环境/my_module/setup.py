from setuptools import setup, find_packages

setup(
    name="spider_system",
    version="0.1",
    description="Custom crawler framework",
    author="daigua",
    url="url",
    license="license",
    packages=find_packages(exclude=[]),
    install_requires=[
        "tornado>=5.1",
        "pycurl",
        "selenium"
    ]
)
