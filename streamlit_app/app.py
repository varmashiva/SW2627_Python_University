"""
============================================================
EarlyRisk - University Academic Risk & Student Performance Dashboard
============================================================
Main Streamlit Application File
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import utils

# Page Configuration
st.set_page_config(
    page_title="EarlyRisk v1.0 • Academic Risk Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS Styling
CSS_PATH = Path(__file__).resolve().parent / "style.css"
if CSS_PATH.exists():
    with open(CSS_PATH) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load Data
@st.cache_data
def get_dataset():
    return utils.load_featured_data()

df = get_dataset()

# Sidebar Navigation & Profile
with st.sidebar:
    st.markdown("""
        <div class="brand-title">
            <span style="color:#F59E0B; font-size:1.4rem;">📊</span> EarlyRisk
        </div>
        <div class="brand-sub">v1.0 • Fall 2026</div>
    """, unsafe_allow_html=True)
    
    view_selection = st.radio(
        "Navigation",
        options=[
            "Advisor Dashboard",
            "Instructor View",
            "Alerts Queue",
            "Audit Log",
            "Insights & Recommendations"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("""
        <div style="margin-top: 100px; padding: 12px; background-color: #131B2E; border-radius: 8px; border: 1px solid #1E293B;">
            <div style="font-weight: 600; font-size: 0.85rem; color: #F8FAFC;">Dr. Priya Nair</div>
            <div style="font-size: 0.75rem; color: #64748B;">Academic Advisor</div>
        </div>
    """, unsafe_allow_html=True)


# Plotly Dark Theme Styling Helper
PLOTLY_LAYOUT = dict(
    paper_bgcolor='#131B2E',
    plot_bgcolor='#131B2E',
    font=dict(color='#94A3B8', family='Inter, sans-serif'),
    margin=dict(l=20, r=20, t=40, b=20),
    xaxis=dict(gridcolor='#1E293B', zerolinecolor='#1E293B'),
    yaxis=dict(gridcolor='#1E293B', zerolinecolor='#1E293B')
)


# ==========================================================
# VIEW 1: ADVISOR DASHBOARD
# ==========================================================
if view_selection == "Advisor Dashboard":
    # Top Header
    header_col1, header_col2 = st.columns([3, 1])
    with header_col1:
        st.markdown("<h2 style='margin:0; color:#F8FAFC;'>Advisor Dashboard</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#64748B; margin-bottom:15px;'>Summer 2026 · 2,001 students monitored</p>", unsafe_allow_html=True)
    with header_col2:
        st.markdown("""
            <div style="text-align: right;">
                <span class="live-pill">● Live</span>
            </div>
        """, unsafe_allow_html=True)
        
    # Top KPI Cards
    total_students = len(df)
    high_risk_cnt = len(df[df["Risk_Tier"] == "High"])
    med_risk_cnt = len(df[df["Risk_Tier"] == "Medium"])
    watch_cnt = len(df[df["Risk_Tier"] == "Watch"])
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Monitored</div>
                <div class="kpi-value">{total_students:,}</div>
                <div class="kpi-subtext">active students</div>
            </div>
        """, unsafe_allow_html=True)
        
    with kpi_col2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">High Risk</div>
                <div class="kpi-value kpi-value-high">{high_risk_cnt}</div>
                <div class="kpi-subtext">immediate action</div>
            </div>
        """, unsafe_allow_html=True)
        
    with kpi_col3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Medium Risk</div>
                <div class="kpi-value kpi-value-medium">{med_risk_cnt}</div>
                <div class="kpi-subtext">close monitoring</div>
            </div>
        """, unsafe_allow_html=True)
        
    with kpi_col4:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Watch</div>
                <div class="kpi-value kpi-value-watch">{watch_cnt:,}</div>
                <div class="kpi-subtext">check-in advised</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Refresh Banner
    st.markdown("""
        <div class="refresh-banner">
            <span>🔄 Data last refreshed: <b>2026-08-11 06:00 UTC</b> · Next refresh in 22h 00m</span>
        </div>
    """, unsafe_allow_html=True)
    
    # At-Risk Student Roster Controls & Section
    st.markdown("""
        <div class="card-header">
            <span>At-Risk Student Roster</span>
        </div>
    """, unsafe_allow_html=True)
    
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([1.5, 1.5, 3, 1])
    with filter_col1:
        tier_filter = st.selectbox("Risk Tier", options=["All", "High", "Medium", "Watch"])
    with filter_col2:
        course_filter = st.selectbox("Course", options=["All"] + utils.COURSES)
    with filter_col3:
        search_query = st.text_input("Search Student ID", placeholder="Search by student ID e.g. S1002...")
    with filter_col4:
        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export CSV", data=csv_data, file_name="at_risk_students.csv", mime="text/csv", use_container_width=True)

    # Filter Application
    filtered_df = df.copy()
    if tier_filter != "All":
        filtered_df = filtered_df[filtered_df["Risk_Tier"] == tier_filter]
    if course_filter != "All":
        filtered_df = filtered_df[filtered_df["Course"] == course_filter]
    if search_query.strip():
        filtered_df = filtered_df[filtered_df["Student_ID"].str.contains(search_query.strip(), case=False)]

    # Sort so highest risk appears on top
    filtered_df = filtered_df.sort_values(by="Risk_Score", ascending=False)
    
    # Format Display Table
    display_cols = ["Student_ID", "Course", "Risk_Tier", "Risk_Score", "Attendance (%)", "Submission_Rate", "Daily Study Hours", "Final Exam Marks (out of 100)"]
    display_df = filtered_df[display_cols].copy()
    display_df.columns = ["Student", "Course", "Risk Tier", "Risk Score", "Attendance", "Submission %", "Study Hrs/Day", "Final Marks"]
    
    st.dataframe(
        display_df.head(50),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Attendance": st.column_config.NumberColumn(format="%d%%"),
            "Submission %": st.column_config.NumberColumn(format="%d%%"),
            "Final Marks": st.column_config.NumberColumn(format="%d/100"),
            "Risk Score": st.column_config.ProgressColumn("Risk Score", min_value=0, max_value=100, format="%d")
        }
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visual Performance Overview Row
    st.markdown("<h4 style='color:#F8FAFC;'>Key Relationship Analysis</h4>", unsafe_allow_html=True)
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        att_avg = df.groupby("Attendance_Category", observed=False)["Final Exam Marks (out of 100)"].mean().reset_index()
        fig_att = px.bar(
            att_avg, x="Attendance_Category", y="Final Exam Marks (out of 100)",
            title="Avg Final Marks by Attendance Category",
            color="Attendance_Category",
            color_discrete_map={"Poor": "#EF4444", "Average": "#F59E0B", "Good": "#38BDF8", "Excellent": "#10B981"}
        )
        fig_att.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_att, use_container_width=True)
        
    with chart_col2:
        study_avg = df.groupby("Study_Hours_Category", observed=False)["Final Exam Marks (out of 100)"].mean().reset_index()
        fig_study = px.bar(
            study_avg, x="Study_Hours_Category", y="Final Exam Marks (out of 100)",
            title="Avg Final Marks by Daily Study Hours",
            color="Study_Hours_Category",
            color_discrete_map={"Low": "#EF4444", "Moderate": "#F59E0B", "High": "#10B981"}
        )
        fig_study.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_study, use_container_width=True)


