"""
Utility helper functions for loading, processing, and generating view data
for the University Academic Risk & Student Performance Streamlit Dashboard.
"""

import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "featured_final_marks.csv"
SUMMARY_DIR = PROJECT_ROOT / "output" / "summaries"
REPORT_DIR = PROJECT_ROOT / "output" / "reports"

COURSES = ["CS 410", "STAT 302", "MATH 201", "ENG 215", "PHYS 110"]

def load_featured_data():
    """Load the featured dataset and enrich with course assignment and risk scores."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")
    
    df = pd.read_csv(DATA_PATH)
    
    # Deterministic course mapping based on Student_ID index
    df["Course_Index"] = df["Student_ID"].apply(lambda s: int(str(s).replace("S", "")) % len(COURSES))
    df["Course"] = df["Course_Index"].apply(lambda idx: COURSES[idx])
    
    # Calculate numeric Risk Score (0 - 100) where higher = higher risk
    # High risk students have scores >75, Medium 50-74, Low/Watch <50
    raw_risk = (
        (100 - df["Final Exam Marks (out of 100)"]) * 0.50 +
        (100 - df["Attendance (%)"]) * 0.30 +
        (10 - df["Assignment Score (out of 10)"]) * 10 * 0.20
    )
    df["Risk_Score"] = np.clip(raw_risk.round(), 10, 99).astype(int)
    
    # Map Risk Tier display names to match EarlyRisk screenshot (High, Medium, Watch)
    def map_tier(risk_label):
        if risk_label == "High Risk":
            return "High"
        elif risk_label == "Moderate Risk":
            return "Medium"
        else:
            return "Watch"
            
    df["Risk_Tier"] = df["Academic_Risk"].apply(map_tier)
    df["Submission_Rate"] = (df["Assignment Score (out of 10)"] * 10).astype(int)
    df["Last_Updated"] = "2026-08-11 08:42"
    
    return df

def load_summary_csv(filename):
    """Load a summary CSV file from output/summaries/."""
    path = SUMMARY_DIR / filename
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()

def generate_alerts(df):
    """Generate early warning alerts dynamically based on dataset thresholds."""
    alerts = []
    
    # High risk & low attendance candidates
    high_risk_df = df[df["Risk_Tier"] == "High"].sort_values(by="Risk_Score", ascending=False).head(15)
    for idx, row in high_risk_df.iterrows():
        alerts.append({
            "id": f"ALT-{idx}",
            "student_id": row["Student_ID"],
            "course": row["Course"],
            "tier": "High",
            "status": "new",
            "timestamp": "2026-08-11 08:42",
            "message": f"Risk score reached {row['Risk_Score']} — Attendance {row['Attendance (%)']}%, Assignment score {row['Assignment Score (out of 10)']}/10, Internal test avg {row['Average_Internal_Score']:.1f}/40."
        })
        
    medium_risk_df = df[df["Risk_Tier"] == "Medium"].sort_values(by="Risk_Score", ascending=False).head(10)
    for idx, row in medium_risk_df.iterrows():
        alerts.append({
            "id": f"ALT-{idx}",
            "student_id": row["Student_ID"],
            "course": row["Course"],
            "tier": "Medium",
            "status": "snoozed" if idx % 2 == 0 else "escalated",
            "timestamp": "2026-08-11 07:15",
            "message": f"Submission rate at {row['Submission_Rate']}% with study hours averaging {row['Daily Study Hours']} hrs/day. Risk score {row['Risk_Score']}."
        })
        
    return pd.DataFrame(alerts)

def generate_audit_logs():
    """Generate FERPA-compliant audit logs matching design screenshot."""
    logs = [
        {"timestamp": "2026-08-11 09:01", "user": "Dr. Priya Nair", "role": "Advisor", "action": "Viewed student risk profile", "target": "Student Cohort (S1000 - S1050)"},
        {"timestamp": "2026-08-11 08:55", "user": "Dr. Priya Nair", "role": "Advisor", "action": "Escalated high-risk alert", "target": "S1002 - CS 410"},
        {"timestamp": "2026-08-11 08:30", "user": "Prof. James Liu", "role": "Instructor", "action": "Viewed course risk summary", "target": "CS 410 - Fall 2026"},
        {"timestamp": "2026-08-11 06:00", "user": "System (ETL)", "role": "ETL", "action": "Data refresh completed", "target": "All courses - 2,001 records"},
        {"timestamp": "2026-08-10 19:35", "user": "Dr. Priya Nair", "role": "Advisor", "action": "Snoozed attendance warning", "target": "S1014 - MATH 201"},
        {"timestamp": "2026-08-10 16:00", "user": "Prof. Clara Moss", "role": "Instructor", "action": "Viewed student profile", "target": "S1028 - STAT 302"},
        {"timestamp": "2026-08-10 06:00", "user": "System (ETL)", "role": "ETL", "action": "Data refresh completed", "target": "All courses - 2,001 records"}
    ]
    return pd.DataFrame(logs)
