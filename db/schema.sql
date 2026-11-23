-- TDKO question bank: star schema. SQLite / Cloudflare D1 compatible.
PRAGMA foreign_keys = ON;

-- ---------- dimensions ----------
CREATE TABLE dim_game (
  game_id      INTEGER PRIMARY KEY,
  slug         TEXT NOT NULL UNIQUE,          -- fast-break, cup-run ...
  name         TEXT NOT NULL,
  menu_order   INTEGER,
  per_day      INTEGER NOT NULL,              -- items needed each day (Fast Break 20, Shirt Swap 3, others 1)
  shape        TEXT NOT NULL                  -- what one item is: question, player, xi, chain, grid, list, run ...
);
CREATE TABLE dim_difficulty (
  difficulty_id INTEGER PRIMARY KEY,
  code          TEXT NOT NULL UNIQUE,         -- E M H
  label         TEXT NOT NULL
);
CREATE TABLE dim_question_type (
  qtype_id   INTEGER PRIMARY KEY,
  code       TEXT NOT NULL UNIQUE,            -- multiple_choice, guess_player, name_the_xi, chain, grid, odd_one_out, rank, higher_lower, name_them_all, guess_winner, anagram, word
  label      TEXT NOT NULL
);
CREATE TABLE dim_nation (
  nation_id  INTEGER PRIMARY KEY,
  name       TEXT NOT NULL UNIQUE,
  fifa_code  TEXT
);
CREATE TABLE dim_club (
  club_id    INTEGER PRIMARY KEY,
  name       TEXT NOT NULL UNIQUE,
  code3      TEXT,
  colour1    TEXT, colour2 TEXT,              -- kit colours for our own crests
  nation_id  INTEGER REFERENCES dim_nation(nation_id)
);
CREATE TABLE dim_player (
  player_id  INTEGER PRIMARY KEY,
  name       TEXT NOT NULL UNIQUE,
  position   TEXT,
  nation_id  INTEGER REFERENCES dim_nation(nation_id),
  aliases    TEXT                             -- JSON array of accepted short names
);
CREATE TABLE dim_competition (
  competition_id INTEGER PRIMARY KEY,
  name           TEXT NOT NULL UNIQUE,        -- World Cup, Premier League, FA Cup, Ballon d'Or ...
  kind           TEXT NOT NULL,               -- league, cup, international, award, record
  scope          TEXT NOT NULL                -- club, international, individual
);
CREATE TABLE dim_season (
  season_id  INTEGER PRIMARY KEY,
  label      TEXT NOT NULL UNIQUE,            -- 2012-13 or 2024
  start_year INTEGER NOT NULL,
  decade     TEXT NOT NULL                    -- 1990s, 2000s ... for "any era" queries
);
CREATE TABLE dim_source (
  source_id  INTEGER PRIMARY KEY,
  title      TEXT NOT NULL UNIQUE,
  url        TEXT,
  checked_on TEXT
);
CREATE TABLE dim_date (
  date_key   INTEGER PRIMARY KEY,             -- 20261123
  date       TEXT NOT NULL UNIQUE,
  day_no     INTEGER NOT NULL,                -- puzzle number (No. 1 = 16 Nov 2026)
  weekday    TEXT NOT NULL,
  theme      TEXT                             -- derby day, Boxing Day ...
);

-- ---------- fact ----------
CREATE TABLE fact_question (
  question_id    INTEGER PRIMARY KEY,
  ext_id         TEXT UNIQUE,                 -- stable id used by the site, e.g. cup-run:arg-wc-2022
  game_id        INTEGER NOT NULL REFERENCES dim_game(game_id),
  qtype_id       INTEGER NOT NULL REFERENCES dim_question_type(qtype_id),
  difficulty_id  INTEGER REFERENCES dim_difficulty(difficulty_id),
  competition_id INTEGER REFERENCES dim_competition(competition_id),
  season_id      INTEGER REFERENCES dim_season(season_id),
  source_id      INTEGER REFERENCES dim_source(source_id),
  prompt         TEXT NOT NULL,               -- what the player sees first
  answer         TEXT NOT NULL,               -- the correct answer in words
  narrative      TEXT,                        -- supporting story shown after
  payload        TEXT NOT NULL,               -- the full puzzle as the game reads it (JSON)
  status         TEXT NOT NULL DEFAULT 'approved' CHECK (status IN ('draft','approved','retired')),
  created_at     TEXT NOT NULL DEFAULT (datetime('now')),
  live           INTEGER NOT NULL DEFAULT 0,  -- 1 = contains a stat that can still change (active player); re-checked the day before it plays
  live_note      TEXT,                        -- what to re-check
  checked_on     TEXT                         -- date of the last re-check (YYYY-MM-DD)
);
-- every accepted answer and every wrong option, one row each
CREATE TABLE fact_answer (
  question_id INTEGER NOT NULL REFERENCES fact_question(question_id),
  seq         INTEGER NOT NULL,
  text        TEXT NOT NULL,
  is_correct  INTEGER NOT NULL,               -- 1 = right answer or accepted alias, 0 = distractor
  player_id   INTEGER REFERENCES dim_player(player_id),
  club_id     INTEGER REFERENCES dim_club(club_id),
  nation_id   INTEGER REFERENCES dim_nation(nation_id),
  PRIMARY KEY (question_id, seq)
);
-- when and where a question was used (keeps the 8-week reuse gap honest)
CREATE TABLE fact_schedule (
  date_key    INTEGER NOT NULL REFERENCES dim_date(date_key),
  game_id     INTEGER NOT NULL REFERENCES dim_game(game_id),
  slot        INTEGER NOT NULL,               -- 1..20 for Fast Break, 5/6/7 for Shirt Swap, 1 otherwise
  question_id INTEGER NOT NULL REFERENCES fact_question(question_id),
  PRIMARY KEY (date_key, game_id, slot)
);

-- ---------- bridges (a question about many players, clubs, nations, competitions) ----------
CREATE TABLE bridge_question_player (
  question_id INTEGER NOT NULL REFERENCES fact_question(question_id),
  player_id   INTEGER NOT NULL REFERENCES dim_player(player_id),
  role        TEXT NOT NULL,                  -- answer, clue, option, in_list ...
  PRIMARY KEY (question_id, player_id, role)
);
CREATE TABLE bridge_question_club (
  question_id INTEGER NOT NULL REFERENCES fact_question(question_id),
  club_id     INTEGER NOT NULL REFERENCES dim_club(club_id),
  role        TEXT NOT NULL,
  PRIMARY KEY (question_id, club_id, role)
);
CREATE TABLE bridge_question_nation (
  question_id INTEGER NOT NULL REFERENCES fact_question(question_id),
  nation_id   INTEGER NOT NULL REFERENCES dim_nation(nation_id),
  role        TEXT NOT NULL,
  PRIMARY KEY (question_id, nation_id, role)
);

CREATE INDEX ix_q_game ON fact_question(game_id, difficulty_id, status);
CREATE INDEX ix_q_comp ON fact_question(competition_id, season_id);
CREATE INDEX ix_sched_q ON fact_schedule(question_id);
CREATE INDEX ix_bp_player ON bridge_question_player(player_id);
CREATE INDEX ix_bc_club ON bridge_question_club(club_id);