# ==========================================================
# VIEW 2: INSTRUCTOR VIEW
# ==========================================================
elif view_selection == "Instructor View":
    header_col1, header_col2 = st.columns([3, 1])
    with header_col1:
        st.markdown("<h2 style='margin:0; color:#F8FAFC;'>Instructor View</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#64748B; margin-bottom:15px;'>Summer 2026 · 5 courses monitored</p>", unsafe_allow_html=True)
    with header_col2:
        st.markdown("<div style='text-align: right;'><span class='live-pill'>● Live</span></div>", unsafe_allow_html=True)

    # Course Selector Pills
    selected_course = st.radio("Select Course", options=["All Courses"] + utils.COURSES, horizontal=True)
    
    inst_df = df if selected_course == "All Courses" else df[df["Course"] == selected_course]
    
    # Course KPIs
    enrolled_count = len(inst_df)
    c_high = len(inst_df[inst_df["Risk_Tier"] == "High"])
    c_med = len(inst_df[inst_df["Risk_Tier"] == "Medium"])
    risk_exposure = round(((c_high + c_med) / enrolled_count) * 100, 1) if enrolled_count > 0 else 0.0
    
    kcol1, kcol2, kcol3, kcol4 = st.columns(4)
    with kcol1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">ENROLLED</div><div class="kpi-value">{enrolled_count}</div></div>', unsafe_allow_html=True)
    with kcol2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">HIGH RISK</div><div class="kpi-value kpi-value-high">{c_high}</div></div>', unsafe_allow_html=True)
    with kcol3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">MEDIUM RISK</div><div class="kpi-value kpi-value-medium">{c_med}</div></div>', unsafe_allow_html=True)
    with kcol4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">RISK EXPOSURE</div><div class="kpi-value kpi-value-medium">{risk_exposure}%</div></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Two Columns layout matching screenshot 2
    c_left, c_right = st.columns(2)
    
    with c_left:
        # Risk Distribution - All Courses
        course_risk = df.groupby(["Course", "Risk_Tier"]).size().reset_index(name="Count")
        fig_dist = px.bar(
            course_risk, x="Course", y="Count", color="Risk_Tier",
            title="Risk Distribution — All Courses", barmode="group",
            color_discrete_map={"High": "#EF4444", "Medium": "#F59E0B", "Watch": "#06B6D4"}
        )
        fig_dist.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_dist, use_container_width=True)
        
    with c_right:
        # Cohort Engagement Profile Radar Chart
        metrics_radar = ['Attendance', 'Submissions', 'Exam Scores', 'Study Hours', 'Internal Score']
        vals = [
            inst_df["Attendance (%)"].mean(),
            inst_df["Submission_Rate"].mean(),
            inst_df["Final Exam Marks (out of 100)"].mean(),
            (inst_df["Daily Study Hours"].mean() / df["Daily Study Hours"].max()) * 100,
            (inst_df["Average_Internal_Score"].mean() / 40) * 100
        ]
        
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=vals, theta=metrics_radar, fill='toself',
            line_color='#06B6D4', fillcolor='rgba(6, 182, 212, 0.25)'
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor='#1E293B'),
                angularaxis=dict(gridcolor='#1E293B'),
                bgcolor='#131B2E'
            ),
            title=f"Cohort Engagement Profile — {selected_course}",
            **PLOTLY_LAYOUT
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # Risk Heatmap across courses
    st.markdown("<h4 style='color:#F8FAFC;'>Risk Heatmap by Attendance Category</h4>", unsafe_allow_html=True)
    heatmap_data = pd.crosstab(df["Course"], df["Attendance_Category"], values=df["Risk_Score"], aggfunc="mean").fillna(0)
    fig_heat = px.imshow(
        heatmap_data, text_auto=".1f", color_continuous_scale="Reds",
        title="Average Risk Score Heatmap (Course vs Attendance Category)"
    )
    fig_heat.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig_heat, use_container_width=True)


