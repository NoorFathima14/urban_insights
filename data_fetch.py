# data_fetch.py (temporary script for data collection)
import requests
import pandas as pd

# Census API endpoint for 2017-2021 ACS 5-year Estimates
BASE_URL = "https://api.census.gov/data/2021/acs/acs5"

# Fetch city data for Washington and California
def fetch_city_data(state_code):
    params = {
        "get": "NAME,B01003_001E,B19013_001E",  # Name, Population, Median Income
        "for": "place:*",                       # All cities
        "in": f"state:{state_code}"             # State code (53=WA, 06=CA)
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    # Convert to DataFrame, skip header row
    df = pd.DataFrame(data[1:], columns=["name", "population", "median_income", "state", "place"])
    return df

# Save data to CSV
wa_cities = fetch_city_data("53")
ca_cities = fetch_city_data("06")
all_cities = pd.concat([wa_cities, ca_cities])
all_cities.to_csv("data/cities_raw.csv", index=False)

print("Data fetched and saved to data/cities_raw.csv")