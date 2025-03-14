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
    median_age: float
    white_pop: int
    black_pop: int
    native_pop: int
    hs_grad: int
    bachelors: int
    labor_force: int
    unemployed: int
    median_income: float
    median_home_value: float
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
    cursor.execute("SELECT name, population, median_age, white_pop, black_pop, native_pop, hs_grad, bachelors, labor_force, unemployed, median_income, median_home_value, state FROM cities WHERE state = ?", (state.upper(),))
    rows = cursor.fetchall()
    conn.close()
    return [{
        "name": row[0], "population": row[1], "median_age": row[2],
        "white_pop": row[3], "black_pop": row[4], "native_pop": row[5],
        "hs_grad": row[6], "bachelors": row[7],
        "labor_force": row[8], "unemployed": row[9],
        "median_income": row[10], "median_home_value": row[11],
        "state": row[12]
    } for row in rows]