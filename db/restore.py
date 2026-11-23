"""Rebuilds db/tdko.db from the copy saved in the site repo (functions/api/bank/_seed.js), e.g. on a fresh machine."""
import json, sqlite3, os, re, sys
SEED='/home/claude/tdko-site/functions/api/bank/_seed.js'; DB='/home/claude/db/tdko.db'
if os.path.exists(DB) and '--force' not in sys.argv: sys.exit('tdko.db exists; use --force to replace it from the saved copy')
t=open(SEED).read()
schema=json.loads(re.search(r'export const SCHEMA = (.*?);\n',t,re.S).group(1)); rows=json.loads(re.search(r'export const ROWS = (.*?);\n',t,re.S).group(1))
if os.path.exists(DB): os.remove(DB)
c=sqlite3.connect(DB); [c.execute(s) for s in schema]; [c.execute(r) for r in rows]; c.commit()
print('restored', c.execute('SELECT COUNT(*) FROM fact_question').fetchone()[0], 'questions')
