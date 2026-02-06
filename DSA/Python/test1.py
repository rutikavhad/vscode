num=9589

old=0
for i in range(10):
    if old!=num:
        old=num
        small =int(''.join(sorted(str(num))))
        big=int(''.join(sorted(str(num),reverse=True)))
        num=big-small
        print(num)



