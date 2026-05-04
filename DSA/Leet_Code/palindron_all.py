def check(s,start,end):
            st=start
            ed=end
            for i in range(start,end+1):
                if start <= end:
                    if s[start]==s[end]:
                        op=True
                        end-=1
                        start+=1
                    else:
                        return False
                else:
                    print(s[st:ed+1])
                    return

class nano:
    def runit(s,numRows):
        start=0
        end=0
        for i in range(len(s)):
            for j in range(len(s)-1,i,-1):
                if s[i] is (s[j]):
                    start=i
                    end=j
                    check(s,start,end)








n="abacacabcddcb"
s=nano
a=s.runit(n,5)
# print(a)

