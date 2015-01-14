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

class decimalvector:
    '''An abstract datatype integrating the qualities of numpy's array
    and the class decimal.

    **How to use**

    >>> cf = decimalvector(5, 0.1)
    >>> cf[4] += 1
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
            self._vec = (ctypes.py_object * tupleOrLength)()
            value = Decimal('%s' % default) 
            for i in range(tupleOrLength):
                self._vec[i] = value
        elif isinstance(tupleOrLength, (tuple, list)):
            length = len(tupleOrLength)
            self._vec = (ctypes.py_object * length)()
            for i in range(length):
                self._vec[i] = Decimal('%s' % tupleOrLength[i])
        elif isinstance(tupleOrLength, decimalvector):
            self._vec = tupleOrLength

    def __str__(self):
        return 'decimalvector([%s])' % ', '.join([str(x) for x in self._vec])

    __repr__ = __str__
                                
    def __len__(self):
        return len(self._vec)
                                
    def __neg__(self):
        length = self.__len__()
        vec = decimalvector(length)
        for i in range(length):
            vec[i] = - self._vec[i]
        return vec
                                
    def __abs__(self):
        length = self.__len__()
        vec = decimalvector(length)
        for i in range(length):
            vec[i] = abs(self._vec[i])
        return vec

    def __getitem__(self, keySliceOrInt):
        if isinstance(keySliceOrInt, int):
            return self._vec[keySliceOrInt]
        return decimalvector(self._vec[keySliceOrInt])
        
    def __setitem__(self, keySliceOrInt, values):
        if isinstance(keySliceOrInt, int):
            keySliceOrInt = slice(keySliceOrInt, keySliceOrInt + 1)
        if isinstance(values, (int, float, Decimal)):
            values = [values]
        elif isinstance(values, (tuple, list, decimalvector)):
            assert len(self._vec[keySliceOrInt]) == len(values), \
                'Number of values does not match slice'
            assert any(isinstance(val, (int, float, Decimal)) for val in values), \
                'list must be list of numbers'
        else:
            raise Exception('')
        self._vec[keySliceOrInt] = values
                                
    def __add__(self, dVectorOrNumber):
        dVectorOrNumber = self.toDecimalVector(dVectorOrNumber)
        length = self.__len__()
        assert length == len(dVectorOrNumber), \
            'To be added vectors must have same length'
        vec = decimalvector(length)
        for i in range(length):
            vec[i] = self._vec[i] + dVectorOrNumber[i]
        return vec

    def __radd__(self, dVector):
        return  self.__add__(dVector)

    def __iadd__(self, dVector):
        vec = self.__add__(dVector)
        self._vec = vec._vec
        return self
                                
    def __sub__(self, dVector):
        return self.__add__(-dVector)
                                
    def __mul__(self, dVectorOrNumber):
        dVectorOrNumber = self.toDecimalVector(dVectorOrNumber)
        length = self.__len__()
        assert length == len(dVectorOrNumber), \
            'To be multiplied vectors must have same length'
        vec = decimalvector(length)
        for i in range(length):
            vec[i] = self._vec[i] * dVectorOrNumber[i]
        return vec

    def __rmul__(self, dVectorOrNumber):
        return self.__mul__(dVectorOrNumber)
                                
    def __imul__(self, dVectorOrNumber):
        self = self.__mul__(dVectorOrNumber)
        return self

    def __div__(self, dVectorOrNumber):
        dVectorOrNumber = self.toDecimalVector(dVectorOrNumber)
        length = self.__len__()
        assert length == len(dVectorOrNumber), \
            'To be divided vectors must have same length'
        vec = decimalvector(length)
        for i in range(length):
            vec[i] = self._vec[i] / dVectorOrNumber[i]
        return vec
                                
    def __rdiv__(self, dVectorOrNumber):
        dVectorOrNumber = self.toDecimalVector(dVectorOrNumber)
        length = self.__len__()
        assert length == len(dVectorOrNumber), \
            'To be divided vectors must have same length'
        vec = decimalvector(length)
        for i in range(length):
            vec[i] = dVectorOrNumber[i] / self._vec[i]
        return vec
                                
    def __idiv__(self, dVectorOrNumber):
        self = self.__div__(dVectorOrNumber)
        return self

    def __pow__(self, dVectorOrNumber):
        dVectorOrNumber = self.toDecimalVector(dVectorOrNumber)
        length = self.__len__()
        assert length == len(dVectorOrNumber), \
            'To be exponentiated vectors must have same length'
        vec = decimalvector(length)
        for i in range(length):
            vec[i] = self._vec[i] ** dVectorOrNumber[i]
        return vec
                                
    def __rpow__(self, dVectorOrNumber):
        dVectorOrNumber = self.toDecimalVector(dVectorOrNumber)
        length = self.__len__()
        assert length == len(dVectorOrNumber), \
            'To be exponentiated vectors must have same length'
        vec = decimalvector(length)
        for i in range(length):
            vec[i] = dVectorOrNumber[i] ** self._vec[i]
        return vec

    def __ipow__(self, dVectorOrNumber):
        self = self.__pow__(dVectorOrNumber)
        return self

    def toDecimalVector(self, dVectorOrNumber):
        if isinstance(dVectorOrNumber, (int, float, Decimal)):
            value = Decimal('%s' % dVectorOrNumber)
            return decimalvector(self.__len__(), value)
        if isinstance(dVectorOrNumber, (tuple, list)):
            return decimalvector(dVectorOrNumber)
        if isinstance(dVectorOrNumber, decimalvector):
            return dVectorOrNumber


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
        '''Function to wrap around methods and functions
        '''
        def npWrapFunc(*args):
            '''Function specifying what the wrapping should do
            '''
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
