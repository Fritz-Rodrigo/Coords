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

# Define a regex pattern to match the first coordinate pair
coordinate_pattern = re.compile(r"(\d+°\d+'(?:\d+(?:\.\d+)?)?\"?[NnSsLl]?\s?\d+°?\d*'?\d*(?:\.\d+)?\"?[EeOoWwLl]?|\d+\.\d+[,]\s?-?\d+\.\d+)")

# Process each row
for i, coord in enumerate(df['Coordenadas']):
    # Find all matches for coordinates
    matches = coordinate_pattern.findall(coord)
    
    if matches:
        first_coord = matches[0].strip()  # Take the first match
        
        if ',' in first_coord:  # Decimal format
            lat, lon = map(str.strip, first_coord.split(','))
            df.loc[i, 'Latitud'] = float(lat)
            df.loc[i, 'Longitud'] = float(lon)
        else:  # DMS format
            lat, lon = dms_to_decimal(first_coord)
            df.loc[i, 'Latitud'] = lat
            df.loc[i, 'Longitud'] = lon

# Save the results to a new CSV file
df.to_csv('coordinates.csv', index=False)

print("Coordinates processed and saved to 'coordinates.csv'")