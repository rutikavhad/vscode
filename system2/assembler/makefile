assembler: main.o databss.o modrm.o sib.o
	gcc main.o databss.o modrm.o sib.o -o assembler

run_assembler:
	./assembler
clean:
	rm -f *.o app
	rm -f assembler
