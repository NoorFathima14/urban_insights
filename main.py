# main.py
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from database import get_cities
import sqlite3
from fastapi.staticfiles import StaticFiles

logging.basicConfig(level=logging.INFO, force=True)
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic model for response validation
class CityData(BaseModel):
    name: str
    population: int
    median_age: float
    white_pop_pct: float
    black_pop_pct: float
    native_pop_pct: float
    hs_grad_pct: float
    bachelors_pct: float
    unemployment_rate: float
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
    transformed_data = []
    for row in rows:
        population = row[1] or 1
        labor_force = row[8] or 1
        data = {
            "name": row[0], "population": row[1], "median_age": row[2],
            "white_pop_pct": (row[3] / population) * 100 if row[3] else 0,
            "black_pop_pct": (row[4] / population) * 100 if row[4] else 0,
            "native_pop_pct": (row[5] / population) * 100 if row[5] else 0,
            "hs_grad_pct": (row[6] / population) * 100 if row[6] else 0,
            "bachelors_pct": (row[7] / population) * 100 if row[7] else 0,
            "unemployment_rate": (row[9] / labor_force) * 100 if row[9] else 0,
            "median_income": row[10], "median_home_value": row[11],
            "state": row[12]
        }
        transformed_data.append(data)
    return transformed_data

class WhitePopData(BaseModel):
    name: str
    white_pop: int

@app.get("/whitepop", response_model=List[WhitePopData])
async def get_whitepop_30():
    logger.info("Entering get_whitepop_30 endpoint")
    conn = sqlite3.connect("/Users/noorfathima/Documents/college/project/urban_insights/demographics.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, white_pop FROM cities WHERE white_pop > 30")
    rows = cursor.fetchall()
    logger.info("Rows fetched: %s", rows[:5])  # Log first 5 for brevity
    conn.close()
    return [{"name": row[0], "white_pop": row[1]} for row in rows]