# ==========================================================
# VIEW 3: ALERTS QUEUE
# ==========================================================
elif view_selection == "Alerts Queue":
    st.markdown("<h2 style='margin:0; color:#F8FAFC;'>Alert Queue</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B; margin-bottom:20px;'>Active early warning triggers requiring academic advisor intervention</p>", unsafe_allow_html=True)
    
    alerts_df = utils.generate_alerts(df)
    
    col_a1, col_a2 = st.columns([4, 1])
    with col_a1:
        st.markdown(f"**Showing {len(alerts_df)} Unresolved Alerts**")
    
    for idx, row in alerts_df.iterrows():
        tier_class = "alert-card" if row["tier"] == "High" else "alert-card alert-card-medium"
        badge_class = "badge-high" if row["tier"] == "High" else "badge-medium"
        
        st.markdown(f"""
            <div class="{tier_class}">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div>
                        <strong style="color:#F8FAFC; font-size:1.05rem;">⚠️ Student {row['student_id']}</strong>
                        <span style="color:#64748B; font-size:0.85rem; margin-left:8px;">{row['course']} · {row['timestamp']}</span>
                        <span class="badge {badge_class}" style="margin-left:12px;">{row['tier']} Risk</span>
                    </div>
                </div>
                <div style="font-size:0.9rem; color:#CBD5E1; margin-bottom:12px;">
                    {row['message']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        btn_c1, btn_c2, btn_c3, _ = st.columns([1, 1, 1, 4])
        with btn_c1:
            st.button("⏰ Snooze", key=f"snooze_{idx}")
        with btn_c2:
            st.button("🚨 Escalate", key=f"esc_{idx}")
        with btn_c3:
            st.button("✖ Dismiss", key=f"dis_{idx}")
        st.markdown("<hr style='border-color:#1E293B; margin-top:8px; margin-bottom:16px;'>", unsafe_allow_html=True)


# ==========================================================
# VIEW 4: AUDIT LOG
# ==========================================================
elif view_selection == "Audit Log":
    st.markdown("<h2 style='margin:0; color:#F8FAFC;'>Audit Log</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B; margin-bottom:20px;'>FERPA-compliant security & event tracking log</p>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="ferpa-banner">
            🛡️ <b>FERPA Policy Compliance:</b> All data access, profile views, and alert actions are logged in compliance with institutional policy. Logs are immutable and retained for 7 years.
        </div>
    """, unsafe_allow_html=True)
    
    logs_df = utils.generate_audit_logs()
    
    st.dataframe(
        logs_df,
        use_container_width=True,
        hide_index=True
    )


