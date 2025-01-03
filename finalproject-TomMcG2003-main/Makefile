CC = /usr/bin/gcc
SRCS = $(wildcard *.c)
CFLGS = -Wall  -Werror -D_FILE_OFFSET_BITS=64
OBJS = $(SRCS:.c=.o)


all: gfs-helper-test grayfs pathnames-test

test: pathnames-test gfs-helper-test

clean:
	rm -f gfs-helper gfs-helper-test grayfs pathnames pathnames-test *.o

gfs-helper.o: gfs-helper.c gfs-helper.h grayfs.h pathnames.h utils.h
	$(CC) $(CFLGS) -c -o gfs-helper.o  gfs-helper.c

gfs-helper-test: gfs-helper.o gfs-helper-test.o pathnames.o utils.o
	$(CC) $(CFLGS) -o gfs-helper-test  gfs-helper.o gfs-helper-test.o pathnames.o utils.o

grayfs: grayfs.c grayfs.h gfs-helper.h pathnames.h utils.h gfs-helper.o pathnames.o utils.o
	$(CC) $(CFLGS) grayfs.c gfs-helper.o pathnames.o utils.o `pkg-config fuse3 --cflags --libs` -o grayfs

pathnames.o: pathnames.c pathnames.h grayfs.h gfs-helper.h utils.h
	$(CC) $(CFLGS) -c -o pathnames.o pathnames.c

pathnames-test: pathnames.o pathnames-test.o utils.o
	$(CC) $(CFLGS) -o pathnames-test  pathnames-test.o pathnames.o utils.o

utils.o: utils.c utils.h
	$(CC) $(CFLGS) -c -o utils.o utils.c
