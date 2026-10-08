import sqlite3

db = sqlite3.connect("smartevent.db")

db.execute(
    "UPDATE users SET role = ? WHERE email = ?",
    ("ORGANIZER", "varshini_test@example.com")
)

db.commit()
db.close()

print("User role changed to ORGANIZER")