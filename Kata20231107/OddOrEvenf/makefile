CC=gcc
CXX=g++
RM=rm -f
CPPFLAGS=-g $(shell root-config --cflags)
LDFLAGS=-g $(shell root-config --ldflags)
LDLIBS=$(shell root-config --libs)

SRCS=OddOrEven.cpp
OBJS=$(subst .cpp,.o,$(SRCS))

all: OddOrEven

OddOrEven: $(OBJS)
	$(CXX) $(LDFLAGS) -o OddOrEven $(OBJS) $(LDLIBS)
OddOrEven.o: OddOrEven.cpp


.depend: $(SRCS)
	$(RM) ./.depend
	$(CXX) $(CPPFLAGS) -MM $^>>./.depend;

clean:
	$(RM) $(OBJS)

distclean: clean
	$(RM) OddOrEven