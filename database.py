# database.py
import sqlite3
import pandas as pd

def init_db():
    """Initialize SQLite database and create cities table."""
    conn = sqlite3.connect("demographics.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            population INTEGER,
            median_income REAL,
            state TEXT,
            place_code TEXT
        )
    """)
    conn.commit()
    conn.close()

def load_and_clean_data():
    """Load raw data, clean it, and insert into database."""
    # Load CSV
    df = pd.read_csv("data/cities_raw.csv")
    
    # Clean: Handle missing values and type conversion
    df["population"] = df["population"].fillna(0).astype(int)
    df["median_income"] = df["median_income"].replace("-666666666", None).fillna(df["median_income"].mean()).astype(float)
    df["state"] = df["state"].astype(str).map({"53": "WA", "06": "CA"}).fillna("Unknown")
    
    # Connect to database
    conn = sqlite3.connect("demographics.db")
    df.to_sql("cities", conn, if_exists="replace", index=False)  # Overwrite for simplicity
    conn.close()

def get_cities():
    """Retrieve all cities from the database."""
    conn = sqlite3.connect("demographics.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, population, median_income, state FROM cities")
    rows = cursor.fetchall()
    conn.close()
    return [{"name": row[0], "population": row[1], "median_income": row[2], "state": row[3]} for row in rows]

if __name__ == "__main__":
    init_db()
    load_and_clean_data()
    print("Database initialized and data loaded.")