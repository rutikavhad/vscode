# s = "1234567"
# l=len(s)
# for length in range(1, l + 1):
#     for i in range(l - length + 1):
#         print(s[i:i+length], end=", ")

s=['A','B','C','D','E','F','G','H']
#s = "abcdefg"
l=len(s)
for length in range(1, l + 1):
    for i in range(l - length + 1):
        print(s[i:i+length])