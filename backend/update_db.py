import sqlite3

db = sqlite3.connect("smartevent.db")
cursor = db.cursor()

# Add role column to users table
try:
    cursor.execute(
        'ALTER TABLE users ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT "USER"'
    )
    print("Added role column to users")
except sqlite3.OperationalError as e:
    print("Users table:", e)

# Add organizer_id column to events table
try:
    cursor.execute(
        "ALTER TABLE events ADD COLUMN organizer_id INTEGER"
    )
    print("Added organizer_id column to events")
except sqlite3.OperationalError as e:
    print("Events organizer_id:", e)

# Add event_status column to events table
try:
    cursor.execute(
        'ALTER TABLE events ADD COLUMN event_status VARCHAR(20) NOT NULL DEFAULT "UPCOMING"'
    )
    print("Added event_status column to events")
except sqlite3.OperationalError as e:
    print("Events event_status:", e)

db.commit()
db.close()

print("Phase 2 database update completed successfully")

