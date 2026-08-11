"""
============================================================
PHASE 3 : SQL ANALYSIS
============================================================

Objective:
Load the cleaned dataset into SQLite and execute
business-related SQL queries.

============================================================
"""

import os
import sqlite3
import pandas as pd

print("=" * 60)
print("PHASE 3 : SQL ANALYSIS")
print("=" * 60)

# ----------------------------------------------------------
# Project Paths
# ----------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "cleaned_final_marks.csv"
)

DATABASE_DIR = os.path.join(BASE_DIR, "database")
os.makedirs(DATABASE_DIR, exist_ok=True)

DATABASE_PATH = os.path.join(
    DATABASE_DIR,
    "student_performance.db"
)

OUTPUT_DIR = os.path.join(BASE_DIR, "output", "sql")
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

    "Student ID":"Student_ID",

    "Attendance (%)":"Attendance",

    "Assignment Score (out of 10)":"Assignment_Score",

    "Internal Test 1 (out of 40)":"Internal_Test_1",

    "Internal Test 2 (out of 40)":"Internal_Test_2",

    "Daily Study Hours":"Study_Hours",

    "Final Exam Marks (out of 100)":"Final_Exam_Marks"

})

# ----------------------------------------------------------
# Create Database
# ----------------------------------------------------------

connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()

print("Database Connected.")

# ----------------------------------------------------------
# Insert Data
# ----------------------------------------------------------

df.to_sql(

    "student_performance",

    connection,

    if_exists="replace",

    index=False

)

print("Table Created Successfully.")

# ----------------------------------------------------------
# SQL Queries
# ----------------------------------------------------------

queries = {

"total_students":
"""
SELECT COUNT(*) AS Total_Students
FROM student_performance
""",

"average_attendance":
"""
SELECT ROUND(AVG(Attendance),2)
AS Average_Attendance
FROM student_performance
""",

"top_students":
"""
SELECT Student_ID,
Final_Exam_Marks

FROM student_performance

ORDER BY Final_Exam_Marks DESC

LIMIT 10
""",

"students_at_risk":
"""
SELECT Student_ID,
Final_Exam_Marks

FROM student_performance

WHERE Final_Exam_Marks < 50
""",

"average_marks":
"""
SELECT ROUND(
AVG(Final_Exam_Marks),2)
AS Average_Final_Marks

FROM student_performance
"""

}

print("\nExecuting SQL Queries...")

for name, query in queries.items():

    result = pd.read_sql_query(query, connection)

    print(f"\n{name}")

    print(result)

    result.to_csv(

        os.path.join(

            OUTPUT_DIR,

            f"{name}.csv"

        ),

        index=False

    )

print("\nSQL Results Saved.")

connection.close()

print("\nDatabase Closed.")

print("\nGenerated Files")

print("---------------------")

for file in os.listdir(OUTPUT_DIR):

    print(file)

print("\nSQL Analysis Completed Successfully.")