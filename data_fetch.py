# data_fetch.py (temporary script for data collection)
import requests
import pandas as pd

# Census API endpoint for 2017-2021 ACS 5-year Estimates
BASE_URL = "https://api.census.gov/data/2021/acs/acs5"

# Fetch city data for Washington and California
def fetch_city_data(state_code):
    params = {
        "get":(
            "NAME,"  # City name
            "B01003_001E,"  # Total Population
            "B01002_001E,"  # Median Age (Age Distribution)
            "B02001_002E,B02001_003E,B02001_004E,"  # Racial Composition (White, Black, Native American)
            "B15003_017E,B15003_022E,"  # Educational Attainment (HS grad, Bachelor's)
            "B23025_002E,B23025_005E,"  # Employment Status (In labor force, Unemployed)
            "B19013_001E,"  # Median Household Income
            "B25077_001E"   # Median Home Value
        ),  
        "for": "place:*",                       # All cities
        "in": f"state:{state_code}"             # State code (53=WA, 06=CA)
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        print(f"Error fetching data for state {state_code}: {response.text}")
        return pd.DataFrame() 
    data = response.json()
    
    # Convert to DataFrame, skip header row
    df = pd.DataFrame(data[1:], columns=[
        "name",
        "population",
        "median_age",
        "white_pop", "black_pop", "native_pop",  # Racial composition
        "hs_grad", "bachelors",                  # Educational attainment
        "labor_force", "unemployed",             # Employment status
        "median_income",
        "median_home_value",
        "state",
        "place"                        
    ])
    return df

# Save data to CSV
wa_cities = fetch_city_data("53")
ca_cities = fetch_city_data("06")
all_cities = pd.concat([wa_cities, ca_cities])
all_cities.to_csv("data/cities_raw.csv", index=False)

print("Data fetched and saved to data/cities_raw.csv")