import os
import random
import sqlite3
import pandas as pd

os.makedirs("data", exist_ok=True)
random.seed(42)

# 1. Generate 80 Students
depts = ["CSE", "ECE", "Mechanical", "Civil", "MBA"]
levels = ["Beginner", "Intermediate", "Advanced"]
goals = ["Software Engineer", "Data Analyst", "Manager", "Researcher", "Government Services"]
names = [
    "Aarav Sharma", "Aditi Patel", "Rohan Mehta", "Priya Singh", "Ananya Verma",
    "Vikram Reddy", "Sneha Nair", "Kunal Joshi", "Divya Pillai", "Arjun Rao",
    "Pooja Deshmukh", "Rahul Gupta", "Kavya Iyer", "Siddharth Das", "Ishita Roy"
]

students = []
for i in range(1, 81):
    base_score = random.randint(35, 88)
    lvl = "Beginner" if base_score < 55 else ("Intermediate" if base_score < 75 else "Advanced")
    
    # Skill scores with variation
    g = max(10, min(100, base_score + random.randint(-12, 12)))
    v = max(10, min(100, base_score + random.randint(-10, 10)))
    s = max(10, min(100, base_score + random.randint(-15, 15)))
    w = max(10, min(100, base_score + random.randint(-10, 10)))
    l = max(10, min(100, base_score + random.randint(-8, 12)))
    
    m1 = max(20, min(100, base_score - 10 + random.randint(-5, 5)))
    m2 = max(20, min(100, m1 + random.randint(1, 4)))
    m3 = max(20, min(100, m2 + random.randint(0, 5)))
    m4 = max(20, min(100, m3 + random.randint(1, 6)))
    m5 = max(20, min(100, m4 + random.randint(0, 4)))
    m6 = max(20, min(100, m5 + random.randint(1, 5)))

    students.append({
        "student_id": f"STU{i:03d}",
        "name": f"{random.choice(names)} {i}",
        "department": random.choice(depts),
        "year": random.randint(1, 4),
        "language": "English",
        "level": lvl,
        "grammar": g,
        "vocabulary": v,
        "speaking": s,
        "writing": w,
        "listening": l,
        "weekly_study_hours": round(random.uniform(2.5, 18.0), 1),
        "streak_days": random.randint(0, 35),
        "career_goal": random.choice(goals),
        "month1": m1, "month2": m2, "month3": m3,
        "month4": m4, "month5": m5, "month6": m6
    })

df_students = pd.DataFrame(students)
df_students.to_csv("data/students.csv", index=False)

# 2. Generate 20 Lessons
lessons_data = [
    ("L01", "Mastering Technical Verbs & Tenses", "Grammar", "Intermediate", "Software Engineer", 30),
    ("L02", "Data Analysis Terminology & Jargon", "Vocabulary", "Intermediate", "Data Analyst", 25),
    ("L03", "Executive Summary Writing", "Writing", "Advanced", "Manager", 45),
    ("L04", "Public Speaking for Thesis Defense", "Speaking", "Advanced", "Researcher", 40),
    ("L05", "Formal Civil Service Correspondence", "Writing", "Intermediate", "Government Services", 35),
    ("L06", "Basic Sentence Structure & Punctuation", "Grammar", "Beginner", "Software Engineer", 20),
    ("L07", "Active Listening in Agile Standups", "Listening", "Beginner", "Software Engineer", 25),
    ("L08", "Explaining Metrics and KPI Dashboards", "Speaking", "Intermediate", "Data Analyst", 30),
    ("L09", "Conflict Resolution Dialogue & Tone", "Speaking", "Advanced", "Manager", 35),
    ("L10", "Research Paper Abstract Formulation", "Writing", "Advanced", "Researcher", 50),
    ("L11", "Essential Vocabulary for Tech Interviews", "Vocabulary", "Beginner", "Software Engineer", 20),
    ("L12", "Comprehending Fast-Paced Audio Briefings", "Listening", "Advanced", "Government Services", 30),
    ("L13", "Persuasive Pitching & Project Demos", "Speaking", "Intermediate", "Manager", 40),
    ("L14", "Prepositions & Phrasal Verbs in Reports", "Grammar", "Beginner", "Data Analyst", 25),
    ("L15", "Literature Review Synthesis Patterns", "Writing", "Advanced", "Researcher", 45),
    ("L16", "Pronunciation: Stress Patterns in Tech", "Speaking", "Beginner", "Software Engineer", 20),
    ("L17", "Interpreting Nuanced Stakeholder Audio", "Listening", "Intermediate", "Manager", 35),
    ("L18", "Statistical Inference Vocabulary", "Vocabulary", "Advanced", "Data Analyst", 30),
    ("L19", "Formal Policy Memo Drafting", "Writing", "Intermediate", "Government Services", 40),
    ("L20", "Academic Colloquium Q&A Responses", "Speaking", "Advanced", "Researcher", 30)
]
df_lessons = pd.DataFrame(lessons_data, columns=["lesson_id", "title", "skill", "level", "career_tag", "duration_min"])
df_lessons.to_csv("data/lessons.csv", index=False)

# 3. Store into SQLite
conn = sqlite3.connect("data/app.db")
df_students.to_sql("students", conn, if_exists="replace", index=False)
df_lessons.to_sql("lessons", conn, if_exists="replace", index=False)
conn.close()
print("Database generated successfully at data/app.db")