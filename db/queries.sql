-- Q1: everything in the bank about one club, any game
SELECT g.name AS game, q.prompt, bc.role
FROM bridge_question_club bc JOIN dim_club c ON c.club_id=bc.club_id
JOIN fact_question q ON q.question_id=bc.question_id JOIN dim_game g ON g.game_id=q.game_id
WHERE c.name='Arsenal' ORDER BY g.menu_order LIMIT 8;
-- Q2: questions per game and difficulty
SELECT g.name, COALESCE(d.label,'(not graded)') AS difficulty, COUNT(*) n
FROM fact_question q JOIN dim_game g USING(game_id) LEFT JOIN dim_difficulty d USING(difficulty_id)
GROUP BY g.name, d.label ORDER BY g.menu_order, d.difficulty_id;
-- Q3: by era: cup runs per decade and competition
SELECT s.decade, c.name AS competition, COUNT(*) n
FROM fact_question q JOIN dim_season s USING(season_id) JOIN dim_competition c USING(competition_id)
GROUP BY s.decade, c.name ORDER BY s.decade;
-- Q4: which games has a player appeared in, and when
SELECT p.name, g.name AS game, MIN(dd.date) first_used, COUNT(DISTINCT q.question_id) puzzles
FROM dim_player p JOIN bridge_question_player bp USING(player_id) JOIN fact_question q USING(question_id)
JOIN dim_game g USING(game_id) LEFT JOIN fact_schedule fs ON fs.question_id=q.question_id LEFT JOIN dim_date dd USING(date_key)
WHERE p.name='Steven Gerrard' GROUP BY g.name ORDER BY first_used;
-- Q5: reuse check: Fast Break questions free to reuse (not used in the last 56 days before 2027-01-10)
SELECT COUNT(*) AS free_to_reuse FROM fact_question q
WHERE q.game_id=(SELECT game_id FROM dim_game WHERE slug='fast-break')
AND NOT EXISTS (SELECT 1 FROM fact_schedule fs JOIN dim_date dd USING(date_key) WHERE fs.question_id=q.question_id AND dd.date > date('2027-01-10','-56 days'));
