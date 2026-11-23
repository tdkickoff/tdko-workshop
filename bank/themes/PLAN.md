# 2027 themes: agreed 11 Nov 2026
Scope: the 2026/27 season only (Jan–Jun 2027). August onwards to be planned next year. No women's puzzles for now. Gold Cup removed.

Themed days (all 10 games): FA Cup rounds (9–10 Jan, 30–31 Jan, 20–21 Feb, 20–21 Mar, 24–25 Apr, 15 May final),
League Cup (11 Jan, 25 Jan, 28 Feb final), Champions League (20–21 Jan, 27 Jan, 16–17 & 23–24 Feb, 9–10 & 16–17 Mar,
6–7 & 13–14 Apr, 27–28 Apr, 4–5 May, 5 Jun final), AFCON final (17 Jul).
International windows (22–30 Mar, 7–15 Jun): ONLY the days England play. Fixtures not confirmed yet
(Nations League A3 / possible quarter-finals in March; Nations League finals 9–13 Jun) — fill in once announced.

Rules
- Tag every puzzle with its competition(s): fa-cup, league-cup, ucl, intl, afcon (retro-tag No. 1–28).
- Non-themed days hold back a competition's material ahead of its themed days.
- Reuse: allowed, but never within 6 months, and never twice in the same competition run. Keep a "last used" log; weekly checks block anything too recent.
- Flag themed weeks in advance in the weekly review.

Game ideas
- Tiki-Taka-Toe: competition columns/rows: winners, losers (beaten finalists), final venues/played a final at X, cups won — and the same within a period (e.g. "Won the FA Cup in the 2000s").
- Link Up Play: links via the competition — scored in the final, man of the match in the final; if not possible, fellow winners.
- Squad Goals: that competition's final XIs. Top Four / Ranked Highly: competition records. Offside: won it / never won it.
- Fast Break: all 20 questions on the competition. WTB / Mixer / Shirt Swap: players known for it.

# 2027: subscription plan (added 11 Nov 2026, ideas from the owner)
Paid tier features:
- Saves and progress across devices (accounts)
- Access to the archive (play past days)
- Leaderboards: world, continent, country and county
- Player stats (personal history, averages, streaks per game)
- Private leagues with friends
- No ads
- Submit a question (credited by name when used)
- Make your own quiz from our catalogue of puzzles
- Early access to new features and games before release
Depends on: the database (D1) + accounts/sign-in; ads must exist first for "no ads" to be a benefit; payments provider (e.g. Stripe); location for regional leaderboards (ask the player for country/county rather than tracking).
Free tier stays: all 10 daily puzzles, streaks on one device, share cards.

# Tester codes: TDKO-VW8UP until Sun 15 Nov 2026 (soft-launch testers). From Mon 16 Nov all devices leave test mode once; new code TDKO-YFK9B (use tdko.app/?tester=TDKO-YFK9B) for testing future features. Done in gate.html — no manual change needed on the day.

# Quality standards (agreed 12 Nov 2026)
- Every fact checked against Wikipedia / match reports before review; sheet shows the source. Nothing from memory alone.
- Grow the Tiki-Taka-Toe player list weekly so valid answers are rarely "not recognised". Review Tiki in a few weeks with real feedback.
- "Report a problem" link under every game → email to hello@tdko.app with game, No. and date.
- Difficulty: watch stats page finish rates; if a game's finish rate is under ~60%, make it easier. Easier early in the week, tougher at the weekend.

# 2027: app (added 12 Nov 2026)
1. Installable from the website (home-screen app: icon, splash, offline, "Add to home screen" prompt). Small, free. Can be done any time.
2. Google Play: wrap tdko.app (Trusted Web Activity) so site updates flow straight into the app. Owner needs a Google Play developer account ($25 one-off, ID check).
   New personal accounts must run a closed test with 12+ testers for 14 days before going public. Draft data-safety form, rating, listing and screenshots.
3. Apple App Store: needs real app features to pass review (daily push notification, streak reminders, maybe a widget). $99/yr developer program; builds need a Mac/Xcode or a cloud build service.
   In-app subscriptions go through Apple (15–30% cut) — factor into the subscription plan. Best done alongside the database, accounts and subscriptions.

