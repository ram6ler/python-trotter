# -*- coding: utf-8 -*-
"""
Author: Richard Ambler <rambler@ibwya.net>
Date: January 2015
"""

_factCache = {2: 2}

def _fact(n):
    n = int(n)
    if n <= 1: 
        return 1
    else:
        if (not (n in _factCache.keys())):
            _factCache[n] = n * _fact(n - 1)
        return _factCache[n]
    
def _nPr(n, r): return _fact(n) // _fact(n - r)
    
def _nCr(n, r): return _nPr(n, r) // _fact(r)

def _permWorker(k, elements):
    k = int(k)
    n = len(elements)
    if n <= 1: 
        return elements
    else:
        group = k // n
        item = k % n
        position = n - item - 1 if group % 2 == 0 else item
        dummy = _permWorker(group, elements[0:(n - 1)])
        dummy.insert(position, elements[n - 1])
        return dummy

def _combination(k, r, elements):
    k = int(k)
    r = int(r)
    n = len(elements)
    position = 0
    d = _nCr(n - position - 1, r - 1)
    
    while k >= d:
        k -= d
        position += 1
        d = _nCr(n - position - 1, r - 1)
        
    if r == 0:
        return []
    else:
        tail = elements[(position + 1):]
        dummy = [elements[position]]
        dummy.extend(_combination(k, r - 1, tail))
        return dummy
        
def _selection(k, r, elements):
    k = int(k)
    r = int(r)
    n = len(elements)
    position = 0
    d = _nCr(n + r - position - 2, r - 1)
    
    while k >= d:
        k -= d
        position += 1
        d = _nCr(n + r - position - 2, r - 1)
        
    if r == 0:
        return []
    else:
        tail = elements[position:]
        dummy = [elements[position]]
        dummy.extend(_selection(k, r - 1, tail))
        return dummy
        
def _permutation(k, r, elements):
    k = int(k)
    r = int(r)
    f = _fact(r)
    group = k // f
    item = k % f    
    comb = _combination(group, r, elements)
    return _permWorker(item, comb)
    
def _amalgam(k, r, elements):
    k = int(k)
    r = int(r)
    def element(i):
        nonlocal k
        p = len(elements) ** (r - i - 1)
        index = k // p
        k %= p
        return elements[index]
    return [element(i) for i in range(r)]
            
def _subset(k, elements):
    k = int(k)
    r = []
    for i in range(len(elements)):
        if k & (1 << i) != 0:
            r.append(elements[i])
    return r
    
