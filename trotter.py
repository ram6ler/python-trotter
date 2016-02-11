# -*- coding: utf-8 -*-
"""
Author: Richard Ambler <rambler@ibwya.net>
Date: January 2015
"""

# Cache to store calculated factorials.
_factCache = {2: 2}

# n!
def _fact(n):
    n = int(n)
    if n <= 1: 
        return 1
    else:
        if (not (n in _factCache.keys())):
            _factCache[n] = n * _fact(n - 1)
        return _factCache[n]

# Number of permutations of r items taken from n.    
def _nPr(n, r): return _fact(n) // _fact(n - r)

# Number of combinations of r items taken from n.    
def _nCr(n, r): return _nPr(n, r) // _fact(r)

# Returns the items in [arrangement] in the same order as they appear in [items].
def _sortedArrangement(arrangement, items):
    return sorted(arrangement, key = lambda item: items.index(item))

# Checks whether items in [items] are unique.
def _itemsAreUnique(items):
    return len(set(items)) == len(items)
    
# Checks whether all items in [items] are in [universal].
def _itemsExistInUniversal(items, universal):
    return all(item in universal for item in items) 

# Returns the kth Johnson-Trotter permutation of all items.
def _permutationWorker(k, items):
    k = int(k)
    n = len(items)
    if n <= 1: 
        return items
    else:
        group = k // n
        item = k % n
        position = n - item - 1 if group % 2 == 0 else item
        dummy = _permutationWorker(group, items[0:(n - 1)])
        dummy.insert(position, items[n - 1])
        return dummy

# Returns the index of [permutation] in the list of permutations
# of items in [items].
def _inversePermutationWorker(permutation, items):
    if len(permutation) == 1:
        return 0
    else:
        n = len(items)
        index = permutation.index(items[-1])
        group = _inversePermutationWorker(
          [x for x in permutation if x != items[-1]],
          items[0:(-1)]
        )
        return n * group + (n - index - 1 if group % 2 == 0 else index)


# Returns the [k]th combination of r items taken from items.
def _combination(k, r, items):
    k = int(k)
    r = int(r)
    n = len(items)
    position = 0
    d = _nCr(n - position - 1, r - 1)
    
    while k >= d:
        k -= d
        position += 1
        d = _nCr(n - position - 1, r - 1)
        
    if r == 0:
        return []
    else:
        tail = items[(position + 1):]
        dummy = [items[position]]
        dummy.extend(_combination(k, r - 1, tail))
        return dummy
  
# Returns the index of [combination] in the ordered combinations
# of items in [items].
def _inverseCombination(combination, items):
    def helper(combination, items):
        if len(combination) == 0:
            return 0
        else:
            k = 0
            r = len(combination)
            n = len(items)
            itemIndex = 0
            while combination[0] != items[itemIndex]:
                k += _nCr(n - itemIndex - 1, r - 1)
                itemIndex += 1
            return k + helper(combination[1:], items[(itemIndex + 1):])
    return helper(_sortedArrangement(combination, items), items)
      
# Returns the [k]th selection of [r] items taken from [items].   
def _selection(k, r, items):
    k = int(k)
    r = int(r)
    n = len(items)
    position = 0
    d = _nCr(n + r - position - 2, r - 1)
    
    while k >= d:
        k -= d
        position += 1
        d = _nCr(n + r - position - 2, r - 1)
        
    if r == 0:
        return []
    else:
        tail = items[position:]
        dummy = [items[position]]
        dummy.extend(_selection(k, r - 1, tail))
        return dummy

# Returns the index of [selection] in the ordered selections
# of items in [items]. 
def _inverseSelection(selection, items):
    def helper(selection, items):
        if len(selection) == 0:
            return 0
        else:
            k = 0
            n = len(items)
            r = len(selection)
            itemIndex = 0
            while (selection[0] != items[itemIndex]):
                k += _nCr(n + r - itemIndex - 2, r - 1)
                itemIndex += 1
            return k + helper(selection[1:], items[itemIndex:])
    return helper(_sortedArrangement(selection, items), items)

