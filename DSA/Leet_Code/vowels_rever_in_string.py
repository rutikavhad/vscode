class dj:
    def test(self,s):
        a=list(s)
        i=0
        j=len(s)-1

        for k in range(len(s)):
            if i <=j:
                if s[i] not in 'aeiouAEIOU':
                    print(s[i])
                    i+=1
                    # print("foun??d")
                if s[j] not in 'aeiouAEIOU':
                    print(s[j])
                    j-=1
                    # print("fooo")
                if s[i] in 'aeiouAEIOU' and s[j] in 'aeiouAEIOU':
                    a[i], a[j] = a[j], a[i]
                    i+=1
                    j-=1
            else:
                s=''.join(a)
                print(s)
                return