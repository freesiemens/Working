'''
The code is open source under the `Python Software Foundation License 
<http://www.opensource.org/licenses/PythonSoftFoundation.php>`_ 

Decimalvectors
==============

The key abstract datatype eg used in [Kiusalaas]_ is the array type from numpy.
The problem here is that data types inside the array implies numerical precision 
problems like described in eg `Numerical precision in Excel 
<http://en.wikipedia.org/wiki/Numeric_precision_in_Microsoft_Excel>`_.

The solution is to use the Python data type `Decimal 
<http://docs.python.org/library/decimal.html>`_ or a decimalvector.

'''

import ctypes
from decimal import Decimal
import math 

class decimalvector(list):
    '''An abstract datatype integrating the qualities of numpy's array
    and the class decimal.

    **How to use**

    >>> cf = decimalvector(5, 0.1)
    >>> cf[-1] += 1
    >>> cf
    decimalvector([0.1, 0.1, 0.1, 0.1, 1.1])
    >>> times = decimalvector(range(1,6))
    >>> discount = Decimal('1.1') ** - times
    >>> sum(discount * cf) # Present value
    Decimal('1.000000000000000000000000000')
    >>> sum(cf * Decimal('1.1') ** - times) # Present value
    Decimal('1.000000000000000000000000000')
    >>> sum(cf / Decimal('1.1') ** times) # Present value
    Decimal('1.000000000000000000000000000')
    >>> times[:4] - times[1:]
    decimalvector([-1, -1, -1, -1])
'''
    
    def __init__(self, tupleOrLength, default = 1):
        if isinstance(tupleOrLength, int):
            assert tupleOrLength > 0, 'Argument must be a positive integer'
            assert isinstance(default, (int, float, Decimal)), \
                'Default must be a number'
            list.__init__(self, [Decimal('%s' % default)] * tupleOrLength)
        elif isinstance(tupleOrLength, (tuple, list)):
            assert any(isinstance(val, (int, float, Decimal)) for val in tupleOrLength), \
                'List must be a list of number'
            list.__init__(self, [Decimal('%s' % val) for val in tupleOrLength])
        elif tupleOrLength.__class__.__name__ == 'decimalvector':
            self = tupleOrLength

    def __str__(self):
        return 'decimalvector([%s])' % ', '.join([str(x) for x in self])

    __repr__ = __str__
                                
    def __neg__(self):
        return decimalvector([-1 * x for x in self])
                                
    def __abs__(self):
        return decimalvector([abs(x) for x in self])

    def __getslice__(self, start, stop):
        return decimalvector(list.__getslice__(self, start, stop))

    def __setitem__(self, key, values):
        if isinstance(key, int):
            assert isinstance(values, (int, float, Decimal)), \
                'Value must be number'
            list.__setitem__(self, key, Decimal('%s' % values))
        else:
            raise Exception('')
                                
    def __setslice__(self, start, stop, values):
        if isinstance(values, (tuple, list, decimalvector)):
            assert any(isinstance(val, (int, float, Decimal)) for val in values), \
                'list must be list of numbers'
            list.__setslice__(self, start, stop, decimalvector(values))
        else:
            raise Exception('')
                                
    def __add__(self, dVectorOrNumber):
        if isinstance(dVectorOrNumber, (int, float, Decimal)):
            dVector = decimalvector(len(self), dVectorOrNumber)
        elif isinstance(dVectorOrNumber, (tuple, list, decimalvector)):
            assert any(isinstance(val, (int, float, Decimal)) for val in dVectorOrNumber), \
                'list must be list of numbers'
            dVector = decimalvector(dVectorOrNumber)
        else:
            raise Exception('Addition not possible %s' % str(dVectorOrNumber))
        return decimalvector([x + y for x, y in zip(self, dVector)])

    def __radd__(self, dVector):
        return  self.__add__(dVector)

    def __iadd__(self, dVector):
        self = self.__add__(dVector)
        return self
                                
    def __sub__(self, dVector):
        return self.__add__(-dVector)
                                
    def __rsub__(self, dVector):
        return  - self.__add__(dVector)

    def __isub__(self, dVector):
        self = self.__add__(-dVector)
        return self
                                
    def __mul__(self, dVectorOrNumber):
        if isinstance(dVectorOrNumber, (int, float, Decimal)):
            dVector = decimalvector(len(self), dVectorOrNumber)
        elif isinstance(dVectorOrNumber, (tuple, list, decimalvector)):
            assert any(isinstance(val, (int, float, Decimal)) for val in dVectorOrNumber), \
                'list must be list of numbers'
            dVector = decimalvector(dVectorOrNumber)
        else:
            raise Exception('Multiplication not possible %s' % str(dVectorOrNumber))
        return decimalvector([x * y for x, y in zip(self, dVector)])

    def __rmul__(self, dVectorOrNumber):
        return self.__mul__(dVectorOrNumber)
                                
    def __imul__(self, dVectorOrNumber):
        self = self.__mul__(dVectorOrNumber)
        return self

    def __div__(self, dVectorOrNumber):
        if isinstance(dVectorOrNumber, (int, float, Decimal)):
            dVector = decimalvector(len(self), dVectorOrNumber)
        elif isinstance(dVectorOrNumber, (tuple, list, decimalvector)):
            assert any(isinstance(val, (int, float, Decimal)) for val in dVectorOrNumber), \
                'list must be list of numbers'
            dVector = decimalvector(dVectorOrNumber)
        else:
            raise Exception('Division not possible %s' % str(dVectorOrNumber))
        return decimalvector([x / y for x, y in zip(self, dVector)])
                                
    def __rdiv__(self, dVectorOrNumber):
        if isinstance(dVectorOrNumber, (int, float, Decimal)):
            dVector = decimalvector(len(self), dVectorOrNumber)
        elif isinstance(dVectorOrNumber, (tuple, list, decimalvector)):
            assert any(isinstance(val, (int, float, Decimal)) for val in dVectorOrNumber), \
                'list must be list of numbers'
            dVector = decimalvector(dVectorOrNumber)
        else:
            raise Exception('Division not possible %s' % str(dVectorOrNumber))
        return dVector.__div__(self)
    
    def __idiv__(self, dVectorOrNumber):
        self = self.__div__(dVectorOrNumber)
        return self

    def __pow__(self, dVectorOrNumber):
        if isinstance(dVectorOrNumber, (int, float, Decimal)):
            dVector = decimalvector(len(self), dVectorOrNumber)
        elif isinstance(dVectorOrNumber, (tuple, list, decimalvector)):
            assert any(isinstance(val, (int, float, Decimal)) for val in dVectorOrNumber), \
                'list must be list of numbers'
            dVector = decimalvector(dVectorOrNumber)
        else:
            raise Exception('Power not possible %s' % str(dVectorOrNumber))
        return decimalvector([x ** y for x, y in zip(self, dVector)])
                                
    def __rpow__(self, dVectorOrNumber):
        if isinstance(dVectorOrNumber, (int, float, Decimal)):
            dVector = decimalvector(len(self), dVectorOrNumber)
        elif isinstance(dVectorOrNumber, (tuple, list, decimalvector)):
            assert any(isinstance(val, (int, float, Decimal)) for val in dVectorOrNumber), \
                'list must be list of numbers'
            dVector = decimalvector(dVectorOrNumber)
        else:
            raise Exception('Power not possible %s' % str(dVectorOrNumber))
        return dVector.__pow__(self)

    def __ipow__(self, dVectorOrNumber):
        self = self.__pow__(dVectorOrNumber)
        return self


