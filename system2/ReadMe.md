# SIB Byte Calculator for x86 Instructions

This C program reads x86 assembly instructions from a `.asm` file and calculates the **SIB byte** for instructions of the form:



Functions
1: Binary functions 
 In This function are used to convert Binary number (0,1) to in Decimal number And Hexadecimal number also.

2: reg ,(Register) functions for index and scale. 
Thus function used for get register value like
Ex. eax. 000 
And Store in array from 0 to 5 only and remaining for base

3: basse function for base 
This function used for calculat base value 
I used simple switch case for this .
1:00
2:01
4:10
8:11

This will return number 0,1,2,3 and is op is binary format.

4:The main function 
In this main function accept a file at run time 
Ask to user to pass or enter .asm file address.

...........................................................................................................................................

Program workflow 
Main->get file path form user
             -> Extract required lines [eax+edx*4]  only and pass to variables
                        ->call reg() function two time for this two register 
                                 ->now last call binary () and basse() to get Hexadecimal number
*******************************************************************************************************************************************
        How to Run this Progaram 
            required files:
            1:mod_rm.c C program file.
            2: .asm file (strcpy.asm file in  my case)
            .asm file have,

            mov eax, [ebx + esi*4]
            mov ecx, [edx + edi*8]

        1: Run this mod_rm.c program and it ask for path of .asm file
       **************************************************************
       *-: gcc sib_calculator.c -o sib_calculator # compile program *
       *-: ./sib_calculator     #run and execute code               *
       **************************************************************

