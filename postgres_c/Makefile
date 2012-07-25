
TARGET = nac.so

SRC = nac.c

LIB_PATH = /usr/local/pgsql/include/server

$(TARGET): $(SRC)
	gcc -shared -lm -L$(LIB_PATH) -I$(LIB_PATH) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET)

test:
	psql test -f nac.sql
