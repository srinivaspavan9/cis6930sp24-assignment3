import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
import time  # Import time for artificial delays

# Append the directory of your script to Python's search path
sys.path.append(os.path.abspath('.'))

# Importing your functions from assignment2.py
from assignment2 import download_pdf, extract_incidents, calculate_location_ranks, calculate_incident_ranks, augment_data, get_urls_from_csv

def process_data(urls_filename, progress_bar):
    urls = get_urls_from_csv(urls_filename)
    all_augmented_records = []
    total_urls = len(urls)
    print("Total URLs to process:", total_urls)  # Debugging output
    for index, url in enumerate(urls):
        print(f"Processing URL {index + 1}/{total_urls}: {url}")  # Debugging output
        download_pdf(url)
        pdf_path = "./docs/incident_report.pdf"
        incidents = extract_incidents(pdf_path)
        location_ranks = calculate_location_ranks(incidents)
        incident_ranks = calculate_incident_ranks(incidents)
        api_key = 'Your_API_Key'  # Replace with your actual API key
        augmented_records = augment_data(incidents, location_ranks, incident_ranks, api_key)
        all_augmented_records.extend(augmented_records)
        progress_percent = (index + 1) / total_urls
        progress_bar.progress(progress_percent)
        time.sleep(1)  # Artificial delay for testing progress bar
    return all_augmented_records

def display_data(df):
    st.write(df)
    
    # Visualization for 'Day of the Week'
    st.subheader("Crime Rates by Day of the Week")
    day_counts = df['Day of the Week'].value_counts().sort_index()
    fig, ax = plt.subplots()
    ax.pie(day_counts, labels=day_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)

    # Visualization for 'Time of Day'
    st.subheader("Incidents by Time of Day")
    time_counts = df['Time of Day'].value_counts().sort_index()
    st.line_chart(time_counts)

    # Visualization for 'Weather'
    st.subheader("Incidents by Weather Conditions")
    weather_counts = df['Weather'].value_counts().sort_index()
    st.bar_chart(weather_counts)

    # Visualization for 'Location Rank'
    st.subheader("Incidents by Location Rank")
    location_counts = df['Location Rank'].value_counts().sort_index()
    st.bar_chart(location_counts)

    # Visualization for 'Side of Town'
    st.subheader("Incidents by Side of Town")
    side_counts = df['Side of Town'].value_counts()
    plt.figure(figsize=(10, 4))
    sns.barplot(x=side_counts.index, y=side_counts.values)
    plt.xticks(rotation=45)
    st.pyplot(plt.gcf())

    # Visualization for 'Incident Rank'
    st.subheader("Incidents by Nature Rank")
    rank_counts = df['Incident Rank'].value_counts().sort_index()
    st.bar_chart(rank_counts)

    # Visualization for 'Nature'
    st.subheader("Nature of Incidents")
    nature_counts = df['Nature'].value_counts()
    plt.figure(figsize=(12, len(nature_counts)/2))
    sns.barplot(y=nature_counts.index, x=nature_counts.values)
    plt.xlabel("Count of Incidents")
    plt.ylabel("Nature")
    plt.title("Nature of Incidents Distribution")
    st.pyplot(plt.gcf(), clear_figure=True)

    # Visualization for 'EMSSTAT'
    st.subheader("Incidents with EMS Status")
    ems_counts = df['EMSSTAT'].value_counts()
    st.bar_chart(ems_counts)

# Streamlit webpage layout
st.title('Incident Analysis Dashboard')
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    # Save uploaded file to a temporary place
    temp_file_path = "uploaded_urls.csv"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    
    # Initialize progress bar
    progress_bar = st.progress(0)

    processed_data = process_data(temp_file_path, progress_bar)
    df = pd.DataFrame(processed_data, columns=['Day of the Week', 'Time of Day', 'Weather', 'Location Rank', 'Side of Town', 'Incident Rank', 'Nature', 'EMSSTAT'])
    display_data(df)

    # Complete the progress bar
    progress_bar.empty()
