SQLite version 3.28.0 2019-04-16 19:49:53
Enter ".help" for usage hints.
sqlite> ^C^Csadf asdf^CPRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE test_table(id int, description varchar(10));
INSERT INTO test_table VALUES(1,'foo');
INSERT INTO test_table VALUES(2,'bar');
CREATE TABLE test2(id int, description varchar(10));
INSERT INTO test2 VALUES(1,'foo');
INSERT INTO test2 VALUES(2,'bar');
COMMIT;
