# import streamlit as st

# st.title("🎓 Academic Results Portal")

# st.write("Welcome to the Academic Results Analysis Portal!")

# st.success("Dashboard is working!")
#http://localhost:8501/

import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

st.title("🎓 Academic Results Portal")

st.write("Student Academic Performance Dashboard")

# Connect to MySQL
connection = mysql.connector.connect(
    user="paree",
    password=st.secrets["mysql_password"],
    database="academic_portal",
    unix_socket="/tmp/mysql.sock"
)

# Get data from MySQL
cursor = connection.cursor()
cursor.execute("SELECT * FROM student")

data = cursor.fetchall()
columns = cursor.column_names

df = pd.DataFrame(data, columns=columns)

cursor.close()
connection.close()


# -----------------------------
# SGPA Calculation
# -----------------------------

df["weighted_points"] = df["credits"] * df["grade_point"]

sgpa = df.groupby(["student_name", "semester"]).agg(
    total_weighted_points=("weighted_points", "sum"),
    total_credits=("credits", "sum")
)

sgpa["SGPA"] = (
    sgpa["total_weighted_points"] /
    sgpa["total_credits"]
)

semester_result = sgpa.reset_index()


# -----------------------------
# CGPA Calculation
# -----------------------------

semester_result["weighted_sgpa"] = (
    semester_result["SGPA"] *
    semester_result["total_credits"]
)

cgpa = semester_result.groupby("student_name").agg(
    total_weighted_sgpa=("weighted_sgpa", "sum"),
    total_credits=("total_credits", "sum")
)

cgpa["CGPA"] = (
    cgpa["total_weighted_sgpa"] /
    cgpa["total_credits"]
)

cgpa_result = cgpa.reset_index()

# Dashboard KPIs

total_students = df["student_id"].nunique()

average_sgpa = semester_result["SGPA"].mean()

average_cgpa = cgpa_result["CGPA"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("👨‍🎓 Total Students", total_students)

col2.metric("📊 Average SGPA", round(average_sgpa, 2))

col3.metric("🎯 Average CGPA", round(average_cgpa, 2))


# -----------------------------
# Display SGPA
# -----------------------------

st.subheader("📊 Semester-wise SGPA")

st.dataframe(
    semester_result[
        ["student_name", "semester", "SGPA"]
    ]
)

# -----------------------------
# SGPA Chart
# -----------------------------



# -----------------------------
# Display CGPA
# -----------------------------

st.subheader("🎯 Student CGPA")

st.dataframe(
    cgpa_result[
        ["student_name", "CGPA"]
    ]
)


# -----------------------------
# Student Selection
# -----------------------------

st.subheader("🔎 Student Performance")

student_list = cgpa_result["student_name"].tolist()

col1, col2 = st.columns(2)

with col1:
    selected_student = st.selectbox(
        "Select Student",
        student_list
    )

semester_list = sorted(
    semester_result[
        semester_result["student_name"] == selected_student
    ]["semester"].unique()
)

with col2:
    selected_semester = st.selectbox(
        "Select Semester",
        semester_list
    )

selected_cgpa = cgpa_result[
    cgpa_result["student_name"] == selected_student
]["CGPA"].iloc[0]

# st.metric(
#     "🎯 CGPA",
#     round(selected_cgpa, 2)
# )

student_sgpa = semester_result[
    (semester_result["student_name"] == selected_student) &
    (semester_result["semester"] == selected_semester)
]

# Selected semester SGPA
selected_sgpa = student_sgpa["SGPA"].iloc[0]

# Display SGPA and CGPA
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "🎯 Semester SGPA",
        f"{selected_sgpa:.2f}"
    )

with col2:
    st.metric(
        "📚 Overall CGPA",
        f"{selected_cgpa:.2f}"
    )

st.subheader(f"📊 {selected_student}'s Semester Performance")

