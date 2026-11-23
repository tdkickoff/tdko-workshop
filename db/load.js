// One-off loader for the question bank (D1 binding BANK).
// GET /api/bank/load?key=<BANK_ADMIN_KEY>  -> creates the tables if missing, adds any rows not already there, returns row counts.
// Safe to run again: every statement is CREATE ... IF NOT EXISTS or INSERT OR IGNORE. Without the right key it does nothing.
import { SCHEMA, ROWS } from './_seed.js';

const json = (data, status = 200) =>
  new Response(JSON.stringify(data, null, 1), { status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } });

function same(a, b) {   // compare without leaking timing
  if (typeof a !== 'string' || typeof b !== 'string' || a.length !== b.length) return false;
  let d = 0; for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i); return d === 0;
}

export async function onRequestGet({ request, env }) {
  if (!env.BANK || !env.BANK_ADMIN_KEY) return json({ error: 'The bank is not connected yet: add the BANK binding and the BANK_ADMIN_KEY secret, then redeploy.' }, 503);
  const key = new URL(request.url).searchParams.get('key') || '';
  if (!same(key, env.BANK_ADMIN_KEY)) return json({ error: 'Wrong or missing key.' }, 403);
  const db = env.BANK;
  await db.batch(SCHEMA.map(s => db.prepare(s)));
  const per = 400; let written = 0;
  for (let i = 0; i < ROWS.length; i += per) {
    const res = await db.batch(ROWS.slice(i, i + per).map(s => db.prepare(s)));
    for (const r of res) written += (r.meta && r.meta.changes) || 0;
  }
  const tables = ['fact_question', 'fact_answer', 'fact_schedule', 'dim_player', 'dim_club', 'dim_nation', 'dim_competition', 'dim_season'];
  const counts = {};
  const res = await db.batch(tables.map(t => db.prepare(`SELECT COUNT(*) AS n FROM ${t}`)));
  tables.forEach((t, i) => { counts[t] = res[i].results[0].n; });
  return json({ ok: true, rows_added_now: written, counts });
}
