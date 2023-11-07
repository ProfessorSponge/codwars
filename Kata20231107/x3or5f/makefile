CC=gcc
CXX=g++
RM=rm -f
CPPFLAGS=-g $(shell root-config --cflags)
LDFLAGS=-g $(shell root-config --ldflags)
LDLIBS=$(shell root-config --libs)

SRCS=x3or5.cpp
OBJS=$(subst .cpp,.o,$(SRCS))

all: x3or5

x3or5: $(OBJS)
	$(CXX) $(LDFLAGS) -o x3or5 $(OBJS) $(LDLIBS)
x3or5.o: x3or5.cpp

clean:
	$(RM) $(OBJS)

distclean: clean
	$(RM) x3or5