name="hellomynameisrutik"

#skip : name

i=0
while i < len(name)-1:
    if name[i:i+4] =="name":
        print(name[i:i+4])
        print(name[0:i],end="")
        i+=4
        print(name[i:],end="")

    else:
        i+=1


