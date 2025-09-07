# 1:file handling
with open("file.text","w") as f:
    f.write("hello good morning") #write

f.close()

with open("file.text","r") as f: #read
    print(f.read())
f.close()

with open("file.text","a")as f: #Append
    f.write("\nthis is append")

f.close()
with open("file.text","r") as f: #read
    print(f.read())
f.close()

#2: exception hadaling

try:
    x=int("abc")
except ValueError as e:
    print("error",e)

finally:
    print("this always run")

#3: functions & arguments

def greet(name,msg="welcome"):
    return f"hello {name} {msg}"

print(greet("king"))
print(greet("king","hi"))

#4: OOPS class and objects

class firwall:
    def __init__(self,name):
        self.name=name
        self.rules=[]
    
    def addrule (self,rule):
        self.rules.append(rule)
    def showrule (self):
        return self.rules


fw=firwall("hello")
fw.addrule("readbook")
fw.addrule("block if not read")

print(fw.showrule)