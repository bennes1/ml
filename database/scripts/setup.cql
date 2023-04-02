CREATE KEYSPACE IF NOT EXISTS tictactoe
WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };

USE tictactoe;

CREATE TABLE IF NOT EXISTS q_table (
    qid int PRIMARY KEY,
    table_values list<int>
);

CREATE TABLE IF NOT EXISTS steps (
    gameid ascii,
    created_time timestamp,
    model list<ascii>,
    steps list<int>,
    PRIMARY KEY (gameid, created_time)
);
