
# Datasheet for Assignment 2 Dataset

## Motivation

**For what purpose was the dataset created?**
- This dataset was created as part of an educational assignment (CIS 6930, Spring 2024) to practice data augmentation techniques on incident records extracted from public police department reports. The augmented dataset aims to facilitate further analysis, keeping fairness and bias in mind.

**Who created this dataset and on behalf of which entity?**
- The dataset was created by students of the CIS 6930 course, under the guidance of the University of Florida's Department of Computer & Information Science & Engineering.

## Composition

**What do the instances represent?**
- Each instance in the dataset represents an augmented record of a police incident, including metadata such as the day of the week, time of day, weather conditions, and incident specifics like nature and EMS status.

**How many instances are there in total?**
- The total number of instances varies depending on the input files processed. Each input PDF containing incident reports contributes to the dataset's size.

**What data does each instance consist of?**
- `Day of the Week`: Numeric representation (1-7) indicating the day of the week.
- `Time of Day`: Hour of the day (0-24) the incident was reported.
- `Weather`: WMO weather code representing the weather condition at the incident's time and location.
- `Location Rank`: An integer ranking based on the frequency of incidents at the location.
- `Side of Town`: Categorization of the incident's location based on its geographic orientation to the town's center.
- `Incident Rank`: Ranking of the incident's nature based on frequency.
- `Nature`: Direct description of the incident's nature.
- `EMSSTAT`: Boolean indicating if EMS was dispatched.

**Is there any missing data?**
- Data completeness depends on the source PDFs. Missing entries may occur due to extraction errors or incomplete records in the source data.

## Collection Process

**How was the data collected?**
- Data was programmatically extracted from publicly available PDF reports from the police department's website using a Python script. Subsequent data augmentation was performed by the script to enrich the dataset with additional metadata.

**Who was involved in the data collection process?**
- The collection and augmentation process were automated, with students overseeing the execution of the Python script to ensure correct operation.

## Preprocessing/Cleaning

**Was any preprocessing/cleaning done?**
- Preprocessing involved the extraction of incidents from PDF files and their conversion into a structured format. Cleaning steps were taken to address inconsistencies in the data, such as missing values or irregular formatting.

**What kind of information was removed from the dataset?**
- Information not relevant to the analysis, such as header/footer text from PDF pages, was removed during preprocessing.

## Intended Uses

**For what tasks is the dataset suitable?**
- The dataset is suitable for analyzing trends in police incidents, including temporal patterns, weather impact, and geographic distribution of incidents.

**Who is the intended audience for the dataset?**
- The intended audience includes data science students, researchers, and law enforcement agencies interested in data-driven insights into incident patterns.

## Distribution

**How will the dataset be distributed?**
- The dataset, along with the code for its generation, is available through the course's online repository. Access is granted for educational purposes to students and faculty members.
