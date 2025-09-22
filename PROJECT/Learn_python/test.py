#python basic

#this is integer 
x=12
#this is  floting number
pi=3.14
print(type(pi))
print(type(x))

#########################################################################################################################################################
#this is string
name ="string"
print(type(name))

#this is  a boolean type
boolean=True
print(type(boolean))

#########################################################################################################################################################
#this is LIST ordered and changable 
lists=["apple","banana","mango","greps",]
lists[1]="app"
#inbuild function
lists.append("orange")
lists.remove("apple")
lists.insert(1,"peru")
lists.pop()
del lists[1]
print(lists[1])
print(lists[-1])
print(type(lists))
print(lists)
for i in lists:
    print(i)


#########################################################################################################################################################
#this is TUPLE a ordered and unchangeble
TUPLE=("apple","banana","mango","greps",)
print(type(TUPLE))

#try to change

print("this is "+TUPLE[2])

temp=list(TUPLE)
pri=list(temp)
print(pri)
print(temp[1])
print(TUPLE)
temp.sort #in tuple are work sorting 


#########################################################################################################################################################
#this is  a DICTIONARY or SET key-values and pairs no dublicates
set={"apple","banana","greps","mango","k",}

ap=set.clear
#print(set)

#this work as random not ordered

#some inbuild fuctions for set
print(type(set))

set.update("k")
set.update("a") # this take only single latter not full word
set.remove("apple") # error if not exits
set.discard("apple") #not error if not exits
popp=set.pop()
print(popp)
set.clear() #remove all / delete all 

#set.add("hello")
print(set)

#########################################################################################################################################################
#some important  set operations
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}

print(A | B)   # Union → {1,2,3,4,5,6}
print(A & B)   # Intersection → {3,4}
print(A - B)   # Difference → {1,2}
print(A ^ B)   # Symmetric Difference → {1,2,5,6}


#########################################################################################################################################################

# Arithmetic
a, b = 10, 3
print(a + b)   # addition
print(a - b)   # subtraction
print(a * b)   # multiplication
print(a / b)   # division (float)
print(a // b)  # floor division
print(a % b)   # modulus
print(a ** b)  # exponentiation (10^3)

# Comparison
print(a > b)   # True
print(a == b)  # False

# Logical
print(a > 5 and b < 5)  # True
print(a > 5 or b > 10)  # True
print(not(a > b))       # False


#########################################################################################################################################################

#LOOP for and while

arr=[1,2,3,4,5,6,7,8,9]

for i in range(len(arr)):
    print(arr[i])

j=0
while j<9:
    print(arr[j])
    j+=1


#########################################################################################################################################################

#this is  a if and else and elif conditions
age=12

if age==18:
    print("age is 18")
elif age<18:
    print("age less then 18")
elif age>18:
    print("age grater then 18")

#########################################################################################################################################################

#this is  functions -:  def used for define a  fuctions

def fun():
    print("hello this is a function")

def funn(target):
    print("this function with aggregate",target)

def names(name):
    #return f"{name}" # this is a new introduce in python 3.6 f-string =f""
    return "hello "+name

#this call fuctions

fun()
funn(target=12)
print(names(name="rutik"))
#########################################################################################################################################################

#File handling

#write in file

with open("file.text","w") as f:
    f.write("hello this is file")

with open("file.text","r") as p:
    data=p.read()
    print(data)


#########################################################################################################################################################

#2nd phase
#Exception handling try-except

try:
    num=int("abc")

except ValueError:
    print("this not a number")

#without exception handling show  a error : ValueError: invalid literal for int() with base 10: 'abc'
#num=int("abc")


#########################################################################################################################################################

#3rd phase

#file handaling
f=open("file.text","r") # file have a " hello this is  file "
print(f.read())
f.close()
#this will overwrite
p=open("file.text","w")
p.write("this new data in file overwride")
p=open("file.text","r")
print(p.read())
p.close()
#this will append :append in last
p=open("file.text","a")
p.write("hello this is append ")
p.close()
p=open("file.text","r")
print(p.read())

#this is a pandas used to read file
import pandas as pd
df=pd.read_csv("tests.csv")
print(df.head)



import joblib as jp

import fastapi as fast