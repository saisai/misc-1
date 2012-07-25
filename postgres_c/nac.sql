
DROP FUNCTION dist(text, text);

CREATE FUNCTION dist(text, text) RETURNS int
    AS '/home/postgres/c/nac.so' LANGUAGE 'C';

SELECT dist('JO43LD', 'JO21MN');

