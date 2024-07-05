from setuptools import setup, find_packages


setup(
    name="phoenixdatatools",
    version="0.0.2",
    author="Indicium",
    description="""
        Utilities for ready-made Databricks,
        to shorten and facilitate the development of notebooks and jobs
    """,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url='https://bitbucket.org/indiciumtech/databricks-phoenixdatatools/src/main',  # noqa: E501
    packages=find_packages(where="phoenixdatatools", exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[]
)
