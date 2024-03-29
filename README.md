# Trotter

Welcome to trotter, a set of Python classes for representing sequences
of structures of item selections commonly encountered in combinatorics.

Classes have been defined according to whether order is important, items may be repeated, and length is specified:

| Class          | Order Important | Repetition Allowed | Specified Length |
| :------------- | :-------------: | :----------------: | :--------------: |
| `Amalgams`     |       Yes       |        Yes         |       Yes        |
| `Permutations` |       Yes       |         No         |       Yes        |
| `Compounds`    |       Yes       |         No         |        No        |
| `Compositions` |       No        |        Yes         |       Yes        |
| `Combinations` |       No        |         No         |       Yes        |
| `Subsets`      |       No        |         No         |        No        |

Instances of these classes are indexable pseudo-lists containing all possible selections of items. Since the number of possible arrangements can grow very quickly with the number of items available (and the number of items taken at a time, where applicable), instances do not actually *store* all arrangements but are rather containers of *mappings between integers and arrangements*. This makes it possible to create instances that "contain" very large numbers of arrangements.

## Installation

```
pip install trotter
```

## Example: combinations of words

```py
from trotter import Combinations

items = ["the", "parrot", "is", "not", "pining"]
combos = Combinations(3, items)

print(repr(combos))
```
```
Combinations(3, ['the', 'parrot', 'is', 'not', 'pining'])
```
```py
print(str(combos))
```
```
A pseudo-list containing 10 3-combinations of ['the', 'parrot', 'is', 'not', 'pining'].
```
```py
print(len(combos))
```
```
10
```
```py
for combo in combos:
    print(" ".join(combo))
```
```
the parrot is
the parrot not
the parrot pining
the is not
the is pining
the not pining
parrot is not
parrot is pining
parrot not pining
is not pining
```
```py
print(combos.index("the parrot pining".split()))
```
```
2
```
```py
print(combos[2])
```
```
['the', 'parrot', 'pining']
```

## Example: subsets of characters in a string

The items can be presented as a list of objects or a string, which is interpreted as a list of characters. Here's an example where we use a string.

```py
for i, subset in enumerate(Subsets("spam")):
     print(f"[{i}] '{subset}'")
```
```
[0] ''
[1] 's'
[2] 'p'
[3] 'sp'
[4] 'a'
[5] 'sa'
[6] 'pa'
[7] 'spa'
[8] 'm'
[9] 'sm'
[10] 'pm'
[11] 'spm'
[12] 'am'
[13] 'sam'
[14] 'pam'
[15] 'spam'
```

## Example: *many* permutations!

```py
from trotter import Permutations
letters = "abcdefghijklmnopqrstuvwxyz"
permutations = Permutations(10, letters)
print(permutations)
```
```
A pseudo-list containing 19275223968000 10-permutations of 'abcdefghijklmnopqrstuvwxyz'.
```

That's almost twenty *trillion*! Luckily, we're only dealing with a pseudo-list, and those permutations are not actually stored!

Notice that the word *algorithms* is a ten-letter permutation of the letters of the alphabet. At what position in the pseudo-list is this word?

```py
print(permutations.index("algorithms"))
```
```
6831894769563
```

Luckily, we were able to find it without a brute-force search! Let's check that result...

```py
print(permutations[6831894769563])
```
```
algorithms
```
