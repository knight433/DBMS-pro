

-- Table to store batting biography
CREATE TABLE BattingBio (
    id BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    preferred_bowlers VARCHAR(255) NULL,
    strength VARCHAR(255) NULL DEFAULT NULL,
    weakness VARCHAR(255) NULL DEFAULT NULL,
    batting_pos INT NULL
);

-- Table to store bowling statistics
CREATE TABLE Bowling (
    id BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    inng INT NULL,
    balls INT NULL,
    runs INT NULL,
    wickets INT NULL,
    avg FLOAT NULL,
    eco FLOAT NULL
);

-- Table to store batting statistics
CREATE TABLE Batting (
    player_id BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    inng INT NULL,
    runs INT NULL,
    balls INT NULL,
    SR FLOAT NULL,
    avg FLOAT NOT NULL,
    highest INT NOT NULL
);

-- Table to store bowling biography
CREATE TABLE BowlingBio (
    id BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    strength VARCHAR(255) NOT NULL,
    preferred_overs INT NOT NULL
);

-- Table to store player information
CREATE TABLE Players (
    id BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    player_name VARCHAR(255) NOT NULL,
    matches INT NOT NULL,
    player_role VARCHAR(255) NOT NULL,
    team VARCHAR(255) NOT NULL
);

-- Table to store batting history
CREATE TABLE BattingHistory (
    id BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    out_to_spin INT NULL,
    str_spin FLOAT NULL,
    avg_spin FLOAT NULL,
    out_to_pace INT NULL,
    str_pace FLOAT NULL,
    avg_pace BIGINT NULL,
    spin_score BIGINT NULL,
    pace_score BIGINT NULL,
    FOREIGN KEY (id) REFERENCES BattingBio (id)
);

-- Table to store bowling history
CREATE TABLE BowlingHistory (
    id BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    L_hand_out INT NULL,
    r_hand_out INT NULL,
    l_hand_avg BIGINT NULL,
    r_hand_avg BIGINT NULL
);

