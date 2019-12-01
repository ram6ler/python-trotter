from setuptools import setup
setup(
    name="trotter",
    version="0.9.0",
    author="Richard Ambler",
    author_email="rambler@wya.top",
    url="https://bitbucket.org/ram6ler/python_trotter",
    download_url="https://bitbucket.org/ram6ler/python_trotter/get/master.zip",
    # packages=["trotter"],
    py_modules=["trotter"],
    keywords=[
        "combinations",
        "permutations",
        "combinatorics",
        "amalgams",
        "compositions",
        "subsets",
        "compounds"
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics"
    ],
    description="Pseudo-lists containing arrangements of item selection types that commonly arise in combinatorics, such as combinations, permutations and subsets.",
    python_requires='>=3.8',
    long_description="""


![](https://bitbucket.org/ram6ler/python_trotter/wiki/trotter_py.png)

Welcome to trotter, a set of Python 3 classes for representing arrangements
of arrangements commonly encountered in combinatorics.

Classes have been defined according to whether order is important, items may be repeated, and length is specified.

|Class         |Order Important|Repetition Allowed|Specified Length|
|:-------------|:-------------:|:----------------:|:--------------:|
|`Amalgams`    |Yes            |Yes               |Yes             |
|`Permutations`|Yes            |No                |Yes             |
|`Compounds`   |Yes            |No                |No              |
|`Compositions`|No             |Yes               |Yes             |
|`Combinations`|No             |No                |Yes             |
|`Subsets`     |No             |No                |No              |

Instances of these classes are indexable pseudo-lists containing all possible arrangements. Since the number of possible arrangements can grow very quickly with the number of items available (and the number of items taken at a time, where applicable), instances do not actually *store* all arrangements but are rather containers of *mappings between integers and arrangements*. This makes it possible to create instances that "contain" very large numbers of arrangements.

For more information, please see the [trotter wiki](https://bitbucket.org/ram6ler/python_trotter/wiki/About.md).

## Example session: pick three words

```python
>>> # Import the Combinations class.
... from trotter import *
>>> 
>>> # A list of words.
... items = ["the", "parrot", "is", "not", "pining"]
>>>
>>> # A representation of 3-combinations of these words.
... combos = Combinations(3, items)
>>>
>>> # Exactly what is c?
... print(combos)
A pseudo-list containing 10 3-combinations of ['the', 'parrot', 'is', 'not', 'pining'].
>>> 
>>> # How many 3-combinations are there, again?
... len(combos)
10
>>> # Let's see them!
... for combo in combos: 
...   print(combo)
... 
['the', 'parrot', 'is']
['the', 'parrot', 'not']
['the', 'parrot', 'pining']
['the', 'is', 'not']
['the', 'is', 'pining']
['the', 'not', 'pining']
['parrot', 'is', 'not']
['parrot', 'is', 'pining']
['parrot', 'not', 'pining']
['is', 'not', 'pining']
```

## Example session: subsets of letters in a string

```python
>>> # The items can also be the characters in a string.
... items = "spam"
>>> # The subsets of the letters in this word
... # (notice the first is the empty string):
... for subset in Subsets(items):
...   print(subset)
... 

s
p
sp
a
sa
pa
spa
m
sm
pm
spm
am
sam
pam
spam
```

## Example session: a looooong pseudo-list!

```python
>>> # How many 10-permutations are there 
... # of the 26 letters in the alphabet?
... letters = "abcdefghijklmnopqrstuvwxyz"
>>> permutations = Permutations(10, letters)
>>> # Just how big is this list?
... print(permutations)
A pseudo-list containing 19275223968000 10-permutations of abcdefghijklmnopqrstuvwxyz.
>>> # Wow! Almost twenty trillion! Luckily it's only a
... # pseudo-list and not really stored on the computer!
... # The word "algorithms" is a ten-letter permutation of letters.
... # What is the index of this word in the list of permutations?
... permutations.index("algorithms")
6831894769563
>>> # Found in a split second - take that, Mathematica!
>>> # Let's check:
... print(permutations[6831894769563])
algorithms
```

""",
    long_description_content_type="text/markdown",
    setup_requires=['wheel']
)
