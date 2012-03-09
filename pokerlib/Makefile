
CC = gcc
LD = gcc

CFLAGS = -O3

.SUFFIXES: .c .h .o

DEPS = constants.h Makefile

.c:
	$(CC) $(CFLAGS) -c $<

PROGRAMS = pokerlib

all: $(PROGRAMS)

clean:
	rm -f $(PROGRAMS) *.o

pokerlib: pokerlib.o combinations.o evaluators.o utils.o deck.o
	$(CC) -o $@ $^

deck.o: deck.c deck.h $(DEPS)
utils.o: utils.c utils.h $(DEPS)
pokerlib.o: pokerlib.c pokerlib.h $(DEPS)
evaluators.o: evaluators.c evaluators.h $(DEPS)
combinations.o: combinations.c combinations.h $(DEPS)
