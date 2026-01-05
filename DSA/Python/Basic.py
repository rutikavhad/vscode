# x = [1, 2, [3, 4, 5], 6, 7] #nested loop

#print(x[2][2])

# x=True
# y=False
# a=x or y
# b=x and y
# c=not y

# # if x is False then y otherwise x
# # if x is False then x otherwise y
# # if x is True then False, otherwise True
# print(a)
# print(b)
# print(c)

# issubclass(bool ,int)

# print(True+False) # true=1 and false=0 op===  1
# print(True+True) ==2
# print(False+False) ==0

# a=43787333333444444444444777777777777777333333333333333355555555555599999999999999999999999999444444444
# print(a) #python have a arbitrary sizes

#------------------------------------------------------------------------------------------------------------------------------------------------#

# a=245.e20
# print(a) # this floting will be work

# a = 2 + 1j
# b = 100 + 10j #  this is a complex number only work j
# print(b)


#------------------------------------------------------------------------------------------------------------------------------------------------#

# 11       #reverce number
# print(''.join(b))
# a=''.join(reversed('hello'))  # reverce string
# print(a)


# num = 100000 # this can not print this 10000=> 000001 only get =? 1
# rev = 0
# while num > 0:
#     rev = rev * 10 + num % 10
#     num //= 10
# print(rev) =>  1 not 000001 ?
 
#------------------------------------------------------------------------------------------------------------------------------------------------#


# a = (1, 2, 3)  # this is *tuppel*
# aa=("hello","wellcome","DJ")
# b=[1,2,3]      # this is *list*
# ab=["hello","wellcome","DJ"]
# c={1,2,3}      # this is *set*  Items must be hashable. 

## set give uniqe no dublicates


# ac={"hello","wellcome","DJ"} # set can't be reverced

# print(type(a))  #tuppel
# print(type(b))  #list
# print(type(c))  #set    


#reversed set list tuppel
# e=reversed(c) # both work int and string ( list and tupple work) not **set** work
# print(list(e)) # want to use a list 


# a=("hello",23,"good",43)

# print(a[1]) #this work good now we can access this using ( *a[0]=hello,a[0][0]=h , a[1]=23 .. *)
                                                        # (if used *a[1][any num]= error this not wokt*)


# a={1:'hello'}

# print(a)



#------------------------------------------------------------------------------------------------------------------------------------------------#
# a="2323.34"  # convert string to int, float etc
# b=float(a)
# c=str(a)

# print(b)
# print(c)



# a="hello"
# k=list(a)
# print(k[1])
# print(k[-2]) # if use  a ( -num ) index start from last(n-1)
# print(list(a))   #list#
# print(tuple(a))  #tupple#
# print(set(a))    #set#   #convert normal string data into tupple set list



#------------------------------------------------------------------------------------------------------------------------------------------------#

# #sorted method

# a={3,6,4,2,1,7,8}
# aa=[3,6,4,2,1,7,8]
# aaa=(3,6,4,2,1,7,8)

# aa.sort() #this method work only in list not work tupple and set
# print(aa)

# print(sorted(aaa)) # work on tupple not work list
# print(sorted(a)) #work on set not work 



# list work    == +---------+---------+---------+
#                 | ptr-->10| ptr-->20| ptr-->30|
#                 +---------+---------+---------+
#     A dynamic array of pointers to Python objects.

#a=[1,2,3,4] #list
# a.append(5)  # 11 method have in this == a.clear a.copya.count a.extend a.index a.insert a.pop a .remove a.reverse a.sort
#print(len(a)) # this will give  a lenght of list

# a.append(1) # apped last
# print("apped",a)
# a.pop(1) # 1 is index
# print("pop",a)
# b=[6,7,8]
# b=a.copy()  # direct overwite data in b list
# print("copy",b)
# print("count 1 =",a.count(1),"time") #1 occucre 2 time in array this count how many time element occucre  
# a.remove(5)
# print("remove",a) # if num avilable in list then they removed if not then error
# a.reverse()
# print("reverse",a) # this reverce a list
# a.sort()
# print("sort ele",a)

# a.clear() # this remove all
# print("clear",a)


#------------------------------------------------------------------------------------------------------------------------------------------------#

