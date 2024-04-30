
# CIS 6930, Spring 2024 Assignment 3 - Incident Analysis Dashboard

## Author
Name: [Srinivas Pavan Singh Runval]  
UFID: [93324706]

## Introduction
Assignment 3 expands on the data processing of police incident records previously enriched in Assignment 2. The primary focus is to visualize the augmented data using a Streamlit dashboard, allowing interactive exploration of incident metrics such as the day of the week, time of day, weather conditions, location ranks, and nature of incidents. This dashboard serves as a practical application to demonstrate real-time data analysis capabilities in an interactive environment.

## Running Instructions
To execute the Streamlit dashboard, follow the instructions below. Ensure Python 3 and required libraries (`streamlit`, `pandas`, `matplotlib`, `seaborn`, etc.) are installed.

1. **Setup Environment:**  
   Ensure Python 3.6 or newer is installed along with `pipenv` for handling virtual environments and dependencies.
   ```bash
   pip install pipenv
   ```

2. **Install Dependencies:**  
   Navigate to the project directory and install dependencies using:
   ```bash
   pipenv install
   ```

3. **Activate Virtual Environment:**  
   Activate the virtual environment with:
   ```bash
   pipenv shell
   ```
   Alternatively, use `pipenv run` before commands to run them directly within the virtual environment.

4. **Execute the Dashboard:**  
   Use the following command to run the Streamlit dashboard:
   ```bash
   pipenv run streamlit run your_dashboard_script.py
   ```
   Replace `your_dashboard_script.py` with the actual path to your Streamlit script.

## Detailed Function Descriptions
The main functionalities included in the dashboard script are:

- **`process_data(urls_filename, progress_bar)`:** Processes each URL from the given CSV file, downloads PDFs, extracts incidents, and augments data, updating a progress bar in the dashboard.
- **`display_data(df)`:** Displays data and various interactive visualizations in the Streamlit dashboard.
- **Visualization Components:** Include pie charts, line charts, and bar charts to explore different aspects of the incident data such as day of the week, time of day, and weather conditions.

## Bugs & Assumptions
- **Bugs:** No major bugs are known. Ensure all dependencies are correctly installed and API keys are set before execution.
- **Assumptions:** Assumes a stable internet connection for downloading PDFs and that the incident PDFs follow a uniform format for correct data extraction and visualization.

## Resources
- Streamlit Documentation: [[Link to Streamlit documentation](https://docs.streamlit.io)]
- Pandas Documentation: [[Link to Pandas documentation](https://pandas.pydata.org/pandas-docs/stable/index.html)]
- Matplotlib and Seaborn for Visualization: [[Link to Matplotlib](https://matplotlib.org)], [[Link to Seaborn](https://seaborn.pydata.org)]
