-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

\c tournament;

CREATE TABLE players (
    id serial PRIMARY KEY,
    name text,
    wins integer,
    matches integer
);

-- win = TRUE if player 1 wins, else FALSE
CREATE TABLE matches (
    winner_id serial REFERENCES players (id),
    loser_id serial REFERENCES players (id)
);