# Returns the [k]th permutation of [r] items taken from [items]. 
def _permutation(k, r, items):
    k = int(k)
    r = int(r)
    f = _fact(r)
    group = k // f
    item = k % f    
    comb = _combination(group, r, items)
    return _permutationWorker(item, comb)

# Returns the index of [permutation] in the ordered permutations
# of items in [items]. 
def _inversePermutation(permutation, items):
    r = len(permutation)
    if r == 0:
        return 0
    else:
        sortedPermutation = _sortedArrangement(permutation, items)
        group = _inverseCombination(sortedPermutation, items)
        return group * _fact(r) + _inversePermutationWorker(permutation, sortedPermutation)

# Returns the [k]th permutation of [r] items taken from [items]. 
def _amalgam(k, r, items):
    k = int(k)
    r = int(r)
    def element(i):
        nonlocal k
        p = len(items) ** (r - i - 1)
        index = k // p
        k %= p
        return items[index]
    return [element(i) for i in range(r)]

# Returns the index of [amalgam] in the ordered amalgams
# of items in [items].
def _inverseAmalgam(amalgam, items):
    r = len(amalgam)
    n = len(items)
    powers = [n ** i for i in range(r)]
    return sum([items.index(amalgam[position]) * powers[r - position - 1] for position in range(r)])

# Returns the [k]th subset of items taken from [items].           
def _subset(k, items):
    k = int(k)
    r = []
    for i in range(len(items)):
        if k & (1 << i) != 0:
            r.append(items[i])
    return r

# Returns the index of [subset] in the ordered subsets
# of items in [items].
def _inverseSubset(subset, items):
    def helper(subset, items):
        k = 0
        n = len(items)
        power = 1
        for index in range(n):
            if items[index] in subset:
                k += power
            power *= 2
        return k
    return helper(_sortedArrangement(list(set(subset)), items), items)

# Returns the [k]th compound of items taken from [items]. 
def _compound(k, items):
    n = len(items)
    for r in range(n):
        groupSize = _nPr(n, r)
        if k >= groupSize:
            k -= groupSize
        else:
            break
    else:
        r += 1
    return _permutation(k, r, items)

# Returns the index of [compound] in the ordered compounds
# of items in [items].
def _inverseCompound(compound, items):
    n = len(items)
    k = sum([_nPr(n, r) for r in range(len(compound))])
    return (k + _inversePermutation(compound, items))
    
# Wrap-around    
def _adjustedIndex(k, n):
    return k % n    

# Base class
class _Combinatoric:
    def __len__(self):
        return self._length

    def __iter__(self):
        return (self[i] for i in range(self._length))

    def _str(self, name):
        return "Indexable pseudo-list containing {} {}-{} of {}.".format(
          self._length,
          self._r,
          name,
          '"{}"'.format(self._items)
            if isinstance(self._items, str)
            else self._items
        )

    def _repr(self, name):
        return "{}({}, {})".format(
          name,
          self._r,
          '"{}"'.format(self._items)
            if isinstance(self._items, str)
            else self._items
        ) 
    
    def _slice(self, s):
        start = 0 if s.start == None else s.start
        stop = self._length if s.stop == None else s.stop
        step = 1 if s.step == None else s.step
        if step > 0:
            while stop < start: stop += self._length
        if step < 0:
            while stop > start: stop -= self._length
        return [
            self[_adjustedIndex(i, self._length)]
            for i in range(start, stop, step)
        ]
        
