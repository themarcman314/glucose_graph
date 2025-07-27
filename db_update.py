from pylibrelinkup import PyLibreLinkUp
from pylibrelinkup.api_url import APIUrl
import creds
from datetime import datetime
import sqlite3
import time

DB_PATH = 'my_db'

def insert_many(db_path, measurements):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.executemany(
        "INSERT OR IGNORE INTO glucose (timestamp, value) VALUES (?, ?)",
        [(m.timestamp.isoformat(), m.value) for m in measurements]
    )
    inserted = conn.total_changes  # number of *actual* changes
    conn.commit()
    conn.close()
    return inserted

def ensure_table_exists(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS glucose (
            timestamp TEXT PRIMARY KEY,
            value REAL
        )
    """)
    conn.commit()
    conn.close()


def main():
    client = PyLibreLinkUp(email=creds.email, password=creds.key, api_url=APIUrl.FR)
    client.authenticate()
    patient_list = client.get_patients()
    patient = patient_list[0] # get the first patient (me)
    ensure_table_exists(DB_PATH)

    # get data for graph from server
    while True:
        try:
            measurements = client.graph(patient_identifier=patient)
            inserted_count = insert_many(DB_PATH, measurements)  # uses INSERT OR IGNORE
            print(f"Inserted {inserted_count} values at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print("Error:", e)
        time.sleep(600)

if __name__ == "__main__":
    main()
