section .data
	a dd 87, "hello"
	b db 32,43,"hello"
	c dw 43,55,"hello",0
section .bss 
	r1 resd 3
	r2 resb 3
	r3 resw 5
section .text
	global main
	
main:
	add eax,a
	sub eax,b
	add eax,10
	add ebx,0xFF
	mov ebx,0xFF
	add eax,ebx
	jmp label
	mov eax,[ebp]
	mov eax,[ebp+255]
	mov ecx,[ebp+ecx]
	add eax,[ebx+ebp*4+8]
	add ebx,r1
	inc eax
	dec ecx
	mul eax
	div ebx
label:
	ret
