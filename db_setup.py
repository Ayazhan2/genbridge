import os
import sqlite3                                   # built-in Python library for SQLite

# Full path: the database is created next to this file (works on PC and server)
DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "genbridge.db")
conn = sqlite3.connect(DB)                       # open (or create) the database file
cur = conn.cursor()                              # the cursor sends SQL commands

# ---------- 1. Create tables ----------
cur.executescript("""
DROP TABLE IF EXISTS jobs;
CREATE TABLE jobs (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    title   TEXT NOT NULL,
    trend   TEXT NOT NULL,                       -- 'growing' or 'declining'
    rank    INTEGER,                             -- place in the WEF list
    related TEXT                                 -- jobs you can move to
);

CREATE TABLE IF NOT EXISTS mentors (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    email      TEXT NOT NULL,
    field      TEXT NOT NULL,
    years      INTEGER,
    topics     TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS requests (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    mentor_id  INTEGER,
    name       TEXT NOT NULL,
    email      TEXT NOT NULL,
    message    TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mentor_id) REFERENCES mentors(id)
);
""")

# ---------- 2. Jobs from the WEF Future of Jobs Report 2025 ----------
growing = [
    "Big Data Specialist", "FinTech Engineer", "AI and Machine Learning Specialist",
    "Software and Applications Developer", "Security Management Specialist",
    "Data Warehousing Specialist", "Autonomous and Electric Vehicle Specialist",
    "UI and UX Designer", "Delivery Driver", "Internet of Things Specialist",
]
declining = [
    "Postal Service Clerk", "Bank Teller", "Data Entry Clerk", "Cashier",
    "Administrative Assistant", "Printing Worker", "Bookkeeping and Payroll Clerk",
    "Stock-Keeping Clerk", "Transportation Attendant", "Door-to-Door Salesperson",
]
# GenBridge suggestions for "where to move" (our idea, not from the WEF report)
related = {
    "Bank Teller": "FinTech Engineer, Financial Advisor",
    "Data Entry Clerk": "Data Analyst, Big Data Specialist",
    "Cashier": "E-commerce Specialist, Customer Success Manager",
    "Administrative Assistant": "Project Coordinator, Operations Analyst",
    "Postal Service Clerk": "Logistics Coordinator, Delivery Driver",
    "Printing Worker": "UI and UX Designer, Digital Marketing Specialist",
    "Bookkeeping and Payroll Clerk": "FinTech Engineer, Financial Data Analyst",
    "Stock-Keeping Clerk": "Supply Chain Analyst, Logistics Coordinator",
    "Transportation Attendant": "Customer Experience Specialist, Travel Coordinator",
    "Door-to-Door Salesperson": "Digital Marketing Specialist, E-commerce Specialist",
}

for i, title in enumerate(growing, start=1):
    cur.execute("INSERT INTO jobs (title, trend, rank, related) VALUES (?, ?, ?, ?)",
                (title, "growing", i, ""))
for i, title in enumerate(declining, start=1):
    cur.execute("INSERT INTO jobs (title, trend, rank, related) VALUES (?, ?, ?, ?)",
                (title, "declining", i, related.get(title, "")))

conn.commit()
conn.close()
print("Database ready: genbridge.db")
