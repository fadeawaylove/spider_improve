from setuptools import setup, find_packages

setup(
    name="spidersystem",

    version="0.1",
    description="spidersystem module",
    author="author",
    url="url",
    license="license",

    packages=find_packages(exclude=[]),
    install_requires=[
        "tornado>=5.1",
        "pycurl",
        "selenium"
    ]
)
