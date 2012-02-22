
CC = gcc
LD = gcc

CFLAGS = -g -I./

.SUFFIXES: .c .h .o

DEPS = constants.h

.c:
	$(CC) $(CFLAGS) -c $<

PROGRAMS = pokerlib

all: $(PROGRAMS)

clean:
	rm -f $(PROGRAMS) *.o

pokerlib: pokerlib.o
	$(CC) -o $@ $^

pokerlib.o: pokerlib.c pokerlib.h $(DEPS)