class Amalgams(_Combinatoric):
    """A pseudo-list containing amalgrams of objects.

    The term *amalgam* is used to refer to an arrangement of items such that
    order is important and replacement is allowed.

    An instance of `Amalgams` is a pseudo-list in that it does not actually
    store the arrangements but rather presents a mapping as an indexable list.

    Args:
      r (int): The number of items to take.
      items: An indexable object containing the items to be arranged.
        If `items` is a string, the individual characters will be arranged.

    Example:
    
      >>> a = Amalgams(3, 'abcde')
      >>> len(a)
      125
      >>> a[0:10]
      
      ['aaa', 'aab', 'aac', 'aad', 'aae', 'aba', 'abb', 'abc', 'abd', 'abe']
      
    """

    def __init__(self, r, items):
        self._r = r
        self._items = items
        self._length = len(items) ** r
         
    def __getitem__(self, k):
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = _amalgam(
              _adjustedIndex(k, self._length), 
              self._r, 
              self._items
            )
            return "".join(dummy) if isinstance(self._items, str) else dummy
        
    def __repr__(self):
        return super()._repr("Amalgams")
    
    def __str__(self):
        return super()._str("amalgams")
        
    def __contains__(self, amalgam):
        return _itemsExistInUniversal(amalgam, self._items)
        
    def index(self, amalgam):
        return _inverseAmalgam(amalgam, self._items) if amalgam in self else -1
        
    
        
class Combinations(_Combinatoric):
    """A pseudo-list containing combinations of objects.

    The term *combination* is used to refer to an arrangement of items such that
    order is not important and replacement is not allowed.

    An instance of `Combinations` is a pseudo-list in that it does not actually
    store the arrangements but rather presents a mapping as an indexable list.

    Args:
      r (int): The number of items to take.
      items: An indexable object containing the items to be arranged.
        If `items` is a string, the individual characters will be arranged.

    Example:
    
      >>> c = Combinations(3, "abcde")
      >>> len(c)
      10
      >>> c[0:]

      ['abc', 'abd', 'abe', 'acd', 'ace', 'ade', 'bcd', 'bce', 'bde', 'cde']
      
    """
    
    def __init__(self, r, items):
        r = int(r)
        self._r = r
        self._items = items
        self._length = _nCr(len(items), r)
    
    def __getitem__(self, k):
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = _combination(
              _adjustedIndex(k, self._length),
              self._r,
              self._items
            )
            return "".join(dummy) if isinstance(self._items, str) else dummy
    
    def __repr__(self):
        return super()._repr("Combinations")   
    
    def __str__(self):
        return super()._str("combinations")
        
    def __contains__(self, combination):
        return _itemsExistInUniversal(combination, self._items) and _itemsAreUnique(combination)
        
    def index(self, combination):
        return _inverseCombination(combination, self._items) if combination in self else -1
        
    
        
class Permutations(_Combinatoric):
    """A pseudo-list containing permutations of objects.

    The term *permutation* is used to refer to an arrangement of items such that
    order is important and replacement is not allowed.

    An instance of `Permutations` is a pseudo-list in that it does not actually
    store the arrangements but rather presents a mapping as an indexable list.

    Args:
      r (int): The number of items to take.
      items: An indexable object containing the items to be arranged.
        If `items` is a string, the individual characters will be arranged.

    Example:
    
      >>> p = Permutations(3, "abcde")
      >>> len(p)
      60
      >>> p[0:10]

      ['abc', 'acb', 'cab', 'cba', 'bca', 'bac', 'abd', 'adb', 'dab', 'dba']
      
    """
    
    def __init__(self, r, items):
        self._r = r
        self._items = items
        self._length = _nPr(len(items), r)
        
    def __getitem__(self, k):
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = _permutation(
              _adjustedIndex(k, self._length),
              self._r,
              self._items
            )
            return "".join(dummy) if isinstance(self._items, str) else dummy
        
    def __repr__(self):
        return super()._repr("Permutations")   
    
    def __str__(self):
        return super()._str("permutations")
        
    def __contains__(self, permutation):
        return _itemsExistInUniversal(permutation, self._items) and _itemsAreUnique(permutation)
        
    def index(self, permutation):
        return _inversePermutation(permutation, self._items) if permutation in self else -1

