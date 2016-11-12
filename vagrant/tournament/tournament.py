#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute('''
    DELETE FROM matches;
    ''')
    c.execute('''
    UPDATE players SET matches = 0, wins = 0;
    ''')
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute('''
    DELETE FROM players;
    ''')
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute('''
    SELECT COUNT(*) FROM players;
    ''')
    num = c.fetchall()[0][0]
    c.close()
    return num


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    data = (bleach.clean(name),)
    c.execute('''
    INSERT INTO players (name, wins, matches) VALUES (%s, 0, 0);
    ''', data)
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute('''
    SELECT id, name, wins, matches FROM players
    ORDER BY wins DESC;
    ''')
    players = c.fetchall()
    conn.close()
    return players


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    def updateWinner():
        c.execute('''
        SELECT wins, matches FROM players
        WHERE id = %s;
        ''', (winner,))
        data = c.fetchone()
        wins, matches = data[0], data[1]

        c.execute('''
        UPDATE players SET wins = %s, matches = %s where id = %s;
        ''', (wins + 1, matches + 1, winner,))

    def updateLoser():
        c.execute('''
        SELECT matches FROM players
        WHERE id = %s;
        ''', (loser,))
        matches = c.fetchone()[0]

        c.execute('''
        UPDATE players SET matches = %s where id = %s;
        ''', (matches + 1, loser,))

    conn = connect()
    c = conn.cursor()
    c.execute('''
    INSERT INTO matches (winner_id, loser_id) VALUES (%s, %s);
    ''', (winner, loser,))
    updateWinner()
    updateLoser()
    conn.commit()
    conn.close()
 
 
def swissPairings():
    """
    Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    res = []
    i, n, players = 0, countPlayers(), playerStandings()
    while i < n:
        p1, p2 = players[i], players[i + 1]
        res.append((p1[0], p1[1], p2[0], p2[1]))
        i += 2
    return res



