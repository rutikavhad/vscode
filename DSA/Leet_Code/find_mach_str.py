s=input("enter string ")

p=input("enter patterns to chcek string ")

k=1
for i in range(len(p)):
    if p[i] == ".":
        # print(s[i]," is skip by .")
        print(True)
    elif p[i]=="*":
        # print("all skip by * ")
        print(True)
        break
    elif p[i]==s[i]:
        k
        print(f"match found {s[i]} equal to {p[i]}")
        print(True)
    else:
        # print("not found")        
        print(False)


print(len(p))