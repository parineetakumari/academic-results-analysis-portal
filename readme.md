# 🎓 Academic Results Analysis Portal

A dynamic web-based portal for managing and analyzing student academic performance using Python, MySQL, Pandas, Plotly, and Streamlit.

## 📌 Project Overview

The Academic Results Analysis Portal is designed to store student examination results in a MySQL database and provide an interactive dashboard for academic performance analysis.

The system dynamically calculates semester-wise SGPA and overall credit-weighted CGPA and presents the results through interactive charts and tables.

## 🚀 Features

- ➕ Add student results dynamically
- 🗄️ Store academic results in MySQL
- 📊 Calculate semester-wise SGPA
- 🎯 Calculate overall credit-weighted CGPA
- 📚 View subject-wise marks
- 📈 Analyze student academic performance
- 🏆 Compare students based on CGPA
- 📊 Visualize grade distribution
- 📉 Visualize CGPA comparison
- 🔐 Store database credentials securely using Streamlit secrets

## 🛠️ Technologies Used

- Python
- Streamlit
- MySQL
- Pandas
- Plotly
- mysql-connector-python
- Git & GitHub

## 🏗️ Project Architecture

```text
User
  ↓
Streamlit Dashboard
  ↓
Python
  ↓
MySQL Database
  ↓
Pandas
  ↓
SGPA / CGPA Calculation
  ↓
Plotly Visualizations
  ↓
Academic Performance Analysis

academic-results-analysis-portal/
│
├── app.py
├── dashboard.py
├── readme.md
├── .gitignore
│
└── .streamlit/
    └── secrets.toml

    📊 Dashboard Features
Student Performance

The dashboard allows users to select a student and semester to view:

Semester SGPA
Overall CGPA
Semester performancecat readme.md
Subject-wise marks
Grade Distribution

Displays the distribution of grades across the available student records using an interactive Plotly chart.

Student Comparison

Students can be compared based on their overall CGPA using:

CGPA comparison table
Interactive bar chart
🧮 SGPA Calculation

SGPA is calculated using subject credits and grade points:

SGPA = Σ(Credit × Grade Point) / Σ(Credit)
🧮 CGPA Calculation

The overall CGPA is calculated using a credit-weighted average of semester performance:

CGPA = Σ(SGPA × Semester Credits) / Σ(Semester Credits)