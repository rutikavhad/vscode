import statistics
nums1=[2,2,4,4]
nums2=[2,2,2,4,4]
# marge=nums1+nums2
# lens=len(marge)
# a=sum(marge)
# #print(lens)
# b=a/lens
# print(b)

# print(statistics.median(nums1 + nums2))


#         nums1 = [2,2,4,4]
#         nums2 = [2,2,2,4,4]

#         merged = sorted(nums1 + nums2)
#         n = len(merged)

#         if n % 2 == 1:               # odd length
#                 median = float(merged[n // 2])
#         else:                        # even length
#                 median = (merged[n//2 - 1] + merged[n//2]) / 2.0

#         return median


# x=-12323

# strr=str(x)
# rev=''.join(reversed(strr))
# #num=int(rev)
# print(rev)


num = "r2323j45h45"
op = []

for ch in num:
    if ch.isdigit():       # ✅ only keep digits
        op.append(ch)
    else:
        break

b = int(''.join(op))        # ✅ join digits into string → convert to int
print(b)