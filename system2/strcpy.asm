section .data

section .text
global _start

_start:
    mov eax, [ebx + esi*4]
    mov ecx, [edi + eax*2]
    mov edx, [ebx + ecx*1]
    mov ebx, [esi + edi*8]
