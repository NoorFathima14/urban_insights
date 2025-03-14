# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from database import get_cities  # Import from our module
import sqlite3

app = FastAPI()

# Pydantic model for response validation
class CityData(BaseModel):
    name: str
    population: int
    median_income: float
    state: str

@app.get("/cities", response_model=List[CityData])
async def read_cities():
    """Fetch all city demographic data from the database."""
    return get_cities()

@app.get("/cities/{state}")
async def read_cities_by_state(state: str):
    """Fetch cities filtered by state (WA or CA)."""
    conn = sqlite3.connect("demographics.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, population, median_income, state FROM cities WHERE state = ?", (state.upper(),))
    rows = cursor.fetchall()
    conn.close()
    return [{"name": row[0], "population": row[1], "median_income": row[2], "state": row[3]} for row in rows]