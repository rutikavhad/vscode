def nine(num):
    if num==1:
        print(num)
        return
    print(num)
    nine(num-1)
    print(num)


nine(5)