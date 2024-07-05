"""
General purpose utilities
"""

#===============================================================================
# Imports
#===============================================================================

import itertools
from typing import TypeVar, Dict


#===============================================================================
# Generic Types
#===============================================================================

KT = TypeVar('KT')
VT = TypeVar('VT')


#===============================================================================
# Indexable Dictionary
#===============================================================================

class IndexableDict(Dict[KT, VT]):

    """
    An ordered dictionary, where values can be retrieved by index as well
    as by key, as long as the key is not an int::

        >>> idict = IndexableDict([('foo', 10), ('bar', 30), ('baz', 20)])
        >>> idict['foo'] == idict[0] == idict[-3] == 10
        True
        >>> idict['bar'] == idict[1] == idict[-2] == 30
        True
        >>> idict['baz'] == idict[2] == idict[-1] == 20
        True
    """

    def __getitem__(self, key):
        """
        If `key` is an integer, retrieve the value at that index.
        Otherwise, retrieve the value with the given `key`
        """

        if isinstance(key, int):
            num = len(self)
            if key < -num or key >= num:
                raise IndexError()
            idx = key if key >= 0 else num + key
            return next(itertools.islice(self.values(), idx, idx + 1))

        return super().__getitem__(key)
