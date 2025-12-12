# compiler
CC = gcc

# compile all programs
all:
	$(CC) urecv.c -o urecv
	$(CC) usend.c -o usend
	$(CC) brain.c -o brain
	$(CC) baby0.c -o baby0
	$(CC) baby1.c -o baby1
	$(CC) baby2.c -o baby2

# run brain program
run_brain:
	./urecv &
	sleep 1
	./brain &
	sleep 1
	./usend

# run baby0 program
run_baby0:
	./urecv &
	sleep 1
	./baby0 params.config &
	sleep 1
	./usend

# run baby1 program (you must set ports manually)
run_baby1_send:
	./baby1 5000 5001

run_baby1_recv:
	./baby1 5001 5000

# run baby2 program (multiple terminals)
run_baby2:
	./baby2


# clean all output files
clean:
	rm -f urecv usend brain baby0 baby1 baby2
