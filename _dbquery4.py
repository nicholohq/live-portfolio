import sqlite3
import json

DB = r"C:\Users\nicholo\.local\share\mimocode\mimocode.db"
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Get Kamp Malaya sessions
print("=== KAMP MALAYA SESSIONS ===")
c.execute("SELECT id, directory, title, time_created FROM session WHERE directory LIKE '%Kamp Malaya%' ORDER BY time_created DESC")
for s in c.fetchall():
    print(f"  id={s[0]}  title={s[2]}  created={s[3]}")

# Get all session directories
print("\n=== ALL UNIQUE DIRECTORIES ===")
c.execute("SELECT DISTINCT directory FROM session")
for r in c.fetchall():
    print(f"  {r[0]}")

# Now check for user statements about rules, decisions, etc. in all sessions
print("\n=== USER STATEMENTS WITH KEYWORDS ===")
keywords = ['always', 'never', 'remember', 'rule', 'decision', 'decided', 'preference', 'prefer']
for kw in keywords:
    c.execute("""
        SELECT m.session_id, substr(json_extract(p.data, '$.text'), 1, 300) as text
        FROM message m
        JOIN part p ON p.message_id = m.id
        WHERE json_extract(m.data, '$.role') = 'user'
          AND json_extract(p.data, '$.type') = 'text'
          AND json_extract(p.data, '$.text') LIKE ?
        LIMIT 5
    """, (f'%{kw}%',))
    rows = c.fetchall()
    if rows:
        print(f"\n  [{kw}]:")
        for r in rows:
            print(f"    session={r[0]}: {r[1][:200]}")

conn.close()
