import pandas as pd
import re

def parse_coordinates(coordinate):
    # Standardize the coordinate string
    coordinate = re.sub(r'[´’]', "'", coordinate)  # Replace special apostrophes
    coordinate = re.sub(r'[“”]', '"', coordinate)  # Replace special quotes
    coordinate = re.sub(r'\*', '°', coordinate)    # Replace asterisks with degrees
    coordinate = re.sub(r'/', ' ', coordinate)     # Replace slashes with spaces
    coordinate = re.sub(r'\s+', ' ', coordinate.strip())  # Normalize spaces
    coordinate = coordinate.replace("O", "W")  # Replace "O" with "W" for longitude
    

    # Handle potential missing hemisphere indicators
    if not re.search(r'[NS]', coordinate, re.IGNORECASE):
        coordinate = 'N ' + coordinate
    if not re.search(r'[EW]', coordinate, re.IGNORECASE):
        coordinate = coordinate + ' W'

    # Regex to handle latitude and longitude, including large seconds (e.g., 990")
    match = re.match(
        r'[NSns]?\s*(?P<lat_deg>\d+)[°*]\s*(?P<lat_min>\d+)[\'’]?\s*(?P<lat_sec>\d+(\.\d+)?)"?\s*[NSns]?\s+'
        r'[WEwe]?\s*(?P<lon_deg>\d+)[°*]\s*(?P<lon_min>\d+)[\'’]?\s*(?P<lon_sec>\d+(\.\d+)?)"?\s*[WEwe]?',
        coordinate
    )
    
    if not match:
        return None, None  # Return None if the format is not matched
    
    # Extract latitude and longitude components
    lat_deg = int(match.group('lat_deg'))
    lat_min = int(match.group('lat_min'))
    lat_sec = float(match.group('lat_sec'))  # Handle decimals for seconds

    lon_deg = int(match.group('lon_deg'))
    lon_min = int(match.group('lon_min'))
    lon_sec = float(match.group('lon_sec'))  # Handle decimals for seconds

    # Normalize seconds if they exceed 60
    lat_min += int(lat_sec // 60)
    lat_sec = lat_sec % 60
    lon_min += int(lon_sec // 60)
    lon_sec = lon_sec % 60

    lat_deg += int(lat_min // 60)
    lat_min = lat_min % 60
    lon_deg += int(lon_min // 60)
    lon_min = lon_min % 60

    # Convert to decimal degrees
    latitude = lat_deg + lat_min / 60 + lat_sec / 3600
    longitude = lon_deg + lon_min / 60 + lon_sec / 3600

    # Adjust for hemisphere
    if 'S' in coordinate.upper():
        latitude = -latitude
    if 'W' in coordinate.upper():
        longitude = -longitude

    return latitude, longitude

# Load the CSV
file_path = "data.csv"  # Update with your file's path
df = pd.read_csv(file_path)

# Create new columns for latitude and longitude
df['Latitud'], df['Longitud'] = zip(*df.iloc[:, 0].apply(parse_coordinates))

# Save the cleaned data to a new CSV
output_path = "cleaned_data.csv"
df.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f"Processed data saved to {output_path}")