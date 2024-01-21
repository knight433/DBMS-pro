CREATE DATABASE player_stats

--@block
CREATE TABLE team(
    team_name VARCHAR(10) PRIMARY KEY
);

--@block
CREATE TABLE player(
    player_id INTEGER PRIMARY KEY,
    player_name VARCHAR(20),
    No_of_matches INTEGER,
    player_role ENUM('batsman','bowler','all-rounder','wicketkeeper'),
    bowlingType ENUM('left-arm spin','left-arm pace','right-arm spin','right-arm pace'),
    battingType ENUM('right','left'),
    team_name VARCHAR(10) REFERENCES team(team_name) 
);

--@block
CREATE TABLE battingStats(
    player_id INTEGER REFERENCES player(player_id) ON DELETE CASCADE,
    inngs INTEGER,
    runs INTEGER,
    SR DECIMAL(3,2),
    battingAvg DECIMAL(3,2),
    best INTEGER,
    PRIMARY KEY (player_id)
);


--@block
CREATE TABLE bowlingStats(
    player_id INTEGER REFERENCES player(player_id) ON DELETE CASCADE,
    inngs INTEGER,
    wickets INTEGER,
    runs_conceded INTEGER,
    economy DECIMAL(4,2),
    best_bowling_figures VARCHAR(10),
    PRIMARY KEY (player_id) 
);


--@block
CREATE TABLE battingbio(
    player_id INTEGER REFERENCES player(player_id) ON DELETE CASCADE,
    prefered_bowler ENUM('left-arm spin','left-arm pace','right-arm spin','right-arm pace'),
    prefered_position ENUM('top','middle','lower','tail'),
    PRIMARY KEY (player_id)
);

CREATE TABLE battingHistory(
    player_id INTEGER REFERENCES player(player_id) ON DELETE CASCADE,
    runs_to_Lspin INTEGER,
    runs_to_Rspin INTEGER,
    runs_to_Rpace INTEGER,
    runs_to_Lpace INTEGER,
    out_to_Lspin INTEGER,
    out_to_Rspin INTEGER,
    out_to_Rpace INTEGER,
    out_to_Lpace INTEGER,
    balls_Lspin INTEGER,
    balls_Rspin INTEGER,
    balls_Rpace INTEGER,
    balls_Lpace INTEGER,
    batting_avg_Lspin DECIMAL(3, 2),
    batting_avg_Rspin DECIMAL(3, 2),
    batting_avg_Rpace DECIMAL(3, 2),
    batting_avg_Lpace DECIMAL(3, 2),
    elo_rating_Lspin DECIMAL(4, 2),
    elo_rating_Rspin DECIMAL(4, 2),
    elo_rating_Rpace DECIMAL(4, 2),
    elo_rating_Lpace DECIMAL(4, 2),
    PRIMARY KEY (player_id)
);

--@block
CREATE TABLE bowlingbio (
    player_id INTEGER REFERENCES player(player_id) ON DELETE CASCADE,
    prefered_batting_hand ENUM('left', 'right'),
    prefered_position ENUM('new', 'first_change', 'second_change', 'death'),
    PRIMARY KEY (player_id)
);

CREATE TABLE bowlingHistory (
    player_id INTEGER REFERENCES player(player_id) ON DELETE CASCADE,
    runs_conceded_to_left INTEGER,
    runs_conceded_to_right INTEGER,
    wickets_against_left INTEGER,
    wickets_against_right INTEGER,
    balls_bowled_to_left INTEGER,
    balls_bowled_to_right INTEGER,
    bowling_avg_against_left DECIMAL(3, 2),
    bowling_avg_against_right DECIMAL(3, 2),
    elo_rating_against_left DECIMAL(4, 2),
    elo_rating_against_right DECIMAL(4, 2),
    PRIMARY KEY (player_id)
);

--@block
SELECT * FROM player