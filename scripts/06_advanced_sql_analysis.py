"""
============================================================
PHASE 6 : ADVANCED SQL ANALYSIS
============================================================

Objective:
Create normalized SQL tables, build views,
execute advanced SQL queries and export results.

Author : SW Team 1 KARE
============================================================
"""

import os
import sqlite3
import pandas as pd

print("=" * 60)
print("PHASE 6 : ADVANCED SQL ANALYSIS")
print("=" * 60)

# ----------------------------------------------------------
# Paths
# ----------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "cleaned_final_marks.csv"
)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "database",
    "student_performance.db"
)

QUERY_DIR = os.path.join(
    BASE_DIR,
    "queries"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "output",
    "sql",
    "advanced"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------

print("\nLoading Dataset...")

df = pd.read_csv(DATA_PATH)

print("Dataset Loaded Successfully.")

# ----------------------------------------------------------
# Rename Columns
# ----------------------------------------------------------

df = df.rename(columns={

    "Student ID": "Student_ID",
    "Attendance (%)": "Attendance",
    "Assignment Score (out of 10)": "Assignment_Score",
    "Internal Test 1 (out of 40)": "Internal_Test_1",
    "Internal Test 2 (out of 40)": "Internal_Test_2",
    "Daily Study Hours": "Study_Hours",
    "Final Exam Marks (out of 100)": "Final_Exam_Marks"

})

# ----------------------------------------------------------
# Connect Database
# ----------------------------------------------------------

connection = sqlite3.connect(DATABASE_PATH)

print("Connected to SQLite.")

# ----------------------------------------------------------
# Create Normalized Tables
# ----------------------------------------------------------

students = df[["Student_ID"]]

performance = df[
[
    "Student_ID",
    "Internal_Test_1",
    "Internal_Test_2",
    "Final_Exam_Marks"
]
]

engagement = df[
[
    "Student_ID",
    "Attendance",
    "Assignment_Score",
    "Study_Hours"
]
]

students.to_sql(
    "students",
    connection,
    if_exists="replace",
    index=False
)

performance.to_sql(
    "performance",
    connection,
    if_exists="replace",
    index=False
)

engagement.to_sql(
    "engagement",
    connection,
    if_exists="replace",
    index=False
)

print("Normalized tables created.")

# ----------------------------------------------------------
# Create View
# ----------------------------------------------------------

view_file = os.path.join(
    QUERY_DIR,
    "03_create_views.sql"
)

with open(view_file, "r") as file:

    connection.executescript(file.read())

print("View created successfully.")

# ----------------------------------------------------------
# Read Advanced Queries
# ----------------------------------------------------------

query_file = os.path.join(
    QUERY_DIR,
    "04_advanced_queries.sql"
)

with open(query_file, "r") as file:

    sql_script = file.read()

queries = [
    q.strip()
    for q in sql_script.split(";")
    if q.strip()
]

# ----------------------------------------------------------
# Output File Names
# ----------------------------------------------------------

output_files = [

    "join_student_report.csv",

    "attendance_category_summary.csv",

    "high_performing_categories.csv",

    "above_average_students.csv",

    "top_performers.csv",

    "grade_distribution.csv"

]

print("\nExecuting SQL Queries...\n")

for query, filename in zip(queries, output_files):

    result = pd.read_sql_query(query, connection)

    print("=" * 50)

    print(filename)

    print(result.head())

    result.to_csv(

        os.path.join(
            OUTPUT_DIR,
            filename
        ),

        index=False

    )

print("\nAll SQL queries executed successfully.")

connection.close()

print("\nDatabase connection closed.")

print("\nOutput saved to:")

print(OUTPUT_DIR)

print("\nADVANCED SQL ANALYSIS COMPLETED")