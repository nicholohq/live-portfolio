import sqlite3
import json

DB = r"C:\Users\nicholo\.local\share\mimocode\mimocode.db"
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# List tables
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in c.fetchall()]
print("TABLES:", tables)

# List sessions
print("\n=== SESSIONS ===")
c.execute("SELECT id, directory, title, time_created FROM session ORDER BY time_created DESC")
for r in c.fetchall():
    print(f"  id={r[0]}  dir={r[1]}  title={r[2]}  created={r[3]}")

# Count messages per session
print("\n=== MESSAGE COUNTS ===")
c.execute("""
    SELECT session_id, COUNT(*) as msg_count
    FROM message
    GROUP BY session_id
    ORDER BY msg_count DESC
""")
for r in c.fetchall():
    print(f"  session={r[0]}  messages={r[1]}")

# List actor_registry entries
print("\n=== ACTOR REGISTRY ===")
try:
    c.execute("SELECT id, name, type FROM actor_registry")
    for r in c.fetchall():
        print(f"  id={r[0]}  name={r[1]}  type={r[2]}")
except Exception as e:
    print(f"  (no actor_registry table: {e})")

conn.close()
