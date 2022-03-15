import pathlib
from setuptools import setup, find_packages

setup(
    name="trotter",
    version="1.0.1",
    description="Pseudo-lists containing arrangements of item selection types that commonly arise in combinatorics, such as combinations, permutations and subsets.",
    long_description=(pathlib.Path(__file__).parent / "readme.md").read_text(),
    long_description_content_type="text/markdown",
    author="Richard Ambler",
    author_email="rambler@wya.top",
    license="MIT Licence",
    url="https://github.com/ram6ler/python-trotter",
    packages=find_packages(),
    keywords=[
        "combinations",
        "permutations",
        "combinatorics",
        "amalgams",
        "compositions",
        "subsets",
        "compounds",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.9",
)
