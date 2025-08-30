data=[1,2,3,4,5,6,7,8,9]


def findtarget(target):

    output=0
    new=0
    k=0
    for i in range(10):
        if output!=target:
            if target>output:
                output=output+i
            else:
                output=output-k
                k=k+1
        else:
            print("found")
            output=output+i

findtarget(target=3)