# | Operation / Method                   | **List** | **Tuple** |          **Set**          | Description / Example                        |              |
# | ------------------------------------ | :------: | :-------: | :-----------------------: | -------------------------------------------- | ------------ |
# | ✅ **Type**                           |  Mutable | Immutable | Mutable (unique elements) | —                                            |              |
# | `len(x)`                             |     ✅    |     ✅     |             ✅             | Returns number of items → `len([1,2,3]) = 3` |              |
# | `min(x)` / `max(x)`                  |     ✅    |     ✅     |             ✅             | Smallest/largest element                     |              |
# | `sum(x)`                             |     ✅    |     ✅     |             ✅             | Sum of elements (numbers only)               |              |
# | `in`, `not in`                       |     ✅    |     ✅     |             ✅             | Membership test → `2 in [1,2,3]`             |              |
# | `sorted(x)`                          |     ✅    |     ✅     |             ✅             | Returns a sorted list copy                   |              |
# | `reversed(x)`                        |     ✅    |     ✅     |             ✅             | Returns reverse iterator                     |              |
# | `any(x)`                             |     ✅    |     ✅     |             ✅             | True if any element is truthy                |              |
# | `all(x)`                             |     ✅    |     ✅     |             ✅             | True if all elements truthy                  |              |
# | `for item in x:`                     |     ✅    |     ✅     |             ✅             | Iterable support                             |              |
# | `copy()`                             |     ✅    |     ❌     |             ✅             | Shallow copy                                 |              |
# | `count(x)`                           |     ✅    |     ✅     |             ❌             | Count how many times `x` appears             |              |
# | `index(x)`                           |     ✅    |     ✅     |             ❌             | First index of `x`                           |              |
# | `append(x)`                          |     ✅    |     ❌     |             ❌             | Add item at end                              |              |
# | `extend(iterable)`                   |     ✅    |     ❌     |       ✅ (`update()`)      | Add multiple elements                        |              |
# | `insert(i, x)`                       |     ✅    |     ❌     |             ❌             | Insert at position                           |              |
# | `remove(x)`                          |     ✅    |     ❌     |             ✅             | Remove specific element                      |              |
# | `pop([i])`                           |     ✅    |     ❌     |     ✅ (random element)    | Remove and return element                    |              |
# | `clear()`                            |     ✅    |     ❌     |             ✅             | Remove all elements                          |              |
# | `sort()`                             |     ✅    |     ❌     |             ❌             | Sort list in place                           |              |
# | `reverse()`                          |     ✅    |     ❌     |             ❌             | Reverse list in place                        |              |
# | `union(other)` or `                  |     `    |     ❌     |             ❌             | ✅                                            | Combine sets |
# | `intersection(other)` or `&`         |     ❌    |     ❌     |             ✅             | Common elements                              |              |
# | `difference(other)` or `-`           |     ❌    |     ❌     |             ✅             | Items in A not in B                          |              |
# | `symmetric_difference(other)` or `^` |     ❌    |     ❌     |             ✅             | Elements in one but not both                 |              |
# | `isdisjoint(other)`                  |     ❌    |     ❌     |             ✅             | True if sets have no common items            |              |
# | `issubset(other)` / `<=`             |     ❌    |     ❌     |             ✅             | A inside B                                   |              |
# | `issuperset(other)` / `>=`           |     ❌    |     ❌     |             ✅             | A contains B                                 |              |
# | `update(other)`                      |     ❌    |     ❌     |             ✅             | Add all from another set                     |              |
# | `discard(x)`                         |     ❌    |     ❌     |             ✅             | Remove if exists (no error)                  |              |
# | `intersection_update()`              |     ❌    |     ❌     |             ✅             | Keep only common elements                    |              |
# | `difference_update()`                |     ❌    |     ❌     |             ✅             | Remove shared elements                       |              |
# | `symmetric_difference_update()`      |     ❌    |     ❌     |             ✅             | Keep only non-overlapping elements           |              |




#------------------------------------------------------------------------------------------------------------------------------------------------#
# #user input

# a=input("enter number")
# print(a)
# b=input("your name")
# print(b)

#------------------------------------------------------------------------------------------------------------------------------------------------#
#build functions
#e.g.
#print(pow(2,4)) #give power number ex 2^4=16 output is 16

