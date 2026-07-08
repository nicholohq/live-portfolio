import sqlite3
import json

DB = r"C:\Users\nicholo\.local\share\mimocode\mimocode.db"
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Get Kamp Malaya sessions with user text content
sessions = [
    ("ses_0d3a12431ffekoDC3NpCgUL330", "GHL integration fix"),
    ("ses_0d3a125b3ffeewGszwSU8FO2rE", "Context usage"),
    ("ses_0d3a11f66ffe206Fg2oNUW0nrA", "Claude Code session"),
]

for sid, title in sessions:
    print(f"\n{'='*80}")
    print(f"SESSION: {sid} ({title})")
    print(f"{'='*80}")
    
    c.execute("""
        SELECT m.id, json_extract(m.data, '$.role') as role,
               json_extract(p.data, '$.type') as ptype,
               json_extract(p.data, '$.text') as text,
               p.data
        FROM message m
        JOIN part p ON p.message_id = m.id
        WHERE m.session_id = ?
        ORDER BY m.time_created, p.time_created
    """, (sid,))
    rows = c.fetchall()
    
    for r in rows:
        role = r[1]
        ptype = r[2]
        if ptype == 'text' and r[3]:
            text = r[3]
            if role == 'user':
                print(f"\n[USER]: {text[:600]}")
            else:
                print(f"\n[ASSISTANT]: {text[:400]}")

# Also check home directory sessions for user rules/preferences
print(f"\n{'='*80}")
print("HOME DIRECTORY SESSIONS (user rules/preferences)")
print(f"{'='*80}")

c.execute("SELECT id, title FROM session WHERE directory = 'C:\\Users\\nicholo' ORDER BY time_created DESC")
for s in c.fetchall():
    print(f"\n  [{s[0]}] {s[1]}")

conn.close()
