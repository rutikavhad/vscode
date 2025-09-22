section .data
	r1 dd 11
	r2 db "rutik"
	r3 dw "rutik"
section .bss
	r4 resb 4


section .text
	global main

main:
	mov ecx,30
	add ecx,30
	sub eax,30
	add edi,[ecx+edi*4]
	add edi,edi
	add eax,[ecx]
	add edi,[ebp]
