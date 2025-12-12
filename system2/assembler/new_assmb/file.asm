; 
; -----------------------------------
;           DATA SECTION
; -----------------------------------
.data

msg1    db "Hello World", 0
bytes   db 1,2,3,4,5
word1   dw 12345
dword1  dd 123456789
qword1  dq 1122334455667788
tbyte1  dt        ; writes 10 zero bytes

; -----------------------------------
;           BSS SECTION
; -----------------------------------
.bss

buf     resb 32      ; reserve 32 bytes
table   resw 16      ; 16 words = 32 bytes
items   resd 8       ; 8 dwords = 32 bytes
block   resq 4       ; 4 qwords = 32 bytes
floatx  rest 3       ; 3 x 10-byte areas = 30 bytes