#print(dir(__builtins__)) # this will print prebuild functions
'''prebuild functions
['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BaseExceptionGroup', 'BlockingIOError', 'BrokenPipeError', 'BufferError', 
'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 
'EOFError', 'Ellipsis', 'EncodingWarning', 'EnvironmentError', 'Exception', 'ExceptionGroup', 'False', 'FileExistsError', 'FileNotFoundError', 
'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'InterruptedError', 
'IsADirectoryError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'ModuleNotFoundError', 'NameError', 'None', 'NotADirectoryError', 
'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError', 
'PythonFinalizationError', 'RecursionError', 'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 'StopAsyncIteration', 'StopIteration', 
'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 
'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'ZeroDivisionError', 
'_IncompleteInputError', '__build_class__', '__debug__', '__doc__', '__import__', '__loader__', '__name__', '__package__', '__spec__', 'abs', 'aiter', 
'all', 'anext', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'copyright',
 'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'exit', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 
 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'map', 'max', 'memoryview', 
 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 
 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip']'''

##use helf to get info about this 
#help(max)

#------------------------------------------------------------------------------------------------------------------------------------------------#

import math
# print(math.sqrt(16))# give root of number == 16 => 4

# print(dir(math)) #get math prebuild functions
# from test import hello # use spacific function using from filename import functionname
# import test as dj 
# print(dj.hello())
#assign name for this using "as"
# print(hello())
# import test # this can access other .py file functions
# print(test.hello()) # using filename.functionname can use a this function 


#------------------------------------------------------------------------------------------------------------------------------------------------#
# def funn():
#     return

# print(funn.__doc__)

# import datetime
# print(datetime.date.today()) # date and time
from enum import Enum

# def color(Enum):
#     red=1
#     yellow=2
#     black=3

# print(color(red))

#------------------------------------------------------------------------------------------------------------------------------------------------#
# this will swich case like
# from enum import Enum
# class Color(Enum):
#     red = 1
#     green = 2
#     blue = 3
# print(Color.red) # Color.red
# print(Color(2)) # Color.red
# print(Color['red']) # Color.red


# a=[1,2,2,2,2,3,3,4,4]
# print(a)
# b=set(a) # set give uniqe no dublicates
# print(b)

#------------------------------------------------------------------------------------------------------------------------------------------------#
import operator # this will give  a all math + - / * oprations
# a=4
# b=4
# c=operator.add(a,b)
# print(c)

# c=operator.mod(3,40)  # have a mod oprater 
# print(c) 

#------------------------------------------------------------------------------------------------------------------------------------------------#

import math  
# print(math.log(4)) # have  a log function


#------------------------------------------------------------------------------------------------------------------------------------------------#


#bit shipting
# print(2<<1)

# print(8>>2)
'''
<<
        decimal         binary
ex:     2               10
        4               0100

    ex 2<<2 this shipt by two 00 

        10<<n               n

        ex= 2=10 << 

| Expression | Binary   | Decimal | Explanation |
| ---------- | -------- | ------- | ----------- |
| `2 << 1`   | `100`    | 4       | 2 × 2¹      |
| `2 << 2`   | `1000`   | 8       | 2 × 2²      |
| `2 << 3`   | `10000`  | 16      | 2 × 2³      |
| `2 << 4`   | `100000` | 32      | 2 × 2⁴      |
|  k << n     
k= main binary num ex 2 = 0010 
n= total time shipted left like n = 2 binary=1000 op= decimal= 8

>>
if binary 10000 =using >> op is   10 remove last digit



ex << >>
8>>2==2
2<<2=8

'''

# 
# print(bin(2<<2)) ## this print a binary values of number
# print(bin(8))

#------------------------------------------------------------------------------------------------------------------------------------------------#


# this all used to get squre root of number
# a=4
# b=4
# print(4*4*4*4)
# print(a**b)
# print(math.pow(4,4))

#------------------------------------------------------------------------------------------------------------------------------------------------#


#global and locals variabl

# x=12
# def num():
#     x=13
#     print(x)
#     print(globals()['xQQ'])

# del x # rhis will remove element scope delete this also used in list = del[0:2] delete from 0 to 2 index
# #print(x)
# num()


# foo = 1
# def func():
#     global foo #if want to  print globle value use globle variable_name
#     print(foo)
#     foo = 2
#     print(foo) # this will print a local values not a globle so local used as same name this will be overwrite

# func()

