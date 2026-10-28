import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data, call_ollama

st.set_page_config(page_title="AI Language Assistant", layout="wide", page_icon="🎓")

students_df, lessons_df = load_data()

st.title("🎓 AI Language Learning Assistant")
st.caption("TCS Tech Day Use Case 13 • Executive Dashboard & Learning Analytics")

# Sidebar Filters
st.sidebar.header("Data Filters")
selected_dept = st.sidebar.multiselect("Department", options=students_df["department"].unique(), default=students_df["department"].unique())
selected_year = st.sidebar.multiselect("Year", options=students_df["year"].unique(), default=students_df["year"].unique())

filtered = students_df[(students_df["department"].isin(selected_dept)) & (students_df["year"].isin(selected_year))]

# 4 Key Metrics
avg_score = round(filtered[["grammar", "vocabulary", "speaking", "writing", "listening"]].mean().mean(), 1)
pct_advanced = round((filtered["level"] == "Advanced").mean() * 100, 1)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Enrolled Students", len(filtered))
k2.metric("Overall Score Avg", f"{avg_score}/100")
k3.metric("Avg Study Hours/Wk", f"{filtered['weekly_study_hours'].mean():.1f} hrs")
k4.metric("Advanced Learners", f"{pct_advanced}%")

st.markdown("---")

# Charts Row 1
c1, c2 = st.columns(2)
with c1:
    skill_means = filtered[["grammar", "vocabulary", "speaking", "writing", "listening"]].mean().reset_index()
    skill_means.columns = ["Skill", "Score"]
    fig1 = px.bar(skill_means, x="Skill", y="Score", title="Average Performance by Core Skill", text="Score", color="Score", color_continuous_scale="Teal")
    fig1.update_layout(yaxis_range=[0, 100])
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    dept_score = filtered.groupby("department")[["grammar", "vocabulary", "speaking", "writing", "listening"]].mean().mean(axis=1).reset_index()
    dept_score.columns = ["Department", "Average Score"]
    fig2 = px.bar(dept_score, x="Department", y="Average Score", title="Average Score by Department", color="Average Score", color_continuous_scale="Blues")
    fig2.update_layout(yaxis_range=[0, 100])
    st.plotly_chart(fig2, use_container_width=True)

# Charts Row 2
c3, c4 = st.columns(2)
with c3:
    progress_cols = ["month1", "month2", "month3", "month4", "month5", "month6"]
    progress_trend = filtered[progress_cols].mean().reset_index()
    progress_trend.columns = ["Month", "Score"]
    fig3 = px.line(progress_trend, x="Month", y="Score", markers=True, title="6-Month Cohort Score Progression")
    fig3.update_layout(yaxis_range=[40, 95])
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    fig4 = px.scatter(
        filtered, x="weekly_study_hours", y="writing",
        color="level", size="streak_days",
        hover_data=["name", "career_goal"],
        title="Weekly Study Hours vs. Writing Proficiency"
    )
    st.plotly_chart(fig4, use_container_width=True)

# LLM AI Insights
st.subheader("💡 Automated AI Cohort Insights")
if st.button("Generate Cohort Insights with AI"):
    with st.spinner("Analyzing performance trends via local LLM..."):
        prompt = f"Analyze these student metrics: Average score {avg_score}/100, Advanced percentage {pct_advanced}%, lowest skill performance on average. Provide 3 actionable executive bullets for the department heads."
        insight = call_ollama(prompt)
        st.info(insight)