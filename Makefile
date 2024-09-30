flags=-Wall -O2  -std=c2x
ldflags=

all: vecdb
	
vecdb: vecdb.o
	cc ${flags} $^ -o $@ 

vecdb.o: vecdb.c
	cc ${flags} -c $^ ${ldflags}

clean: 
	rm -f *.o vecdb