class Selections(_Combinatoric):
    """A pseudo-list containing selections of objects.

    The term *selection* is used to refer to an arrangement of items such that
    order is not important and replacement is allowed.

    An instance of `Selections` is a pseudo-list in that it does not actually
    store the arrangements but rather presents a mapping as an indexable list.

    Args:
      r (int): The number of items to take.
      items: An indexable object containing the items to be arranged.
        If `items` is a string, the individual characters will be arranged.

    Example:
    
      >>> s = Selections(3, "abcde")
      >>> len(s)
      35
      >>> s[0:10]
      
      ['aaa', 'aab', 'aac', 'aad', 'aae', 'abb', 'abc', 'abd', 'abe', 'acc']
      
    """
    
    def __init__(self, r, items):
        self._r = r
        self._items = items
        self._length = _nCr(len(items) + r - 1, r)
        
    def __getitem__(self, k):
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = _selection(
              _adjustedIndex(k, self._length),
              self._r,
              self._items          
            )
            return "".join(dummy) if isinstance(self._items, str) else dummy
    
    def __repr__(self):
        return super()._repr("Selections")   
    
    def __str__(self):
        return super()._str("selections")
        
    def __contains__(self, selection):
        return _itemsExistInUniversal(selection, self._items)
        
    def index(self, selection):
        return _inverseSelection(selection, self._items) if selection in self else -1
    
class Subsets(_Combinatoric):
    """A pseudo-list containing subsets of objects.

    An instance of `Subsets` is a pseudo-list in that it does not actually
    store the subsets but rather presents a mapping as an indexable list.

    Args:
      items: An indexable object containing the items to be arranged.
        If `items` is a string, the individual characters will be arranged.

    Example:
    
      >>> ss = Subsets("abcde")
      >>> len(ss)
      32
      >>> ss[0:10]

      ['', 'a', 'b', 'ab', 'c', 'ac', 'bc', 'abc', 'd', 'ad']
      
    """
    
    def __init__(self, items):
        self._items = items
        self._length = 1 << len(items)
        
    def __getitem__(self, k):
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = _subset(
              _adjustedIndex(k, self._length),
              self._items
            )
            return "".join(dummy) if isinstance(self._items, str) else dummy
    
    def __repr__(self):
        return "Subsets({})".format(
          '"{}"'.format(self._items)
            if isinstance(self._items, str)
            else self._items
        )
    
    def __str__(self):
        return "Indexable pseudo-list of {} subsets of {}".format(
          self._length, 
          '"{}"'.format(self._items)
            if isinstance(self._items, str)
            else self._items
        )
    
    def __contains__(self, subset):
        return _itemsExistInUniversal(subset, self._items) and _itemsAreUnique(subset)
        
    def index(self, subset):
        return _inverseSubset(subset, self._items) if subset in self else -1


class Compounds(_Combinatoric):
    """A pseudo-list containing compounds (permutations of unspecified length) of objects.

    An instance of `Compounds` is a pseudo-list in that it does not actually
    store the compounds but rather presents a mapping as an indexable list.

    Args:
      items: An indexable object containing the items to be arranged.
        If `items` is a string, the individual characters will be arranged.

    Example:
    
      >>> cp = Compounds("abcde")
      >>> len(cp)
      326
      >>> cp[0:10]
      ['', 'a', 'b', 'c', 'd', 'e', 'ab', 'ba', 'ac', 'ca']
      
    """
    
    def __init__(self, items):
        n = len(items)
        self._items = items
        self._length = sum([_nPr(n, r) for r in range(n + 1)])
        
    def __getitem__(self, k):
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = _compound(
              _adjustedIndex(k, self._length),
              self._items
            )
            return "".join(dummy) if isinstance(self._items, str) else dummy
    
    def __repr__(self):
        return "Compounds({})".format(
          '"{}"'.format(self._items)
            if isinstance(self._items, str)
            else self._items
        )
    
    def __str__(self):
        return "Indexable pseudo-list of {} compounds of {}".format(
          self._length, 
          '"{}"'.format(self._items)
            if isinstance(self._items, str)
            else self._items
        )
    
    def __contains__(self, compound):
        return _itemsExistInUniversal(compound, self._items) and _itemsAreUnique(compound)
        
    def index(self, compound):
        return _inverseCompound(compound, self._items) if compound in self else -1


