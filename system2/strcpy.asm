section .data
	string db "this is string",0
section .bss
	string1 resb 30
section .text
	global main
	extern puts
main:
	mov esi , string
	mov edi,string1
	xor ecx,ecx
	mov al,byte[edi]
	mov byte[edi],al
	inc esi
	inc edi
	cmp byte[esi],0
	jnz lp

	push string1
	call puts
	add esp,4
	ret
