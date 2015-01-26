from distutils.core import setup

setup(
  name="trotter",
  version="0.5.0",
  author="Richard Ambler",
  author_email="rambler@ibwya.net",
  url="https://bitbucket.org/ram6ler/python_trotter",
  download_url="https://bitbucket.org/ram6ler/python_trotter/get/master.zip",
  #packages=["trotter"],
  py_modules=["trotter"],
  keywords=[
    "combinations", 
    "permutations", 
    "combinatorics", 
    "amalgams", 
    "selections"
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
  description="A set of classes that map integers to particular combinations, permutations and subsets of items.",
  long_description="""\
.. image:: https://bitbucket.org/ram6ler/python_trotter/wiki/trotter_py.png

Welcome to trotter, a set of Python 3 classes for representing arrangements
commonly encountered in combinatorics.

Classes have been defined according to whether order is important and 
whether items may be reused. The main classes supported are:

+------------+---------------+-------------+
|Class       |Order Important|Reuse Allowed|
+============+===============+=============+
|Amalgams    |Yes            |Yes          |
+------------+---------------+-------------+
|Permutations|Yes            |No           |
+------------+---------------+-------------+
|Selections  |No             |Yes          |
+------------+---------------+-------------+
|Combinations|No             |No           |
+------------+---------------+-------------+

Instances of these classes are indexable pseudo-lists containing all possible
arrangements. Since the number of possible arrangements can grow very 
quickly with the number of items available and the number of items taken at a
time, instances do not actually store all arrangements but are rather
containers mappings between integers and containers. This makes it
possible to create instances that represent very large numbers of 
arrangements.

For more information, please see the `trotter wiki <https://bitbucket.org/ram6ler/python_trotter/wiki/About.md>`_ .

An example session:

::
  >>> # Import the Combinations class.
  ... from trotter import Combinations
  >>> 
  >>> # A list of words.
  ... someWords = ["the", "parrot", "is", "not", "pining"]
  >>>
  >>> # A representation of 3-combinations of these words.
  ... c = Combinations(3, someWords)
  >>>
  >>> # Exactly what is c?
  ... print(c)
  Indexable pseudo-list containing 10 3-combinations of ['the', 'parrot', 'is', 'not', 'pining'].
  >>> 
  >>> # How many 3-combinations are there, again?
  ... len(c)
  10
  >>> # Let's see them!
  ... for combo in c: 
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
    
"""
)
