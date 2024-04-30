import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Append the directory of your script to Python's search path
sys.path.append(os.path.abspath('.'))

# Importing your functions from assignment2.py
from assignment2 import download_pdf, extract_incidents, calculate_location_ranks, calculate_incident_ranks, augment_data, get_urls_from_csv

def process_data(urls_filename):
    urls = get_urls_from_csv(urls_filename)
    all_augmented_records = []
    for url in urls:
        download_pdf(url)
        pdf_path = "./docs/incident_report.pdf"
        incidents = extract_incidents(pdf_path)
        location_ranks = calculate_location_ranks(incidents)
        incident_ranks = calculate_incident_ranks(incidents)
        api_key = 'Your_API_Key'  # Replace with your actual API key
        augmented_records = augment_data(incidents, location_ranks, incident_ranks, api_key)
        all_augmented_records.extend(augmented_records)
    return all_augmented_records

def display_data(df):
    st.write(df)
    
    # Visualization for 'Day of the Week'
    st.subheader("Crime Rates by Day of the Week")
    day_counts = df['Day of the Week'].value_counts().sort_index()
    plt.figure(figsize=(6, 6))
    plt.pie(day_counts, labels=day_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Crime Rates by Day of the Week')
    st.pyplot(plt.gcf())

    # Visualization for 'Time of Day' - using a line graph
    st.subheader("Incidents by Time of Day")
    time_counts = df['Time of Day'].value_counts().sort_index()
    plt.figure(figsize=(10, 5))
    plt.plot(time_counts.index, time_counts.values)
    plt.xticks(time_counts.index)
    plt.xlabel("Time of Day")
    plt.ylabel("Number of Incidents")
    plt.title("Incidents by Time of Day")
    st.pyplot(plt.gcf())

    # Visualization for 'Weather' - using a bar chart
    st.subheader("Incidents by Weather Conditions")
    weather_counts = df['Weather'].value_counts().sort_index()
    plt.figure(figsize=(10, 5))
    sns.barplot(x=weather_counts.index, y=weather_counts.values)
    plt.xticks(rotation=45)
    plt.xlabel("Weather Condition")
    plt.ylabel("Number of Incidents")
    plt.title("Incidents by Weather Conditions")
    st.pyplot(plt.gcf())

    # Visualization for 'Location Rank' - using a heat map
    st.subheader("Heat Map of Incidents by Location Rank")
    # Convert location ranks into a matrix for heatmap
    rank_matrix = df['Location Rank'].value_counts().sort_index().to_numpy()
    rank_matrix = np.reshape(rank_matrix, (1, -1))
    sns.heatmap(rank_matrix, annot=True, fmt="d", cmap="YlGnBu")
    plt.xlabel("Location Rank")
    plt.ylabel("Number of Incidents")
    plt.title("Heat Map of Incidents by Location Rank")
    st.pyplot(plt.gcf())

    # Visualization for 'Side of Town' - using a horizontal bar chart
    st.subheader("Incidents by Side of Town")
    side_counts = df['Side of Town'].value_counts()
    plt.figure(figsize=(12, 8))
    sns.barplot(x=side_counts.values, y=side_counts.index)
    plt.xlabel("Number of Incidents")
    plt.ylabel("Side of Town")
    plt.title("Incidents by Side of Town")
    st.pyplot(plt.gcf())

    # Visualization for 'Incident Rank' - using a scatter plot
    st.subheader("Scatter Plot of Incidents by Nature Rank")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=df['Incident Rank'], y=df.index)
    plt.xlabel("Incident Rank")
    plt.ylabel("Incidents")
    plt.title("Scatter Plot of Incidents by Nature Rank")
    st.pyplot(plt.gcf())

    # Visualization for 'Nature' - using a horizontal bar chart
    st.subheader("Nature of Incidents")
    nature_counts = df['Nature'].value_counts()
    plt.figure(figsize=(12, len(nature_counts)/2))
    sns.barplot(x=nature_counts.values, y=nature_counts.index)
    plt.xlabel("Count of Incidents")
    plt.ylabel("Nature")
    plt.title("Nature of Incidents Distribution")
    st.pyplot(plt.gcf())

    # Visualization for 'EMSSTAT' - using a pie chart
    st.subheader("Incidents with EMS Status")
    ems_counts = df['EMSSTAT'].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(ems_counts, labels=ems_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('EMS Status of Incidents')
    st.pyplot(plt.gcf())

# Streamlit webpage layout
st.title('Incident Analysis Dashboard')
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    # Save uploaded file to a temporary place
    temp_file_path = "uploaded_urls.csv"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    
    processed_data = process_data(temp_file_path)
    df = pd.DataFrame(processed_data, columns=['Day of the Week', 'Time of Day', 'Weather', 'Location Rank', 'Side of Town', 'Incident Rank', 'Nature', 'EMSSTAT'])
    display_data(df)