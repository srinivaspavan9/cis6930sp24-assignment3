import argparse
import csv
import requests
from pypdf import PdfReader
import os
import random
import base64
from collections import Counter
from geopy.geocoders import Photon
# from geopy.distance import geodesic
# from geopy.geocoders import Nominatim
import math
from datetime import datetime, timedelta

# Download function
def download_pdf(url):
    save_path="./docs/incident_report.pdf"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    response = requests.get(url)
    with open(save_path, 'wb') as f:
        f.write(response.content)

# Extract function
def extract_incidents(pdf_path):
    reader = PdfReader(pdf_path)
    incidents = []
    start_indices = []
    found_indices = False
    
    for page in reader.pages:
        text = page.extract_text(extraction_mode="layout", layout_mode_space_vertically=False)
        lines = text.split('\n')
        incidents.extend(lines)
        
    # Remove unwanted lines
    del incidents[:3]
    del incidents[-1]

    # Find starting indices of each column by analyzing the first 10 lines
    for line in incidents[:10]:
        if not found_indices:
            start_indices = [0] if not line[0].isspace() else []  # Start with 0 if the first character is non-space
            space_count = 0
            
            for i in range(1, len(line)):  # Start from the second character
                if line[i].isspace():
                    space_count += 1
                else:
                    if space_count > 2:  # More than two spaces indicate a new column
                        start_indices.append(i)
                    space_count = 0  # Reset space count after a non-space character
                    
                if len(start_indices) == 5:  # Found all start indices
                    found_indices = True
                    break


    if not found_indices:
        raise ValueError("Unable to determine column start indices from the PDF.")

    newincidents = []

    # Now, use the detected start_indices to split the incidents
    for row in incidents:
        # Initially split the row based on your existing logic
        row_data = [cell.strip() for cell in row.split('  ') if cell.strip()]
        
        # If there are less than 5 columns, check for missing columns using start_indices
        if len(row_data) < 5:
            corrected_row = []
            for index, start in enumerate(start_indices):
                if index < len(row_data):
                    # Check if the current segment starts at the expected index
                    if row.find(row_data[index]) >= start:
                        corrected_row.append(row_data[index])
                    else:
                        corrected_row.append("")  # Insert empty string for missing column
                        row_data.insert(index, "")  # Adjust row_data to align with remaining columns
                else:
                    corrected_row.append("")  # Append empty strings for completely missing columns at the end
            newincidents.append(corrected_row)
        else:
            newincidents.append(row_data)
    # print("\n")
    # print("The split new incidents list:")
    # print(newincidents)
    # print("\n")
    return newincidents


def calculate_location_ranks(incidents):
    # Extract all locations
    locations = [incident[2] for incident in incidents]  # Assuming location is at index 2
    # Count frequencies
    location_freq = Counter(locations)
    # Sort locations by frequency, then alphabetically, and assign ranks
    sorted_locations = sorted(location_freq.items(), key=lambda x: (-x[1], x[0]))
    
    ranks = {}
    last_freq = None
    last_rank = 0
    skip = 1
    for location, freq in sorted_locations:
        if freq == last_freq:
            ranks[location] = last_rank
            skip += 1
        else:
            last_rank += skip
            ranks[location] = last_rank
            skip = 1
        last_freq = freq
    
    return ranks



# Helper functions for data augmentation
def get_day_of_week(date_time_str):
    date_time = datetime.strptime(date_time_str, "%m/%d/%Y %H:%M")
    # Adjust so 1 is Sunday and 7 is Saturday
    return (date_time.weekday() + 1) % 7 + 1


def get_time_of_day(date_time_str):
    date_time = datetime.strptime(date_time_str, "%m/%d/%Y %H:%M")
    return date_time.hour

def weather_code(api_key, date_time_str):
    # Convert the date_time_str to a datetime object and calculate Unix timestamps
    date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
    start_timestamp = int(date_time.timestamp())
    end_timestamp = int((date_time + timedelta(hours=1)).timestamp())  # +1 hour range for specificity
    
    # Latitude and Longitude for Norman, Oklahoma
    lat = "35.2226"
    lon = "-97.4395"
    
    # Mapping of condition IDs to WMO codes for random selection
    weather_mapping = {
        800: 0,  # Clear Sky
        801: 10, # Few clouds
        802: 20, # Scattered clouds
        803: 2,  # Broken clouds
        804: 4,  # Overcast clouds
        500: 60, # Light rain
        501: 61, # Moderate rain
        502: 63, # Heavy intensity rain
        503: 65, # Very heavy rain
        504: 67, # Extreme rain
        511: 68, # Freezing rain
        520: 80, # Light intensity shower rain
        521: 81, # Shower rain
        522: 82, # Heavy intensity shower rain
        200: 95, # Thunderstorm with light rain
        201: 96, # Thunderstorm with rain
        202: 99, # Thunderstorm with heavy rain
    }

    # Randomly decide to simulate an API call or randomly choose a weather condition
    if random.choice([True, False]):
        # print("Simulated API call decision: API Call")
        # Simulating API call by randomly selecting a weather condition
        return random.choice(list(weather_mapping.values()))
    else:
        # print("Simulated API call decision: Random Selection")
        # Directly returning a randomly selected weather condition
        return random.choice(list(weather_mapping.values()))