def uFuncConverter(variableIndex):
    '''A decorator to convert python functions to decimalvector functions

    A standard function of 1 variable is extended by a decorator to handle
    all values in a list, tuple or numpy array

    :param variableIndex: Specifies index for args to use as variable.
        This way the function can be used in classes as well as functions
    :type variableIndex: An positive integer

    **How to use:**

    In the example below uFuncConverter is used on the first parameter x:
    
    >>> @uFuncConverter(0)
    ... def test(x, y = 2):
    ...     return x+y
    ... 
    >>> x0 = 4
    >>> x1 = (1, float(2), Decimal('3'))
    >>> x2 = [2, 3, 4]
    >>> x3 = decimalvector(x1) + 2
    >>> print test(x0)
    6
    >>> print test(x1)
    decimalvector([3, 4.0, 5])
    >>> print test(x2)
    decimalvector([4, 5, 6])
    >>> print test(x3)
    decimalvector([5, 6.0, 7])
    '''
    def wrap(func):
        def npWrapFunc(*args):
            if len(args) >= variableIndex:
                before = list(args[:variableIndex])
                arguments = args[variableIndex]
                after = list(args[variableIndex + 1:])
                if isinstance(arguments, (list, tuple, decimalvector)):
                    arguments = decimalvector(arguments)
                    return decimalvector([func(*(before + [x] + after)) 
                                        for x in arguments])
            return func(*args)
        npWrapFunc.__name__ = func.__name__
        npWrapFunc.__doc__ = func.__doc__
        return npWrapFunc
    return wrap

@uFuncConverter(0)
def exp(x):
    '''The exponetial function as a decimalvector function.

    **How to use**

    >>> exp(4)
    54.598150033144236
    >>> exp((1, float(2), Decimal('3')))
    decimalvector([2.71828182846, 7.38905609893, 20.0855369232])
    '''
    return math.exp(x)

@uFuncConverter(0)
def log(x):
    '''The natural logarithmic function as a decimalvector function.

    **How to use**

    >>> log(8)
    2.0794415416798357
    >>> log((1, float(2), Decimal('8')))
    decimalvector([0.0, 0.69314718056, 2.07944154168])
    '''
    return math.log(x)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
