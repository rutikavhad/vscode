; ************************************************************
;   HARD TEST SUITE — ALL COMPLEX SIB / MODRM / DISP CASES
; ************************************************************

; ---------- 1) Simple MOV tests ----------
mov eax, 0
mov ebx, 1000
mov ecx, eax
mov edx, ebx
mov esi, ecx
mov edi, edx

; ---------- 2) Full ModR/M register pairs ----------
mov eax, ecx
mov ecx, edx
mov edx, ebx
mov ebx, esp
mov esp, ebp
mov ebp, esi
mov esi, edi
mov edi, eax

; ---------- 3) Basic SIB tests (base + index*scale) ----------
mov eax, [ebx + ecx*2]
mov ebx, [ecx + edx*4]
mov ecx, [edx + ebx*8]
mov edx, [esi + edi*2]
mov esi, [edi + eax*4]
mov edi, [eax + esi*8]

; ---------- 4) With displacement (positive) ----------
mov eax, [ebx + ecx*2 + 12]
mov ebx, [ecx + edx*4 + 255]
mov ecx, [edx + ebx*8 + 256]
mov edx, [esi + edi*2 + 4096]
mov esi, [edi + eax*4 + 65536]
mov edi, [eax + esi*8 + 12345678]

; ---------- 5) With displacement (negative) ----------
mov eax, [ebx + ecx*2 - 12]
mov ebx, [ecx + edx*4 - 50]
mov ecx, [esi + edi*8 - 128]
mov edx, [edi + eax*4 - 255]
mov esi, [eax + esi*8 - 4096]
mov edi, [ebp + eax*2 - 20000]

; ---------- 6) Special SIB edge cases ----------
; ESP cannot be an index — assembler must handle correctly
mov eax, [ebx + esp*1]
mov ebx, [esp + ecx*2]

; Base = EBP with no displacement forces DISP32
mov ecx, [ebp + eax*4]
mov edx, [ebp + ecx*8]

; ---------- 7) No index SIB form ----------
mov eax, [ebx + 100]
mov ecx, [edx + 4096]
mov esi, [esp + 1]
mov edi, [ebp + 256]

; ---------- 8) Arithmetic instructions ----------
add eax, ebx
add ecx, edx
sub edx, esi
xor esi, edi
cmp eax, ecx

; ---------- 9) IMUL / DIV ----------
mul eax, ebx
mul esi, edi
div eax, ebx
div esi, edi

; ---------- 10) PUSH/POP/INC/DEC ----------
push eax
push ebx
push ecx
pop edx
pop esi
inc eax
dec ebx
inc ecx
dec edi

; ---------- 11) JMP tests ----------
jmp 0
jmp 100
jmp -50
jmp 1234567

; ---------- 12) Mixed complex cases ----------
mov eax, [esp + edi*8 + 12345678]
mov ebx, [esi + ebp*4 - 300]
mov ecx, [eax + edx*1 + 50]
mov edx, [ebx + esi*2 - 5000]
mov esi, [edi + ecx*8 + 99999]
mov edi, [ebp + esp*2 + 2048]

; ************************************************************
; END OF HARD TEST SUITE
; ************************************************************
