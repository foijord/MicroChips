
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

pokerlib: pokerlib.o combinations.o
	$(CC) -o $@ $^

pokerlib.o: pokerlib.c pokerlib.h $(DEPS)
combinations.o: combinations.c combinations.h $(DEPS)