# Parked: data-mined Toughies (15 Nov 2026), ready to turn into posts when wanted
1. The Calendar Man: David May, only PL winner with a month as surname.
2. The Shinji Coincidence: first two Japanese PL winners both named Shinji (Kagawa 2013, Okazaki 2016).
3. Paint the Trophy: Brown (1999), Gray (2016), White (Ben White, 2026).
4. The Cole Collection: Andy/Ashley/Joe Cole; Cole Palmer (2023) as first name.
5. Double D Champions: Dion Dublin, Didier Drogba, Damien Duff, Danny Drinkwater (post-2016 checked squad by squad).
Source data: bank/trivia/medals_to_2016.txt + Wikipedia list of PL winners (to 2025-26).

## Game in the locker: Clean Sweep (added 15 Nov 2026; built 18 Nov in the Training Ground only: clean-sweep.html, lists in bank/cleansweep/lists.json, testOnly in the menu)
- Timed list game: name every player who fits a prompt (e.g. "every player signed by Liverpool from Everton") before the clock runs out. Time allowed depends on difficulty / list length.
- Inspired by JOE's "name these players by their transfer history" quizzes.
- Use only if a current game isn't landing in the stats; swap it in for that game.
- Varied prompts, not just transfers: top scorers, clean sheets, appearances, moves between two clubs, caps for a country, goals + assists combined, moves between rival clubs, and combinations (e.g. top 10 Premier League scorers from Argentina). Combinations are the hook: they make the game niche and stop it being a Wikipedia list anyone has seen.
- Every list is exactly 10, 15 or 20 names. Clock (user, 19 Nov 2026): 10 names = 3 min, 15 = 4 min, 20 = 5 min.
- For ranked lists (most goals etc.) the cut-off must be clean: no tie straddling the last place, and an "as of" date in the note.
- Name shortlist: Clean Sweep (favourite), Full Squad, Roll Call, The Full 90. (Deadline Day / Transfer Window dropped as too transfer-specific.)
- Every list must be complete and source-checked (Wikipedia / Transfermarkt), with accepted spellings and aliases, like Tiki-Taka-Toe.
- Answer entry (proposed): one typing box, no submit button: a name is accepted the moment it matches. No dropdown (it would give answers away).
  Match on surname alone. If two or more players in the list share that surname, typing it once gets all of them (user's call, 15 Nov).
  Ignore accents, capitals, hyphens and apostrophes (as in the current games). Known nicknames and short names as aliases (e.g. "Kun").
  Small typos accepted: 1 wrong letter for names of 5–8 letters, 2 for longer names. Short surnames must be exact.
  Wrong guesses cost nothing except time. Clock and the answers you have so far stay on screen; unfound names are revealed at full time.
- Big-match themes (on top of the 2027 competition schedule): on derby / big-fixture days the Clean Sweep list matches the game,
  e.g. Arsenal v Spurs → players who played for both; El Clásico → a Barcelona/Real Madrid list. User will add these dates to the 2027 schedule.
  Fixture dates move for TV, so re-check each themed date about two weeks before and shift the puzzle if the game moves.

# Tiki-Taka-Toe: next batch ideas (user, 17 Nov 2026)
- Mix up the accolades: league titles across Europe (Premier League, Scottish Premiership, Ligue 1, La Liga, Serie A, Bundesliga, Eredivisie), domestic cups, golden boots and assist awards.
- Rows/columns can be famous youth academies instead of clubs (e.g. La Masia, Ajax, Man Utd academy).
- RULE (17 Nov): club x achievement = achieved WHILE at that club. Nationality x achievement = at any point. Every square must have its full answer list available.
- Square size (user, 17 Nov): niche criteria = small answer pool, and that's fine. Aim for each square to have roughly 3-40 valid answers.
  Avoid giveaway squares, e.g. Real Madrid x Champions League (165 answers) or a club crossed with its own league (AC Milan x Serie A).
  Use check_grids.py counts when building each batch.

# Social posting (to look at w/c 23 Nov 2026)
- Posting the same thing to Instagram, Facebook, X and TikTok separately takes too long. Compare scheduling tools that post to all four at once (e.g. Meta Business Suite for FB+IG; Buffer, Later, Metricool for all four), on cost, the free tier, TikTok support and scheduling Reels/Stories.

# Fast Break variety rules (user, 17 Nov 2026), applied to every new batch
- Keep the gradual difficulty (easy Q1-10, medium Q11-19, hard Q20), but make each day as varied as possible.
- No more than 2 questions on one club, and no player appearing twice in a day (as subject or answer).
- Each question format at most once a week (e.g. "Which country hosted the X World Cup?", "Who won Euro X?", "In which city are X based?").
- No answer that appeared in any game the day before (e.g. Top Four "Arsenal goals" then "Arsenal's record scorer" the next day).
- Mix the topics each day: clubs, countries, grounds, managers, transfers, finals, records, awards, eras, and different leagues and countries.
- The weekly check script flags anything that breaks these rules before the sign-off sheet goes out.

# Reminders
- After 30 Nov 2026: remove the one-time launch-day progress wipe (reset.html "Launch clear" block and its copy in the menu).

# Clash rule (user, 18 Nov 2026)
- No player may appear in two games on the same day WHERE one of them has a small answer pool (1-4 players):
  Who's That Baller, In The Mixer, Shirt Swap, Offside's odd one out, Top Four. (Link Up Play chain also kept clear.)
- Games with a large answer pool (Clean Sweep lists, Tiki-Taka-Toe grids, Squad Goals XIs, Offside's eight, Ranked Highly, Fast Break text)
  are excused from clashing with each other. Check: bank/cleansweep/check_cs.py (and bank/final/clash.py for the rest).

# Social video status (user, 19 Nov 2026)
- All 12 reels in social/reels-final (neon trailer, Fast Break neon, 10 game reels) are posted or scheduled.
- Clean Sweep reel: wanted (user, 19 Nov). Hall of Fame + Journey highlights set up (user, 19 Nov).

# Clean Sweep difficulty rules (user, 19 Nov 2026)
- All-time scorer lists that include pre-2000 players = hard. Lists of post-2010 players = easy/medium. User reviews and may override.
- Spread for streaks: never three hard days in a row (aim for no back-to-back). Easy Mondays, hard Sundays; launch week starts easy.
- Same list type spaced out: club scorer lists and World Cup lists at least 3 days apart, others 2.

# Clean Sweep sign-off (user approved 19 Nov 2026)
- No. 8-28 lists, levels and order approved (bank/cleansweep/lists.json); clock 3/4/5 min.
- No. 29-35 lists approved (bank/cleansweep/next_week.json, POOL2 in pool.py); run check_cs.py once the other games' No. 29-35 puzzles exist and reshuffle if anything clashes.
- Avoid subjective lists (e.g. "important goals"); "every goal in a final over a recent range" is fine.

# 2027 derby / big-match theme days (user's schedule, added 19 Nov 2026; source: 2027_Football_Schedule.xlsx)
- 7 Feb PSG v Marseille · 14 Feb Inter v Milan · 6 Mar Dortmund v Bayern · 20 Mar Man City v Man Utd (same weekend as FA Cup QFs)
- 18 Apr Roma v Lazio · 1 May Arsenal v Spurs + Sunderland v Newcastle (split day) · 9 May Real Madrid v Barcelona
- Theme-day puzzles on the EASY side (niche for a global audience). Reusing past puzzles that fit the theme is allowed (user, 19 Nov).
- 1 May split: games with the highest completes (stats page) get Arsenal v Spurs, the rest Newcastle v Sunderland.
- Re-check every derby date ~2 weeks before (TV moves).
- 20-21 Mar: Sat 20 = Manchester derby day, Sun 21 = FA Cup QF day. If City or United are still in the FA Cup the derby may be moved: include it in the 2-week date re-check.
- Gold Cup, Women's FA Cup final and Women's World Cup final stay OUT (user, 19 Nov: old copy of the sheet).

# Question bank / database (agreed 19 Nov 2026)
- Development starts December 2026, ready before the first 2027 theme days (FA Cup 3rd round, 9-10 Jan).
- Scope: puzzle bank with tags (competition, clubs, players, theme) + last-used dates for reuse and clash checks; site loads only today's puzzle per game.
- Accounts/leaderboards/subscriptions come later with the 2027 subscription plan.

# Live lobbies: "Play live with friends" (agreed 19 Nov 2026, target: live before end of 2026)
- Host creates a lobby, friends join by link + nickname (strict word filter: nothing offensive at all). No accounts.
- All 11 games. Fast Break first (same question, same clock, speed scores). Clean Sweep = race to name most.
  WTB / Mixer / Shirt Swap: everyone guesses each clue round together; ties broken by time. Tiki-Taka-Toe / Squad Goals: fastest with fewest hints wins.
- Lobby games do NOT count towards daily scores, streaks or stats. Puzzles drawn at random from the bank, ONLY puzzles already released (never future dailies).
- Timed tightly to limit looking answers up (detail later).
- Free: up to 5 players. Bigger lobbies (up to ~20) for subscribers later; that needs accounts/payments, so 5 cap at launch.
- Needs: question bank first (Dec), Cloudflare Workers paid plan (~$5/month, Durable Objects) on the owner's account.
- Order (user, 19 Nov): question bank/DB first, then Fast Break Live. Review priority of the other games once the DB is done.

# Social Kit page (19 Nov 2026)
- Pinned artifact "TDKO Social Kit" holds every final video, image and caption. Rebuild with social/kit/build_kit.py and republish whenever a new asset is made.

## Game in the locker: "Route to the final" idea (user, 20 Nov 2026), name: Cup Run or Road To Glory
- Show the teams a trophy winner beat on the way (one round at a time, ending with the final opponent); guess the winner.
- Group stages: show ALL group fixtures together as one round (user, 20 Nov).
- Hints: year, competition, final score. Fewer reveals/hints = more points.
- Pools: World Cup, Euros, Copa América, AFCON (last ~30 years); FA Cup, League Cup, UCL, Europa League, Conference League; other European domestic cups.
- Badges: club badges are trademarks, so not on the public site; use national flags for international tournaments and simple club-colour shields + names for clubs (decision pending).
- Fits the 2027 competition theme days (FA Cup rounds, League Cup final, UCL final, AFCON final).

## Cup Run (game 12) — 20 Nov
- Public from Mon 23 Nov (No. 8) with Clean Sweep; one run a day. No. 8–28 international (approved 20 Nov).
- Club runs join from No. 29 (kit-colour crests, user approved the crest approach). Sources: Wikipedia final "Route to the final", cross-checked where gaps.
- Data: bank/cuprun/intl.py, club.py, build_runs.py -> runs.json; flags.js; signoff.py -> sign-off artifact Uhz8BJ8jjskgQDBPZaFThU.
- Format: winner's score first; two-legged ties "agg x–y"; European groups "h, a" per opponent.

## Fast Break grading rules (user, 20 Nov)
- Naming the stadium or city of a final = Hard.
- AFCON / Asian Cup questions = Hard (at least medium-hard).
- Anything pre-1990 = medium-to-hard, never Easy.
- Days can carry more than one Hard; each day = 20, ordered easy → medium → hard.
- Fast Break No. 29–35 approved 20 Nov (140 Qs, bank/fb2/week29_days.json); Toffees + Cottagers dropped as repeats.

## Week No. 29–35 content: progress (20 Nov, paused on usage limit)
- DONE + live: Fast Break, Clean Sweep, Cup Run.
- Shirt Swap drafted (bank/wk29/ss.json; names from approved Squad Goals XIs / sourced lists), not yet signed off.
- Squad Goals in progress. Lineups sourced so far: rma24 (Real Madrid, 2024 UCL final, capt. Nacho), psg25 (PSG, 2025 UCL final, capt. Marquinhos), mun24 (Man Utd, 2024 FA Cup final, capt. Bruno Fernandes).
  Still to fetch: Spain Euro 2024 final, Inter 2010 UCL final (dfb datencenter links), Italy Euro 2020 (dfb .../2020-in-europe/final/2261445), Portugal Euro 2016 (cavac.at UEFA_Euro_2016_Final).
  Spain 2026 WC final XI: only one source (SI), clubs unknown — skipped for now.
- Remaining games: WTB, Mixer, Link Up, Offside, Top Four, Tiki, Ranked Highly. Clash check (small-pool) once all drafted.
- Bank: loader live with stable ids (db/ids.json, copy in functions/api/bank/_ids.json). Next DB step after content: daily files generated from the bank.
- 20 Nov 15:00: also sourced (dfb datencenter): Spain Euro 2024 XI (Simón; Carvajal, Le Normand, Laporte, Cucurella; Rodri, Fabián Ruiz; Yamal, Olmo, Nico Williams; Morata),
  Inter 2010 XI (Júlio César; Maicon, Lúcio, Samuel, Chivu; Zanetti, Cambiasso; Sneijder, Eto'o, Pandev; Milito — positions to confirm),
  Italy Euro 2020 XI (Donnarumma; Di Lorenzo, Bonucci, Chiellini, Emerson; Barella, Jorginho, Verratti; Chiesa, Insigne, Immobile). Captains not stated by dfb.
  Still need: 7th XI (Portugal Euro 2016 via cavac.at), captains/positions confirmation. Weekly usage limit hit; resumes after 21 Nov 23:00.

## 22 Nov: Cloudflare free-plan limit hit (Fri 20 Nov afternoon), user upgraded to paid Friday evening
- Likely cause: D1 daily write limit (100k rows/day free) — bank loads that day wrote ~30k+ rows (plus index writes) on top of site traffic.
- Fix built (preview/self-heal): /api/backfill + footer snippet; each device re-sends last 7 days of saved progress once a day; dedupe via plays_seen.
- Rule: big bank loads only off-peak, and only the new rows.
- 22 Nov: wk29 drafts in bank/wk29: ss, squad, tf, rh, off (sign-off artifact FVL9Az9m4PgxrDrbjmwVTy). WTB research started (wtb_research.json: Weah, Laudrup, Juninho, Klinsmann, Kaká; Cantona page lacked stats, Totti redirect). Still to do: 2 more WTB + blurbs, Mixer x7, Link Up x7, Tiki x7, then clash check.
- NEXT WEEK (user, 22 Nov): rework the stats page: some metrics still don't make sense, and the user wants to change how the page is used. Ask for specifics first.
- WTB wk29: 6 researched (Laudrup, Juninho, Klinsmann, Kaká, Batistuta, Šuker); Weah dropped (early club stats unpublished). Need 1 more + aliases + day placement.
- 22 Nov: Social Kit now has 14-cup-run-reel.mp4 (shots from video/all/cr-shots.js, promo uses cry-facup-2025, which is removed from SPARE so it never goes live) and the combined "Two new games" poster (social/cs-cr, feed + story, captions.txt). Reel end card now says "One of 12".
- 22 Nov: Stats page v2 on branch preview/stats-v2 (filters, 2 charts, totals/uniques table, /api/stats). Stats has its own code (private, user-chosen), checked server-side by SHA-256 in functions/api/stats.js; header x-tdko-stats; devices keep it in localStorage tdko-stats-key. Tester/Training Ground code unchanged. New tracking: page_views/page_viewers (game page opens), rstart/rgaveup replay events, from 23 Nov.
- 23 Nov: visits fix live. Footer: first page of a new day = a visit (sessionStorage tdko-sess holds the day). /api/stats unique visits: plays_seen only fills days before counting began (site < 18 Nov, games < 23 Nov). hit.js ignores bot/crawler/preview user agents. Today (23 Nov) may still show unique > total from early-morning visits before the fix.
- 23 Nov: Tiki-Taka-Toe data gap: 990/1196 players are 'partial' (clubs only from honours lists) so club x club/league/country squares can't confirm correct answers. Fixed 6 named players via bank/tiki/careers.json (live). PARKED by user (thinking through mechanics; "there may be an easier solution"). Options discussed: research full careers (helpers or batches) or rule that every square has a closed-list axis. Don't start without the user.
- 23 Nov: BANK IS MASTER (branch preview/bank-master, awaiting go live). db/export.py builds daily data from tdko.db (identical to the old files); bank/final/inject.py now reads the bank; db/bank.py adds puzzles (never wipes); db/checks.py = 8-week reuse, same-day clash, gaps; db/restore.py rebuilds tdko.db from functions/api/bank/_seed.js; db/load.py is a guarded one-off migration.
- 23 Nov: Fast Break gap-filling (user idea: same question shape for every year since 1990). bank/fbgap: classify.py (coverage map, ~850 gaps), finals.py (sourced finals data), make_batch1.py -> batch1.json (349 Qs: FA Cup, League Cup, UCL, UEL; winner/runner-up/FA Cup manager/venue). Sign-off artifact MK5LsLn2JKVXsPG6VEEyRS. Next batches: PL champions/runners-up/managers, Golden Boot, PFA, Ballon d'Or, World Cup/Euros/Copa/AFCON gaps, UCL managers (needs source).
- 23 Nov: AUTO-SCHEDULING agreed (user): approve questions ONCE into the bank; db/scheduler.py picks days by rule. Rules: reuse gap FB 56 days, every other game 182 days (6 months); FB mix 15E/4M/1H from No. 36 (easy first); same-day small-pool clash; FB one question per final/tournament a day, no repeated answer, max 2 of the same shape a day; days filled in order, stops and reports when stock runs out. --stock shows shortfall.
- 23 Nov: Finals batch (349) APPROVED and added to the bank as reserve (commit on preview/bank-master). Site files now carry only scheduled questions (reserve stays private). D1 copy needs a reload (?reset=1) after go live; not urgent (only lobbies use D1).
- Stock needed for hands-off scheduling: FB E 840 (have 388), M 224 (426), H 56 (239). Other games 182 each (have 22-34); Shirt Swap 182 per length.
- 23 Nov: Easy gap-fill batch2 (bank/fbgap/batch2_data.py, make_batch2.py -> batch2.json, 192 Qs: 62 E / 111 M / 19 H) on sign-off artifact D1qiSKaF6wTQd9WX94asqS. Generic sign-off builder: bank/fbgap/signoff.py. Ballon d'Or list page wouldn't load (skip until a source works). Easy is the bottleneck for 15/4/1 (needs 840 E in 8 weeks).
- Grading rules (user, 23 Nov): World Cup winners before 1980 = Hard; every World Cup / Euro beaten finalist = Hard; World Cup / Euro hosts = Hard except the most recent (already in bank). PL runners-up questions not wanted. Batch2 now 175 (59 E / 54 M / 62 H).
- 23 Nov: batch3 (bank/fbgap/make_batch3.py -> batch3.json, 256 Qs: 219 E / 20 M / 17 H): 'Which country has X played for?' (time-proof wording) from tiki player sources, fame filter = 2+ appearances in our puzzles or BdO/GB winner; plus 22 missing Ballon d'Or years (topendsports list; 2026 Kane confirmed by ITV/SI). Sign-off artifact Y8WcGuMwM1tK9JiByfssdC. Batch2 (D1qiSKaF6wTQd9WX94asqS) also awaiting approval.
- 23 Nov: Ballon d'Or grading (user): pre-2000 Hard, 2000-2009 Medium, 2010 on Easy (batch3 updated: 216 E). batch4 transfers since 2016 (make_batch4.py -> batch4.json, 57 Qs: 20 E / 27 M / 10 H; 2026 moves news-checked) sign-off PherqwRrXTp76WCiVpDeXs. Pending approval: batch2, batch3, batch4. Easy after all: ~683 of 840.
- 23 Nov: batch5 current internationals (batch5.json, 167 Qs, 71 E) sign-off P5QGViTaq9ETxScjLuGyQE. Captains batch in progress: bank/fbgap/captains_notes.md.
- 23 Nov 10:55: user APPROVED batches 2-5; added to the bank (FB now 1708: E 754/840, M 620, H 334). Seed committed on preview/bank-master (still awaiting "go live": bank as master + reserve). TOMORROW: captains batch (bank/fbgap/captains_notes.md) to close the last 86 Easy; then the scheduler can run Fast Break from No. 36. After go live, owner reloads D1 copy (?reset=1).
- 23 Nov 12:20: BANK SWITCH LIVE (main 9615084). Owner still to reload D1 copy (?reset=1) when convenient.

## 23 Nov: Performance page live (commit 2872ec4)
- tdko.app/performance.html: Stats + Scheduler tabs (#scheduler), stats code TDKO-ST@T5, follows 'tdko-theme' (light default) with its own toggle.
- Built by site-build/make_perf.py from stats.html + scheduler.html (sources); package.py ships performance.html and redirect stubs for stats.html / scheduler.html.
- Scheduler data: db/make_seed.py also writes functions/api/_schedule.js (counts only); GET /api/scheduler is stats-code gated. Re-run make_seed.py before each release so it stays current.
- Orange (draft) only appears once drafts are put in the bank with status 'draft' (export must skip them first).

## 23 Nov evening: bank filled to 31 Dec for single-answer games (preview/dec-singles, awaiting go live)
- Approved + scheduled: wk29 (14-20 Dec) Shirt Swap, Squad Goals, Top Four, Ranked Highly, Offside; new 14-31 Dec WTB (18), Mixer (18), Shirt Swap (33), Offside (11: FWA + CAF removed by user, replaced by Germany 100 caps / Euro Player of the Tournament).
- Sources: bank/dec/*.json (sign-off artifact 9rDEWXT5sHXYtGFf7TJPBw). Loader: db/add_games.py.
- Guards: checks.py fails on unapproved puzzles in the calendar and Shirt Swap answers missing from the guess list (source of truth /home/claude/shirt-swap.html); export.py refuses drafts.
- Still short of 31 Dec: Squad Goals, Top Four, Ranked Highly (to 20 Dec); Link Up Play, Tiki-Taka-Toe, Clean Sweep (to 13 Dec); Cup Run (to 20 Dec).
- Ranked Highly difficulty: user wants level SHOWN; grading table sent (4E/16M/12H), awaiting user's check.

## 23 Nov evening (cont.): bank to 31 Dec + live-stat checks
- Approved and scheduled to 31 Dec: every game except Link Up (18 chains awaiting approval, bank/dec/link.json, built from approved Squad Goals XIs) and Tiki-Taka-Toe (PAUSED from 14 Dec by user: menu pauseFrom + page "Back soon", never wraps to old grids).
- Clean Sweep: FWA removed by user; all-time league scorer lists replaced by StatMuse "last 5 years" top 10s (PL, La Liga, Serie A, UCL; dated to 23 Nov 2026).
- Cup Run: 6 new runs (+ flags FRG, URS, YUG, BUL in /home/claude/cup-run.html); Crystal Palace 2025 retired (promo).
- Squad Goals: 11 new XIs (IPFS Wikipedia mirror line-ups); flags added to /home/claude/who-playedle.html: MEX UKR GEO ECU MAR MKD ROU CRC BIH BUL.
- Fast Break: scheduler filled No. 36-46 (15E/4M/1H).
- LIVE FLAG (user idea): fact_question.live / live_note / checked_on. 19 puzzles flagged. db/livecheck.py lists/marks. make_seed.py writes functions/api/_live.js (calendar from today). Scheduled task "TDKO live-stat check" (trig_01WBScLupkzNWwCzaxJVN2bN) 06:53 daily reads _live.js from GitHub, checks tomorrow's flagged puzzles, push-notifies only when something changed.
- RH difficulty: new chains carry d (e/m/h); showing the level in the game still to build after user confirms grades.
- 23 Nov 19:20 LIVE (commit 70c4b1f): every game to 31 Dec, Tiki paused from 14 Dec, live checklist on GitHub.
- User on Link Up: loves long cross-team chains (Ramos → Dugarry); do more in 2027 but keep players recognisable ("balance is always for players to come back tomorrow").