def _adjustedIndex(k, n):
    return k % n    

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
          '"{}"'.format(self._elements)
            if isinstance(self._elements, str)
            else self._elements
        )

    def _repr(self, name):
        return "{}({}, {})".format(
          name,
          self._r,
          '"{}"'.format(self._elements)
            if isinstance(self._elements, str)
            else self._elements
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
      elements: An indexable object containing the items to be arranged.
        If `elements` is a string, the individual characters will be arranged.

    Example:
    
      >>> a = Amalgams(3, 'abcde')
      >>> len(a)
      125
      >>> a[0:10]
      
      ['aaa', 'aab', 'aac', 'aad', 'aae', 'aba', 'abb', 'abc', 'abd', 'abe']
      
    """

    def __init__(self, r, elements):
        self._r = r
        self._elements = elements
        self._length = len(elements) ** r
         
    def __getitem__(self, k):
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = _amalgam(
              _adjustedIndex(k, self._length), 
              self._r, 
              self._elements
            )
            return "".join(dummy) if isinstance(self._elements, str) else dummy
        
    def __repr__(self):
        return super()._repr("Amalgams")
    
    def __str__(self):
        return super()._str("amalgams")
        
class Combinations(_Combinatoric):
    """A pseudo-list containing combinations of objects.

    The term *combination* is used to refer to an arrangement of items such that
    order is not important and replacement is not allowed.

    An instance of `Combinations` is a pseudo-list in that it does not actually
    store the arrangements but rather presents a mapping as an indexable list.

    Args:
      r (int): The number of items to take.
      elements: An indexable object containing the items to be arranged.
        If `elements` is a string, the individual characters will be arranged.

    Example:
    
      >>> c = Combinations(3, "abcde")
      >>> len(c)
      10
      >>> c[0:]

      ['abc', 'abd', 'abe', 'acd', 'ace', 'ade', 'bcd', 'bce', 'bde', 'cde']
      
    """
    
    def __init__(self, r, elements):
        r = int(r)
        self._r = r
        self._elements = elements
        self._length = _nCr(len(elements), r)
    
    def __getitem__(self, k):
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = _combination(
              _adjustedIndex(k, self._length),
              self._r,
              self._elements
            )
            return "".join(dummy) if isinstance(self._elements, str) else dummy
    
    def __repr__(self):
        return super()._repr("Combinations")   
    
    def __str__(self):
        return super()._str("combinations")
        
class Permutations(_Combinatoric):
    """A pseudo-list containing permutations of objects.

    The term *permutation* is used to refer to an arrangement of items such that
    order is important and replacement is not allowed.

    An instance of `Permutations` is a pseudo-list in that it does not actually
    store the arrangements but rather presents a mapping as an indexable list.

    Args:
      r (int): The number of items to take.
      elements: An indexable object containing the items to be arranged.
        If `elements` is a string, the individual characters will be arranged.

    Example:
    
      >>> p = Permutations(3, "abcde")
      >>> len(p)
      60
      >>> p[0:10]

      ['abc', 'acb', 'cab', 'cba', 'bca', 'bac', 'abd', 'adb', 'dab', 'dba']
      
    """
    
    def __init__(self, r, elements):
        self._r = r
        self._elements = elements
        self._length = _nPr(len(elements), r)
        
    def __getitem__(self, k):
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = _permutation(
              _adjustedIndex(k, self._length),
              self._r,
              self._elements
            )
            return "".join(dummy) if isinstance(self._elements, str) else dummy
        
    def __repr__(self):
        return super()._repr("Permutations")   
    
    def __str__(self):
        return super()._str("permutations")

class Selections(_Combinatoric):
    """A pseudo-list containing selections of objects.

    The term *selection* is used to refer to an arrangement of items such that
    order is not important and replacement is allowed.

    An instance of `Selections` is a pseudo-list in that it does not actually
    store the arrangements but rather presents a mapping as an indexable list.

    Args:
      r (int): The number of items to take.
      elements: An indexable object containing the items to be arranged.
        If `elements` is a string, the individual characters will be arranged.

    Example:
    
      >>> s = Selections(3, "abcde")
      >>> len(s)
      35
      >>> s[0:10]
      
      ['aaa', 'aab', 'aac', 'aad', 'aae', 'abb', 'abc', 'abd', 'abe', 'acc']
      
    """
    
    def __init__(self, r, elements):
        self._r = r
        self._elements = elements
        self._length = _nCr(len(elements) + r - 1, r)
        
    def __getitem__(self, k):
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = _selection(
              _adjustedIndex(k, self._length),
              self._r,
              self._elements          
            )
            return "".join(dummy) if isinstance(self._elements, str) else dummy
    
    def __repr__(self):
        return super()._repr("Selections")   
    
    def __str__(self):
        return super()._str("selections")
    
class Subsets(_Combinatoric):
    """A pseudo-list containing subsets of objects.

    An instance of `Subsets` is a pseudo-list in that it does not actually
    store the subsets but rather presents a mapping as an indexable list.

    Args:
      elements: An indexable object containing the items to be arranged.
        If `elements` is a string, the individual characters will be arranged.

    Example:
    
      >>> ss = Subsets("abcde")
      >>> len(ss)
      32
      >>> ss[0:10]

      ['', 'a', 'b', 'ab', 'c', 'ac', 'bc', 'abc', 'd', 'ad']
      
    """
    
    def __init__(self, elements):
        self._elements = elements
        self._length = 1 << len(elements)
        
    def __getitem__(self, k):
        if isinstance(k, slice):
            return super()._slice(k)
        else:
            dummy = _subset(
              _adjustedIndex(k, self._length),
              self._elements
            )
            return "".join(dummy) if isinstance(self._elements, str) else dummy
    
    def __repr__(self):
        return "Subsets({})".format(
          '"{}"'.format(self._elements)
            if isinstance(self._elements, str)
            else self._elements
        )
    
    def __str__(self):
        return "Indexable pseudo-list of {} subsets of {}".format(
          self._length, 
          '"{}"'.format(self._elements)
            if isinstance(self._elements, str)
            else self._elements
        )
