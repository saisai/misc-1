
TARGET = hp97

SRCS = main.cc

INCPATH =
LIBPATH =

CPPFLAGS = $(INCPATH) -D_GNU_SOURCE -Wall -O3 -fomit-frame-pointer

LOADLIBES = $(LIBPATH) -lg++ -lstdc++ -lm

OBJS= $(SRCS:%.cc=%.o)

$(TARGET): $(OBJS)
	$(CXX) -o $@ $(OBJS) $(LDFLAGS) $(LOADLIBES) -s


depend::
	$(CXX) -MM $(CPPFLAGS) $(SRCS) > depend

ifeq (depend,$(wildcard depend))
include depend
endif
