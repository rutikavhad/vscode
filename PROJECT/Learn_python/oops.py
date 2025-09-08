#all oops in python

class data:
    def names(self):
        #print(f"hellooo {name}")
        self.name=input("enter name")
         

    def dis (self):
        print("my name is ",self.name)



a=data()
a.names()
a.dis()

from main import printt  # this used to run any progeram other files
#main is program name and printt is a function of this main program

printt() # this call this printt function from main program

#work with json file most imp for our system

import json

data = '{"user":"matrix","attack":"SQLi"}'

# Convert string → dict
parsed = json.loads(data)
print(parsed["attack"])

# Convert dict → JSON string
new_json = json.dumps({"status": "blocked", "ip": "127.0.0.1"})
print(new_json)
