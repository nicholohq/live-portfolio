import sqlite3
import json

DB = r"C:\Users\nicholo\.local\share\mimocode\mimocode.db"
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Get detailed parts for the two older sessions
sessions_to_check = [
    ("ses_0d39b6b0effe2ODMWXzMZ0sr6f", "Conversation title request"),
    ("ses_0d39b6bcaffedBkiNjcV8FO8tg", "GitHub INSTALL.md installation"),
]

for sid, title in sessions_to_check:
    print(f"\n{'='*80}")
    print(f"SESSION: {sid} ({title})")
    print(f"{'='*80}")
    
    c.execute("""
        SELECT m.id, m.agent_id, json_extract(m.data, '$.role') as role,
               m.time_created
        FROM message m
        WHERE m.session_id = ?
        ORDER BY m.time_created
    """, (sid,))
    messages = c.fetchall()
    
    for m in messages:
        mid = m[0]
        role = m[2]
        agent = m[1] or 'main'
        
        # Get all parts for this message
        c.execute("""
            SELECT json_extract(data, '$.type') as ptype,
                   json_extract(data, '$.text') as text,
                   json_extract(data, '$.tool') as tool,
                   data
            FROM part
            WHERE message_id = ?
            ORDER BY time_created
        """, (mid,))
        parts = c.fetchall()
        
        for p in parts:
            ptype = p[0]
            if ptype == 'text':
                text = p[1] or ''
                print(f"\n[{role}] {text[:500]}")
            elif ptype == 'tool':
                tool = p[2] or 'unknown'
                pdata = p[3] or ''
                # Extract state output preview
                try:
                    pd = json.loads(pdata)
                    state = pd.get('state', {})
                    output = str(state.get('output', ''))[:400]
                    print(f"\n[tool:{tool}] {output}")
                except:
                    print(f"\n[tool:{tool}] {pdata[:400]}")
            elif ptype == 'step-finish':
                try:
                    pd = json.loads(p[3] or '{}')
                    tokens = pd.get('tokens', {})
                    print(f"\n[step-finish] tokens={tokens}")
                except:
                    pass

conn.close()
