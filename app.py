import mysql.connector
import pandas as pd

# 1. Connect to MySQL
connection = mysql.connector.connect(
    user="paree",
    password=st.secrets["mysql_password"],
    database="academic_portal",
    unix_socket="/tmp/mysql.sock"
)

print("MySQL connected successfully!")


# 2. Get student data from MySQL
query = "SELECT * FROM student"

cursor = connection.cursor()
cursor.execute(query)

data = cursor.fetchall()
columns = cursor.column_names

df = pd.DataFrame(data, columns=columns)

cursor.close()
connection.close()


# 3. Calculate weighted points
df["weighted_points"] = df["credits"] * df["grade_point"]


# 4. Calculate semester-wise SGPA
sgpa = df.groupby(["student_name", "semester"]).agg(
    total_weighted_points=("weighted_points", "sum"),
    total_credits=("credits", "sum")
)

sgpa["SGPA"] = (
    sgpa["total_weighted_points"] /
    sgpa["total_credits"]
)


# 5. Display SGPA
print("\nSemester-wise SGPA:")
print(sgpa)


#creating cgpa
semester_result = sgpa.reset_index()

print("\nSemester Results:")
print(semester_result)

semester_result["weighted_sgpa"] = (
    semester_result["SGPA"] * semester_result["total_credits"]
)

cgpa = semester_result.groupby("student_name").agg(
    total_weighted_sgpa=("weighted_sgpa", "sum"),
    total_credits=("total_credits", "sum")
)

cgpa["CGPA"] = (
    cgpa["total_weighted_sgpa"] /
    cgpa["total_credits"]
)

print("\nFinal CGPA:")
print(cgpa)