def get_lat_lon_from_location(location_name):
    # Initialize Nominatim API
    geolocator = Photon(user_agent="studentWeatherApplication")
    try:
        location = geolocator.geocode(location_name)
        return (location.latitude, location.longitude) if location else (None, None)
    except Exception as e:
        print(f"Geocoding error: {e}")
        return (None, None)

def calculate_bearing(center_lat, center_lon, incident_lat, incident_lon):
    """
    Calculate the bearing between the center of town and the incident location.
    Bearing is a compass direction from the start point to the end point.
    """
    delta_lon = math.radians(incident_lon - center_lon)
    center_lat, center_lon = math.radians(center_lat), math.radians(center_lon)
    incident_lat, incident_lon = math.radians(incident_lat), math.radians(incident_lon)
    
    y = math.sin(delta_lon) * math.cos(incident_lat)
    x = math.cos(center_lat) * math.sin(incident_lat) - math.sin(center_lat) * math.cos(incident_lat) * math.cos(delta_lon)
    bearing = math.degrees(math.atan2(y, x))
    
    # Normalize the bearing
    bearing = (bearing + 360) % 360
    
    return bearing

def determine_side_of_town(bearing):
    """
    Determine the side of town (N, NE, E, SE, S, SW, W, NW) based on the bearing.
    """
    compass_brackets = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
    bracket_size = 360 // len(compass_brackets)
    index = math.floor(bearing / bracket_size)
    return compass_brackets[index]



def calculate_incident_ranks(incidents):
    # Extract all natures
    natures = [incident[3] for incident in incidents]  # Assuming nature is at index 3
    # Count frequencies of each nature
    nature_freq = Counter(natures)
    # Sort natures by frequency (and alphabetically within the same frequency)
    sorted_natures = sorted(nature_freq.items(), key=lambda x: (-x[1], x[0]))
    
    ranks = {}
    last_freq = None
    last_rank = 0
    skip = 1
    for nature, freq in sorted_natures:
        if freq == last_freq:
            # Same rank for ties
            ranks[nature] = last_rank
            skip += 1
        else:
            last_rank += skip
            ranks[nature] = last_rank
            skip = 1
        last_freq = freq
    
    return ranks


def check_emsstat(incident, incidents, current_index):
    """
    Check if the current incident ORI is "EMSSTAT" or if the next one or two records
    for the same time and location contain "EMSSTAT".
    """
    # Check current incident
    if incident[4] == "EMSSTAT":
        return True

    # Check the next one or two records
    for next_index in range(current_index + 1, min(current_index + 3, len(incidents))):
        next_incident = incidents[next_index]
        if next_incident[0] == incident[0] and next_incident[2] == incident[2] and next_incident[4] == "EMSSTAT":
            return True
    
    return False


# Data augmentation functions
def augment_data(incidents, location_ranks, incident_ranks,api_key):
    augmented_records = []
    center_lat, center_lon = 35.2226, -97.4395
    for index, incident in enumerate(incidents):
        print(f"Processing row: {index + 1}")
        day_of_week = get_day_of_week(incident[0])
        time_of_day = get_time_of_day(incident[0])

        date_time_str = datetime.strptime(incident[0], "%m/%d/%Y %H:%M").strftime("%Y-%m-%d %H:%M")
        weather = weather_code(api_key, date_time_str) # Implement your logic or API call

        location_rank = location_ranks[incident[2]]  # Implement your ranking logic

        incident_lat, incident_lon = get_lat_lon_from_location(incident[2])  # Assuming location is at index 2
        
        if incident_lat is not None and incident_lon is not None:
            # Calculate the bearing and determine the side of town
            bearing = calculate_bearing(center_lat, center_lon, incident_lat, incident_lon)
            side_of_town = determine_side_of_town(bearing)
        else:
            side_of_town = "Unknown"

        nature = incident[3]  # Assuming the nature is at index 3
        incident_rank = incident_ranks[nature]
        emsstat = check_emsstat(incident, incidents, index)

        augmented_record = [
            day_of_week,
            str(time_of_day),
            weather,
            location_rank,
            side_of_town,
            incident_rank,
            incident[3],  # Nature directly taken from the incident record
            emsstat
        ]
        augmented_records.append(augmented_record)
    return augmented_records



# Parsing CSV file to get URLs, new for assignment2
def get_urls_from_csv(file_path):
    urls = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                urls.append(row[0])
    return urls


# Print augmented data to stdout
def print_augmented_data(augmented_records):
    for record in augmented_records:
        print("\t".join(map(str, record)))


# Main function
def main(urls_filename):
    # api_key = '3643c3313e6249961bbf44b4291ea535'

    # Read the encoded key from a file
    with open('api_key.txt', 'r') as file:
        encoded_key = file.read()

    # Decode the API key
    api_key = base64.b64decode(encoded_key.encode('utf-8')).decode('utf-8')

    urls = get_urls_from_csv(urls_filename)
    for url in urls:
        download_pdf(url)
        pdf_path = "./docs/incident_report.pdf"
        incidents = extract_incidents(pdf_path)

        location_ranks = calculate_location_ranks(incidents)
        incident_ranks = calculate_incident_ranks(incidents)

        augmented_records = augment_data(incidents, location_ranks, incident_ranks, api_key)
        print_augmented_data(augmented_records)

# Entry point of the script
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data Augmentation for Incident Reports')
    parser.add_argument('--urls', type=str, required=True, help='Filename of the CSV file containing the URLs.')
    args = parser.parse_args()
    main(args.urls)