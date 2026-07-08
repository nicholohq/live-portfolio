import sqlite3
import json

DB = r"C:\Users\nicholo\.local\share\mimocode\mimocode.db"
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Focus on current project sessions
PROJECT_DIR = r"C:\Users\nicholo\Documents\Clients\Portfolio"

# Get sessions for this project
c.execute("SELECT id, directory, title, time_created FROM session WHERE directory=? ORDER BY time_created DESC", (PROJECT_DIR,))
sessions = c.fetchall()
print("=== PROJECT SESSIONS ===")
for s in sessions:
    print(f"  id={s[0]}  title={s[2]}  created={s[3]}")

# Now get all messages for each session with role info
for s in sessions:
    sid = s[0]
    print(f"\n=== SESSION {sid} ({s[2]}) ===")
    c.execute("""
        SELECT m.id, m.agent_id, json_extract(m.data, '$.role') as role,
               m.time_created, m.data
        FROM message m
        WHERE m.session_id = ?
        ORDER BY m.time_created
    """, (sid,))
    for m in c.fetchall():
        role = m[2]
        agent = m[1] or 'main'
        # Get first part preview
        c.execute("""
            SELECT json_extract(data, '$.type') as ptype, data
            FROM part
            WHERE message_id = ?
            ORDER BY time_created
            LIMIT 1
        """, (m[0],))
        part = c.fetchone()
        preview = ""
        if part:
            pdata = part[1][:300] if part[1] else ""
            preview = f"  [{part[0]}] {pdata}"
        print(f"  msg={m[0]} agent={agent} role={role} time={m[3]}{preview}")

conn.close()