st.dataframe(
    student_sgpa[
        ["semester", "SGPA"]
    ]
)

# -----------------------------
# SGPA Chart
# -----------------------------

fig = px.line(
    student_sgpa,
    x="semester",
    y="SGPA",
    markers=True,
    title=f"{selected_student}'s SGPA Trend"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Subject-wise Marks
# -----------------------------

student_data = df[
    (df["student_name"] == selected_student) &
    (df["semester"] == selected_semester)
]

# # -----------------------------
# # Attendance Analysis
# # -----------------------------

# st.subheader(
#     f"📅 {selected_student}'s Semester {selected_semester} Attendance"
# )

# fig_attendance = px.bar(
#     student_data,
#     x="subject",
#     y="attendance",
#     title=f"Attendance - Semester {selected_semester}",
#     text="attendance"
# )

# st.plotly_chart(
#     fig_attendance,
#     use_container_width=True
# )

# average_attendance = student_data["attendance"].mean()

# st.metric(
#     "📅 Average Attendance",
#     f"{average_attendance:.1f}%"
# )

st.subheader(f"📚 {selected_student}'s Subject-wise Marks")

fig_marks = px.bar(
    student_data,
    x="subject",
    y="marks",
    title=f"{selected_student}'s Subject Performance",
    text="marks"
)

st.plotly_chart(
    fig_marks,
    use_container_width=True
)





# -----------------------------
# Add Student Result
# -----------------------------

st.subheader("➕ Add Student Result")

with st.form("add_result_form"):

    student_id = st.number_input(
        "Student ID",
        min_value=1,
        step=1
    )

    student_name = st.text_input(
        "Student Name"
    )

    semester = st.number_input(
        "Semester",
        min_value=1,
        step=1
    )

    subject = st.text_input(
        "Subject"
    )

    credits = st.number_input(
        "Credits",
        min_value=1,
        step=1
    )

    marks = st.number_input(
        "Marks",
        min_value=0,
        max_value=100,
        step=1
    )

    grade = st.text_input(
        "Grade"
    )

    grade_point = st.number_input(
        "Grade Point",
        min_value=0,
        max_value=10,
        step=1
    )

    submitted = st.form_submit_button(
        "💾 Save Result"
    )

if submitted:

    connection = mysql.connector.connect(
        user="paree",
        password=st.secrets["mysql_password"],
        database="academic_portal",
        unix_socket="/tmp/mysql.sock"
    )

    cursor = connection.cursor()

    query = """
        INSERT INTO student
        (student_id, student_name, semester, subject,
         credits, marks, grade, grade_point, attendance)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        student_id,
        student_name,
        semester,
        subject,
        credits,
        marks,
        grade,
        grade_point,
        0
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

    st.success("✅ Result saved successfully!")

    st.rerun() 


# -----------------------------
# Grade Distribution
# -----------------------------

st.subheader("📊 Grade Distribution")

grade_counts = df["grade"].value_counts().reset_index()

grade_counts.columns = ["Grade", "Count"]

fig_grade = px.bar(
    grade_counts,
    x="Grade",
    y="Count",
    text="Count",
    title="Grade Distribution"
)

st.plotly_chart(
    fig_grade,
    use_container_width=True
)

# -----------------------------
# Student Comparison
# -----------------------------

st.subheader("🏆 Student Comparison")

comparison = cgpa_result[
    ["student_name", "CGPA"]
].copy()
comparison["CGPA"] = comparison["CGPA"].round(2)

comparison = comparison.sort_values(
    by="CGPA",
    ascending=False
)

st.dataframe(
    comparison,
    use_container_width=True
)

# -----------------------------
# CGPA Comparison Chart
# -----------------------------

fig_cgpa = px.bar(
    comparison,
    x="student_name",
    y="CGPA",
    text="CGPA",
    title="Student CGPA Comparison"
)

st.plotly_chart(
    fig_cgpa,
    use_container_width=True
)