# ==========================================================
# VIEW 5: INSIGHTS & RECOMMENDATIONS
# ==========================================================
elif view_selection == "Insights & Recommendations":
    st.markdown("<h2 style='margin:0; color:#F8FAFC;'>Business Insights & Recommendations</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B; margin-bottom:20px;'>Analytical conclusions and strategic recommendations derived from the university dataset</p>", unsafe_allow_html=True)
    
    col_i1, col_i2 = st.columns(2)
    
    with col_i1:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#F8FAFC;'>Key Business Insights</h3>", unsafe_allow_html=True)
        
        insights_df = utils.load_summary_csv("business_insights.csv")
        if not insights_df.empty:
            for idx, row in insights_df.iterrows():
                val = row.iloc[0]
                if isinstance(val, str) and not val.startswith("==") and not val.startswith("report") and not val.startswith("main"):
                    st.markdown(f"• **{val}**")
        else:
            st.write("1. Attendance below 75% is the single strongest indicator of academic risk.")
            st.write("2. Average Internal Score has the highest correlation (0.87) with final exam success.")
            st.write("3. Low performance in Internal Test 1 serves as an early warning predictor.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_i2:
        st.markdown("<div class='content-card'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#F8FAFC;'>Strategic Recommendations</h3>", unsafe_allow_html=True)
        
        rec_df = utils.load_summary_csv("recommendations.csv")
        if not rec_df.empty:
            for idx, row in rec_df.iterrows():
                val = row.iloc[0]
                if isinstance(val, str) and not val.startswith("==") and not val.startswith("report") and not val.startswith("main"):
                    st.markdown(f"✔ {val}")
        else:
            st.write("✔ Establish an Early Warning System when attendance falls below 75%.")
            st.write("✔ Offer targeted academic counseling after Internal Test 1.")
            st.write("✔ Organize mandatory study groups for students with low study hours.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Feature Importance Correlation Chart
    feat_df = utils.load_summary_csv("feature_importance.csv")
    if not feat_df.empty:
        st.markdown("<h4 style='color:#F8FAFC;'>Feature Correlation Matrix with Final Exam Marks</h4>", unsafe_allow_html=True)
        # Compute real correlation matrix from current dataset
        numeric_cols = ["Attendance (%)", "Internal Test 1 (out of 40)", "Internal Test 2 (out of 40)", 
                        "Assignment Score (out of 10)", "Daily Study Hours", "Average_Internal_Score", 
                        "Engagement_Score", "Final Exam Marks (out of 100)"]
        corr = df[numeric_cols].corr()
        fig_corr = px.imshow(
            corr, text_auto=".2f", color_continuous_scale="Viridis",
            title="Correlation Heatmap (All Dataset Features)"
        )
        fig_corr.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_corr, use_container_width=True)
