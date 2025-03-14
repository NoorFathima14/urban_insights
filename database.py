# database.py
import sqlite3
import pandas as pd
import numpy as np

def init_db():
    """Initialize SQLite database and create cities table."""
    conn = sqlite3.connect("demographics.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            population INTEGER,
            median_age REAL,
            white_pop INTEGER,
            black_pop INTEGER,
            native_pop INTEGER,
            hs_grad INTEGER,
            bachelors INTEGER,
            labor_force INTEGER,
            unemployed INTEGER,
            median_income REAL,
            median_home_value REAL,
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
    
    numeric_cols = ["population", "white_pop", "black_pop", "native_pop", 
                    "hs_grad", "bachelors", "labor_force", "unemployed"]
    for col in numeric_cols:
        df[col] = df[col].fillna(0).astype(int)
    
    for col in ["median_age", "median_income", "median_home_value"]:
        # Replace -666666666 (string or int) with NaN
        df[col] = df[col].replace(["-666666666", -666666666], np.nan)
        # Calculate mean of non-NaN values
        valid_mean = df[col].dropna().astype(float).mean()
        # Fill NaN with the valid mean
        df[col] = df[col].fillna(valid_mean).astype(float)
        print(f"{col} mean (excluding -666666666): {valid_mean}")
    df["state"] = df["state"].astype(str).map({"53": "WA", "06": "CA"}).fillna("Unknown")

    # Connect to database
    conn = sqlite3.connect("demographics.db")
    df.to_sql("cities", conn, if_exists="replace", index=False)  # Overwrite for simplicity
    conn.close()

def get_cities():
    """Retrieve all cities from the database."""
    conn = sqlite3.connect("demographics.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, population, median_age, white_pop, black_pop, native_pop, hs_grad, bachelors, labor_force, unemployed, median_income, median_home_value, state FROM cities")
    rows = cursor.fetchall()
    conn.close()
    
    transformed_data = []
    for row in rows:
        population = row[1] or 1  # Avoid division by zero
        labor_force = row[8] or 1  # Avoid division by zero
        data = {
            "name": row[0],
            "population": row[1],
            "median_age": row[2],
            "white_pop_pct": round((row[3] / population) * 100,2) if row[3] else 0,
            "black_pop_pct": round((row[4] / population) * 100,2) if row[4] else 0,
            "native_pop_pct": round((row[5] / population) * 100,2) if row[5] else 0,
            "hs_grad_pct": round((row[6] / population) * 100,2) if row[6] else 0,
            "bachelors_pct": round((row[7] / population) * 100,2) if row[7] else 0,
            "unemployment_rate": round((row[9] / labor_force) * 100,2) if row[9] else 0,
            "median_income": row[10],
            "median_home_value": row[11],
            "state": row[12]
        }
        transformed_data.append(data)
    return transformed_data

if __name__ == "__main__":
    init_db()
    load_and_clean_data()
    print("Database initialized and data loaded.")
    print(get_cities()[:2])