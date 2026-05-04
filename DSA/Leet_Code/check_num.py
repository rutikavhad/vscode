def check(s):
        op=False
        if len(s)>1:

            for i in range(1,len(s)):
                a=s[i]
                aa=s[i-1]
                if a.isdigit() or a=="-" or a=="+" or a.lower()=="a" or a==".":
                    op=True
                elif a.lower()=="e" and aa.isdigit():
                    op=True
                else:
                    return False
            return op
        else:
            return True

class nano:
    def runit(s,numRows):
        if len(s)==0:
            return False       
        a=s[0]
        if a.isdigit() or a=="-" or a=="+":
           return check(s)
        elif a=="." and len(s)>1:
            return check(s)
        else:
            return False








n="-.e3"
s=nano
a=s.runit(n,5)
print(a)
# print(len(n))