def test():
    items = ["a", "b", "c", "d", "e"]
    
    print("\n\nCheck 1 - inverse permutation worker \n\n")
    for i in range(_fact(4)):
        permutation = _permutationWorker(i, items)
        inversePermutation = _inversePermutationWorker(permutation, items)
        print("{}\t{}\t-> {}".format(i, permutation, inversePermutation))
    print("\n")
    
    print("\n\nCheck 2 - inverse combinations \n\n")
    for i in range(10):
        combination = _combination(i, 3, items)
        inverseCombination = _inverseCombination(combination, items)
        print("{}\t{}\t-> {}".format(i, combination, inverseCombination))
    print("\n")
    
    print("\n\nCheck 3 - inverse selections \n\n")
    for i in range(35):
        selection = _selection(i, 3, items)
        inverseSelection = _inverseSelection(selection, items)
        print("{}\t{}\t-> {}".format(i, selection, inverseSelection))
    print("\n")
    
    print("\n\nCheck 4 - inverse permutations \n\n")
    for i in range(60):
        permutation = _permutation(i, 3, items)
        inversePermutation = _inversePermutation(permutation, items)
        print("{}\t{}\t-> {}".format(i, permutation, inversePermutation))
    print("\n")
    
    print("\n\nCheck 5 - inverse amalgams \n\n")
    for i in range(125):
        amalgam = _amalgam(i, 3, items)
        inverseAmalgam = _inverseAmalgam(amalgam, items)
        print("{}\t{}\t-> {}".format(i, amalgam, inverseAmalgam))
    print("\n")
    
    print("\n\nCheck 6 - inverse subsets \n\n")
    for i in range(32):
        subset = _subset(i, items)
        inverseSubset = _inverseSubset(subset, items)
        print("{}\t{}\t-> {}".format(i, subset, inverseSubset))
    print("\n")
    
    print("\n\nCheck 7 - inverse compounds \n\n")
    for i in range(326):
        compound = _compound(i, items)
        inverseCompound = _inverseCompound(compound, items)
        print("{}\t{}\t-> {}".format(i, compound, inverseCompound))
    print("\n")
    
    def classTest(instance, item):
        print(instance)
        print("length: {}".format(len(instance)))
        print("\n")
        index = 0
        for arrangement in instance:
            print("{}.\t{}\t".format(index, arrangement))
            index += 1
        
        print("\n")
        print("Item {} in pseudo-list? {}".format(item, item in instance))
        print("Index: {}".format(instance.index(item)))
        print("\n\n")
    
    
    print("\n\nCheck 8 - Amalgams class \n\n")
    classTest(Amalgams(3, items), ["a", "b", "d"])
    
    print("\n\nCheck 9 - Combinations class \n\n")
    classTest(Combinations(3, items), ["a", "b", "d"])
    
    print("\n\nCheck 10 - Permutations class \n\n")
    classTest(Permutations(3, items), ["a", "b", "d"])
    
    print("\n\nCheck 11 - Selections class \n\n")
    classTest(Selections(3, items), ["a", "b", "d"])
    
    print("\n\nCheck 12 - Subsets class \n\n")
    classTest(Subsets(items), ["a", "b", "d"])
    
    print("\n\nCheck 13 - Compounds class \n\n")
    classTest(Compounds(items), ["a", "b", "d"])
    