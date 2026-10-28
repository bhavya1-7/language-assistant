import streamlit as st
import plotly.graph_objects as go
from utils import load_data, call_ollama

st.set_page_config(page_title="Recommendations", layout="wide")
students_df, lessons_df = load_data()

st.title("🎯 Personalized Recommendations & Study Plan")
st.caption("AI-driven weakness diagnosis and custom curriculum matching")

student_names = students_df["student_id"] + " - " + students_df["name"]
selected_label = st.selectbox("Select Student", student_names)
stu_id = selected_label.split(" - ")[0]
student = students_df[students_df["student_id"] == stu_id].iloc[0]

# Left Profile & Radar, Right Recommendations
col1, col2 = st.columns([1, 1.2])

skills = ["grammar", "vocabulary", "speaking", "writing", "listening"]
scores = [student[s] for s in skills]

sorted_skills = sorted([(s.capitalize(), student[s]) for s in skills], key=lambda x: x[1])
weakest_skills = [sorted_skills[0][0], sorted_skills[1][0]]

with col1:
    st.subheader(f"{student['name']} ({student['student_id']})")
    st.write(f"**Department:** {student['department']} | **Year:** {student['year']}")
    st.write(f"**Proficiency Level:** {student['level']} | **Career Goal:** :blue[{student['career_goal']}]")
    
    fig = go.Figure(data=go.Scatterpolar(r=scores + [scores[0]], theta=[s.capitalize() for s in skills] + [skills[0].capitalize()], fill='toself', name='Score'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, title="Skill Competency Radar")
    st.plotly_chart(fig, use_container_width=True)
    
    st.error(f"⚠️ Primary Weaknesses: **{weakest_skills[0]}** ({sorted_skills[0][1]}/100) & **{weakest_skills[1]}** ({sorted_skills[1][1]}/100)")

with col2:
    st.subheader("📚 Tailored Lesson Recommendations")
    matched_lessons = lessons_df[
        (lessons_df["skill"].isin(weakest_skills)) | 
        (lessons_df["career_tag"] == student["career_goal"])
    ].head(5)
    
    for _, row in matched_lessons.iterrows():
        with st.expander(f"{row['title']} ({row['skill']} • {row['duration_min']} mins)"):
            st.write(f"**Target Level:** {row['level']}")
            st.write(f"**Career Focus:** {row['career_tag']}")
            st.button(f"Enroll in {row['lesson_id']}", key=row['lesson_id'])

    st.markdown("---")
    st.subheader("🤖 Automated 7-Day Action Plan")
    if st.button("Generate Personalized AI Study Plan"):
        with st.spinner("Generating targeted curriculum with LLM..."):
            prompt = (
                f"Student: {student['name']}. Level: {student['level']}. Goal: {student['career_goal']}. "
                f"Weak skills: {weakest_skills[0]} and {weakest_skills[1]}. "
                f"Generate a concise 7-day study schedule with 1 focused activity per day."
            )
            plan = call_ollama(prompt)
            st.success(plan)