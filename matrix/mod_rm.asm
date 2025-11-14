section .data 
	
section .text 
	globle main

main: 
	mov [eax+edx*2]
        mov eax, edi*2
	mov ebx, esi*4
	mov edi, eax*4

