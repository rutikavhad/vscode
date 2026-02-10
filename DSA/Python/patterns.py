'''all type of patterns
******
******
******
******

p1
*
**
***
****
*****
******

p2
******
*****
****
***
**
*

p3
1
1 2
1 2 3
1 2 3 4
1 2 3 4 5

p4
1 2 3 4 5
1 2 3 4
1 2 3 
1 2 
1 

p5
*
**
***
****
*****
******
*****
****
***
**
*

p6
     *
    **
   ***
  ****
 ***** 
******

P7
******
*****
****
***
**
*
p8 *
  * *
  ***
 *****
*******
 *****
  ***
  * *
   *

print("Hello", end="\n")



best in one code p6:

            print(" ",end="")
        else:
            print(" *",end="")
         * 
        * * 
       * * * 
      * * * * 
     * * * * * 
    * * * * * * 
   * * * * * * * 
  * * * * * * * * 
 * * * * * * * * * 


                print("",end="")
            else:
                print("*",end="")
                * 
** 
*** 
**** 
***** 
****** 
******* 
******** 
********* 


                print(" ",end="")
            else:
                print("*",end="")

        * 
       ** 
      *** 
     **** 
    ***** 
   ****** 
  ******* 
 ******** 
********* 
'''

def p1():
    for i in range(5):
        for j in range(i):
            print("*",end="")
        print(end="\n")



def p2():
    n=5
    for i in range(n):
        for j in range(n-i):
            print("* ",end="")
        print(end="\n")



def p3():
    for i in range(1,6):
        for j in range(1,i+1):
            print(j," ",end="")
        print(end="\n")



def p4():
    n=6
    for i in range(n):
        for j in range(1,n-i):
            print(j," ",end="")
        print(end="\n")


def p5():
    n=9
    for i in range(n):
        k=i+1
        if i>n/2:
            k=n-i
        for j in range(k):
            print("* ",end="")
            
        print("")


def pt():
    n=9
    for i in range(1,n):
        k=i+1
        if i>n/2:
            k=n-i
        for j in range(1,k):
            print(j," ",end="")
            
        print("")
            


def p6():
    n=9
    for i in range(n):
        for j in range(n):
            if j<n-i-1:
                print(" ",end="")
            else:
                print("*",end="")
        print("")



def p7():
    n=9
    for i in range(n):
        for j in range(n):
            if j>n-i-1:
                print("* ",end="")
            else:
                print(" ",end="")
        print("")


def P8():
    n=10
    for i in range(n):
        for j in range(n):
            if i<n/2:
                if j>n-i-1:
                    print(" *",end="")
                else:
                    print(" ",end="")
            else:    
                if j<i:
                    print(" ",end="")
                else:
                    print(" *",end="")
        print("")

# ***** 
# *   *
# *   *
# *   *
# *****
def p9():
    n=10
    for i in range(n):
        print("* ",end="")
        for j in range(n):
            if i==0 or i==n-1:
                print("* ",end="")
            else:
                if j==n-1:
                    print("* ",end="")
                else:
                    print("  ",end="")
        print("")
        
        
def p10():
    n=10
    min=n
    for i in range(1,n):
        for j in range(1,n):
            min=n
            mi=n-i
            mj=n-j
            if min>mi:
                min=mi
            if min>mj:
                min=mj
            if min>i:
                min=i
            if min>j:
                min=j
            print(min," ",end="")
            min=n

        print()
        

def P11():
    n=10
    for i in range(n):
        for j in range(n):
            if i<n/2:
                if j>n-i-1:
                    print(i," ",end="")
                else:
                    print(" ",end="")
            else:    
                if j<i:
                    print(" ",end="")
                else:
                    print(n-i," ",end="")
        print("")




# p1()
# p2()
# p3()
# p4()
# p5()
# pt()
# p6()
# p7()
# P8()
# p9()
p10()
# P11()