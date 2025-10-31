output=1234
count=0
while output!=6174:
    rev=int(str(output)[::-1])
    #print(rev)
    count+1
    if output>rev:
        output=output-rev

    else:
        output=rev-output


print("found total couunt "+count)