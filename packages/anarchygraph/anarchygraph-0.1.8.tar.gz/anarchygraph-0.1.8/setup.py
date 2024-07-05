# setup.py
from setuptools import setup, find_packages

setup(
    name="anarchygraph",
    version="0.1.8",
    author="Chris Mangum",
    author_email="csmangum@gmail.com",
    description="A decentralized graph system to simulate agents in an artificial reality.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/anarchygraph/",
    packages=find_packages(),
    install_requires=[
        "ipycytoscape",
        "hypothesis",
        "pytest",
        "pyperf",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
