#old=new=1
def facto(end):
    global new
    global old
    old+=1
    new=new*old
    print(new)
    if old == end:
        return
    facto(end)



    