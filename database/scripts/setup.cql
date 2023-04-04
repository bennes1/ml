CREATE KEYSPACE IF NOT EXISTS tictactoe
WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };

USE tictactoe;

CREATE TABLE IF NOT EXISTS qtable (
    qid int PRIMARY KEY,
    table_values list<float>
);

CREATE TABLE IF NOT EXISTS game (
    gameid ascii PRIMARY KEY,
    model list<int>,
);
