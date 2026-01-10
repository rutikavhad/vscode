;This Data Given by ChatGpt For test our Assembler
; ==========================================================
; BIG TEST FILE FOR YOUR CUSTOM ASSEMBLER
; Covers: labels, data, bss, int, register ops, SIB, etc
; ==========================================================

section .data

msg1        db "Hello World!", 10
msg1_end:
msg1_len    dd msg1_end       ; store pointer just to test symbol->imm32
msg1_size   dd 13

num1        dd 12345
word1       dw 0x1122
quad1       dq 0x1122334455667788

string2     db "Another string for testing",0

arr1        db 10,20,30,40,50
arr2        dd 100,200,300,400

section .bss

buffer1     resb 64
buffer2     resd 16
bigspace    resq 32

section .text
global _start

_start:

; ---------------------------------------------------------------
; SIMPLE MOV TESTS
; ---------------------------------------------------------------
        mov eax, 4          ; immediate
        mov ebx, num1       ; symbol immediate
        mov ecx, [num1]     ; absolute memory load
        mov edx, [msg1]     ; load first byte of msg1
        mov esi, [msg1_size]
        mov edi, msg1_size  ; immediate symbol

; ---------------------------------------------------------------
; SIB TESTS (uses your sib.c)
; ---------------------------------------------------------------
        mov eax, [ebx + ecx*2 + 16]
        mov eax, [esp + edi*4 + 128]
        mov edx, [esi + esi*8 + 256]
        mov ecx, [eax + 4]              ; register + disp
        mov ebx, [esp + 32]             ; base + small disp

; ---------------------------------------------------------------
; REGISTER–REGISTER & ARITHMETIC
; ---------------------------------------------------------------
        xor eax, eax
        xor ebx, ebx
        xor ecx, ecx

        add eax, ebx
        sub ecx, eax
        cmp eax, ecx

        inc eax
        dec ebx

        push eax
        pop  eax

; ---------------------------------------------------------------
; MUL / DIV TESTING
; ---------------------------------------------------------------
        mov eax, 20
        mov ebx, 4
        mul eax, ebx
        div eax, ebx

; ---------------------------------------------------------------
; JMP AND LABELS
; ---------------------------------------------------------------
loop_start:
        add eax, 1
        cmp eax, 50
        jmp end_check

middle_point:
        sub eax, 5

end_check:
        cmp eax, 50
        jmp loop_start

; ---------------------------------------------------------------
; INT 0x80 TESTS
; ---------------------------------------------------------------
        mov eax, 4          ; sys_write
        mov ebx, 1          ; stdout
        mov ecx, msg1       ; message
        mov edx, 13         ; length
        int 0x80

        mov eax, 1          ; sys_exit
        xor ebx, ebx
        int 0x80

; ==========================================================
; END
; ==========================================================
