import pandas as pd
import re
from geopy.point import Point

# Helper function to parse DMS to decimal
def dms_to_decimal(coord):
    try:
        point = Point(coord)
        return point.latitude, point.longitude
    except ValueError:
        return None, None

# Load your data (assuming a CSV file named 'data.csv')
df = pd.read_csv('data.csv')

# Create empty columns for latitude and longitude
df['Latitud'] = None
df['Longitud'] = None

# Updated regex pattern
coordinate_pattern = re.compile(r"""
    (?:(\d+°\d+'(?:\d+(?:\.\d+)?)?\"?[NnSsEeWw]))   # Matches DMS format for lat/lon
    [\s,]+                                          # Separator (space or comma)
    (?:(\d+°\d+'(?:\d+(?:\.\d+)?)?\"?[NnSsEeWw]))   # Matches the other DMS coordinate
    |                                               # OR
    (\d+\.\d+)[\s,]+(-?\d+\.\d+)                    # Matches decimal lat/lon (space or comma separated)
""", re.VERBOSE)

# Process each row
for i, coord in enumerate(df['Coordenadas']):
    if pd.isna(coord):
        continue  # Skip empty rows
    
    # Find all matches for coordinates
    match = coordinate_pattern.search(coord)
    
    if match:
        if match.group(1) and match.group(2):  # DMS pair
            lat_dms, lon_dms = match.group(1), match.group(2)
            lat, lon = dms_to_decimal(f"{lat_dms}, {lon_dms}")
            if lat is not None and lon is not None:
                df.loc[i, 'Latitud'] = lat
                df.loc[i, 'Longitud'] = lon
            else:
                print(f"Error parsing DMS format: {coord}")
        elif match.group(3) and match.group(4):  # Decimal pair
            try:
                lat, lon = float(match.group(3)), float(match.group(4))
                df.loc[i, 'Latitud'] = lat
                df.loc[i, 'Longitud'] = lon
            except ValueError:
                print(f"Error parsing decimal format: {coord}")
        else:
            print(f"Unmatched format: {coord}")
    else:
        print(f"No match for: {coord}")

# Save the results to a new CSV file
df.to_csv('coordinates1.csv', index=False)
